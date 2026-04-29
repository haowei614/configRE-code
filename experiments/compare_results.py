#!/usr/bin/env python3
"""Summarize configurable-agent QUARE experiment artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from statistics import mean
from statistics import pstdev
from typing import Any


RESULTS_DIR = Path("experiments/results")
SUMMARY_CSV = RESULTS_DIR / "comparison_summary.csv"
GROUND_TRUTH_FILE = Path("experiments/ground_truth/domain_relevance.json")

CONFIG_NAMES = {
    "config_a": "Fixed-5",
    "config_b": "Domain-optimized-6",
    "config_c": "Full-15",
    "config_d": "Phase0-Auto",
}
CONFIG_ORDER = {config_id: index for index, config_id in enumerate(CONFIG_NAMES)}

PHASE1_FILE = "phase1_initial_models.json"
PHASE2_FILE = "phase2_negotiation_trace.json"
PHASE3_FILE = "phase3_integrated_kaos_model.json"
PHASE4_FILE = "phase4_verification_report.json"
RUN_RECORD_FILE = "run_record.json"
PHASE0_FILE = "phase0_agent_selection.json"

METRIC_NAMES = [
    "requirement_count",
    "n_agents",
    "n_negotiations",
    "n_conflicts",
    "conflict_noise_count",
    "conflict_noise_rate",
    "asp",
    "asr",
    "dfs",
    "compliance_coverage",
    "verifiability",
    "feasibility",
    "bertscore",
    "phase0_tokens",
    "phase2_tokens",
    "input_tokens",
    "output_tokens",
    "total_tokens",
]

_GROUND_TRUTH_CACHE: dict[str, set[str] | None] = {}
_BERTSCORER: Any | None = None
_SEMANTIC_CACHE: dict[str, float | None] = {}


def main() -> None:
    rows = collect_run_rows()
    summary_rows = build_summary_rows(rows)
    write_summary_csv(summary_rows)
    print_summary_table(summary_rows)
    print(f"\nWrote summary CSV: {SUMMARY_CSV}")


def collect_run_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for config_dir in sorted(RESULTS_DIR.iterdir()):
        if not config_dir.is_dir():
            continue

        for seed_dir in sorted(config_dir.glob("seed_*")):
            if not seed_dir.is_dir():
                continue
            run_record = read_json(seed_dir / RUN_RECORD_FILE)
            if not isinstance(run_record, dict):
                continue
            case_id = str(run_record.get("case_id", "")).strip() or "UNKNOWN"
            config_id = normalize_config_id(config_dir.name)
            config_name = CONFIG_NAMES.get(config_id, config_dir.name)
            seed = seed_dir.name.removeprefix("seed_")
            row = {
                "case_id": case_id,
                "config_dir": config_dir.name,
                "config_id": config_id,
                "config_name": config_name,
                "seed": seed,
            }
            row.update(extract_metrics(seed_dir))
            rows.append(row)
    return rows


def normalize_config_id(config_dir_name: str) -> str:
    for config_id in CONFIG_NAMES:
        if config_dir_name == config_id or config_dir_name.endswith(f"_{config_id}"):
            return config_id
    return config_dir_name


def extract_metrics(run_dir: Path) -> dict[str, Any]:
    phase1 = read_json(run_dir / PHASE1_FILE)
    phase2 = read_json(run_dir / PHASE2_FILE)
    phase3 = read_json(run_dir / PHASE3_FILE)
    phase4 = read_json(run_dir / PHASE4_FILE)
    run_record = read_json(run_dir / RUN_RECORD_FILE)

    metrics: dict[str, Any] = {name: None for name in METRIC_NAMES}
    activated_agents = activated_agents_for_run(run_dir, phase1)
    case_id = str(run_record.get("case_id", "")) if isinstance(run_record, dict) else ""
    ground_truth_relevant = load_ground_truth(case_id)

    if activated_agents:
        metrics["n_agents"] = len(activated_agents)
        selection_metrics = compute_agent_selection_metrics(
            activated_agents,
            ground_truth_relevant,
        )
        metrics["asp"] = selection_metrics["agent_selection_precision"]
        metrics["asr"] = selection_metrics["agent_selection_recall"]
        metrics["dfs"] = selection_metrics["domain_fit_score"]

    if isinstance(phase1, dict):
        if metrics["n_agents"] is None:
            metrics["n_agents"] = len(phase1)
        metrics["requirement_count"] = sum(
            len(elements) for elements in phase1.values() if isinstance(elements, list)
        )

    if isinstance(phase2, dict):
        negotiations = phase2.get("negotiations", {})
        metrics["n_negotiations"] = phase2.get(
            "total_negotiations",
            len(negotiations) if isinstance(negotiations, dict) else None,
        )
        summary_stats = phase2.get("summary_stats", {})
        if isinstance(summary_stats, dict):
            metrics["n_conflicts"] = summary_stats.get("detected_conflicts")
        noise_count, noise_rate = compute_conflict_noise(phase2, ground_truth_relevant)
        metrics["conflict_noise_count"] = noise_count
        metrics["conflict_noise_rate"] = noise_rate

    if isinstance(phase4, dict):
        verification_results = phase4.get("verification_results", {})
        if isinstance(verification_results, dict):
            compliance = verification_results.get("compliance_coverage", {})
            if isinstance(compliance, dict):
                metrics["compliance_coverage"] = compliance.get("coverage_ratio")
            iso_scores = compute_iso29148_scores(phase3, phase4)
            metrics["verifiability"] = iso_scores.get("verifiability")
            metrics["feasibility"] = iso_scores.get("set_feasibility")

    metrics["bertscore"] = compute_semantic_preservation_f1(phase1, phase3)

    token_metrics = extract_token_metrics(run_record, run_dir)
    metrics.update(token_metrics)
    return metrics


def activated_agents_for_run(run_dir: Path, phase1: Any) -> list[str]:
    """Prefer Phase 0 selection output when present, then fall back to Phase 1 keys."""

    phase0 = read_json(run_dir / PHASE0_FILE)
    if isinstance(phase0, dict):
        selected_agents = phase0.get("selected_agents")
        if isinstance(selected_agents, list):
            return [str(agent) for agent in selected_agents if str(agent).strip()]

    if isinstance(phase1, dict):
        return [str(agent) for agent in phase1.keys()]

    return []


def load_ground_truth(case_id: str) -> set[str] | None:
    """Load independent domain-relevance labels for the current case."""

    normalized_case_id = case_id.strip()
    if normalized_case_id in _GROUND_TRUTH_CACHE:
        return _GROUND_TRUTH_CACHE[normalized_case_id]

    payload = read_json(GROUND_TRUTH_FILE)
    if not isinstance(payload, dict):
        print(f"Warning: unable to read ground truth file: {GROUND_TRUTH_FILE}")
        _GROUND_TRUTH_CACHE[normalized_case_id] = None
        return None

    case_payload = payload.get(normalized_case_id)
    if not isinstance(case_payload, dict):
        print(f"Warning: no ground truth relevance labels for case_id={normalized_case_id!r}")
        _GROUND_TRUTH_CACHE[normalized_case_id] = None
        return None

    relevant_agents = case_payload.get("relevant_agents")
    if not isinstance(relevant_agents, list):
        print(f"Warning: invalid relevant_agents for case_id={normalized_case_id!r}")
        _GROUND_TRUTH_CACHE[normalized_case_id] = None
        return None

    result = {str(agent) for agent in relevant_agents if str(agent).strip()}
    _GROUND_TRUTH_CACHE[normalized_case_id] = result
    return result


def compute_agent_selection_metrics(
    activated_agents: list[str],
    ground_truth_relevant: set[str] | None,
) -> dict[str, Any]:
    if ground_truth_relevant is None:
        return {
            "agent_selection_precision": None,
            "agent_selection_recall": None,
            "domain_fit_score": None,
            "relevant_activated": [],
            "relevant_missed": [],
            "irrelevant_activated": [],
        }

    activated = set(activated_agents)
    relevant_activated = activated & ground_truth_relevant
    relevant_missed = ground_truth_relevant - activated
    irrelevant_activated = activated - ground_truth_relevant

    precision = len(relevant_activated) / len(activated) if activated else 0.0
    recall = len(relevant_activated) / len(ground_truth_relevant) if ground_truth_relevant else 0.0
    domain_fit_score = (
        2 * precision * recall / (precision + recall) if precision + recall > 0 else 0.0
    )
    return {
        "agent_selection_precision": precision,
        "agent_selection_recall": recall,
        "domain_fit_score": domain_fit_score,
        "relevant_activated": sorted(relevant_activated),
        "relevant_missed": sorted(relevant_missed),
        "irrelevant_activated": sorted(irrelevant_activated),
    }


def extract_token_metrics(run_record: Any, run_dir: Path) -> dict[str, Any]:
    """Extract token usage from run_record, with Phase 0 artifact fallback."""

    result = {
        "phase0_tokens": None,
        "phase2_tokens": None,
        "input_tokens": None,
        "output_tokens": None,
        "total_tokens": None,
    }
    token_usage = run_record.get("token_usage") if isinstance(run_record, dict) else None
    if isinstance(token_usage, dict):
        phase0_usage = coerce_usage_dict(token_usage.get("phase0"))
        phase2_usage = coerce_usage_dict(token_usage.get("phase2"))
        total_usage = coerce_usage_dict(token_usage.get("total"))
        result["phase0_tokens"] = phase0_usage.get("total_tokens")
        result["phase2_tokens"] = phase2_usage.get("total_tokens")
        result["input_tokens"] = total_usage.get("input_tokens")
        result["output_tokens"] = total_usage.get("output_tokens")
        result["total_tokens"] = total_usage.get("total_tokens")

    phase0 = read_json(run_dir / PHASE0_FILE)
    if result["phase0_tokens"] is None and isinstance(phase0, dict):
        phase0_usage = coerce_usage_dict(phase0.get("token_usage"))
        result["phase0_tokens"] = phase0_usage.get("total_tokens")
        if result["total_tokens"] is None:
            result["input_tokens"] = phase0_usage.get("input_tokens")
            result["output_tokens"] = phase0_usage.get("output_tokens")
            result["total_tokens"] = phase0_usage.get("total_tokens")

    if isinstance(run_record, dict) and result["total_tokens"] is None:
        result["input_tokens"] = find_first_numeric_by_key(
            run_record,
            ("input_tokens", "prompt_tokens"),
        )
        result["output_tokens"] = find_first_numeric_by_key(
            run_record,
            ("output_tokens", "completion_tokens"),
        )
        result["total_tokens"] = find_first_numeric_by_key(run_record, ("total_tokens",))
    return result


def coerce_usage_dict(value: Any) -> dict[str, float | None]:
    if not isinstance(value, dict):
        return {"input_tokens": None, "output_tokens": None, "total_tokens": None}
    return {
        "input_tokens": to_float(value.get("input_tokens")),
        "output_tokens": to_float(value.get("output_tokens")),
        "total_tokens": to_float(value.get("total_tokens")),
    }


def compute_iso29148_scores(phase3: Any, phase4: Any) -> dict[str, float]:
    """Mirror comparison_harness ISO29148 score derivation from phase artifacts."""

    verification_results = phase4.get("verification_results", {}) if isinstance(phase4, dict) else {}
    if not isinstance(verification_results, dict):
        verification_results = {}

    s_logic = to_float(verification_results.get("s_logic")) or 0.0
    s_term = to_float(
        nested_get(
            verification_results,
            ("terminology_consistency", "consistency_ratio"),
        )
    )
    if s_term is None:
        s_term = 0.0
    compliance_coverage = to_float(
        nested_get(
            verification_results,
            ("compliance_coverage", "coverage_ratio"),
        )
    )
    if compliance_coverage is None:
        compliance_coverage = 0.0

    topology_valid = int(
        bool(
            nested_get(phase3, ("topology_status", "is_valid"))
            if isinstance(phase3, dict)
            else False
        )
    )
    deterministic_valid = int(
        bool(
            nested_get(phase4, ("deterministic_validation", "is_valid"))
            if isinstance(phase4, dict)
            else False
        )
    )

    normalized_logic = clamp01(s_logic)
    normalized_term = clamp01(s_term)
    normalized_topology = clamp01(float(topology_valid))
    normalized_deterministic = clamp01(float(deterministic_valid))
    normalized_compliance = clamp01(compliance_coverage)

    return {
        "unambiguous": likert_from_ratio(0.55 * normalized_term + 0.45 * normalized_logic),
        "correctness": likert_from_ratio(0.70 * normalized_logic + 0.30 * normalized_deterministic),
        "verifiability": likert_from_ratio(
            0.50 * normalized_deterministic + 0.50 * normalized_compliance
        ),
        "set_consistency": likert_from_ratio(0.50 * normalized_logic + 0.50 * normalized_topology),
        "set_feasibility": likert_from_ratio(
            0.60 * normalized_compliance + 0.40 * normalized_deterministic
        ),
    }


def compute_semantic_preservation_f1(phase1: Any, phase3: Any) -> float | None:
    """Compute BERTScore F1 for Phase 3 descriptions against Phase 1 descriptions."""

    candidates = phase3_requirement_texts(phase3)
    references = phase1_requirement_texts(phase1)
    if not candidates or not references:
        return None

    cache_key = json.dumps(
        {"candidates": candidates, "references": references},
        ensure_ascii=False,
        sort_keys=True,
    )
    if cache_key in _SEMANTIC_CACHE:
        return _SEMANTIC_CACHE[cache_key]

    try:
        scorer = get_bertscorer()
    except Exception:
        return None

    pair_candidates: list[str] = []
    pair_references: list[str] = []
    row_offsets: list[tuple[int, int]] = []
    for candidate in candidates:
        start = len(pair_candidates)
        for reference in references:
            pair_candidates.append(candidate)
            pair_references.append(reference)
        row_offsets.append((start, len(pair_candidates)))

    try:
        _, _, f1_values = scorer.score(
            pair_candidates,
            pair_references,
            batch_size=64,
            verbose=False,
        )
    except Exception:
        return None

    f1_scores: list[float] = []
    for start, end in row_offsets:
        row = f1_values[start:end]
        best_index = int(row.argmax().item())
        f1_scores.append(float(row[best_index].item()))
    result = sum(f1_scores) / len(f1_scores) if f1_scores else None
    _SEMANTIC_CACHE[cache_key] = result
    return result


def get_bertscorer() -> Any:
    global _BERTSCORER
    if _BERTSCORER is not None:
        return _BERTSCORER

    from bert_score import BERTScorer  # type: ignore[import-not-found]

    _BERTSCORER = BERTScorer(
        model_type="bert-base-uncased",
        lang="en",
        rescale_with_baseline=False,
    )
    return _BERTSCORER


def phase1_requirement_texts(phase1: Any) -> list[str]:
    texts: list[str] = []
    if not isinstance(phase1, dict):
        return texts
    for elements in phase1.values():
        if not isinstance(elements, list):
            continue
        for element in elements:
            if not isinstance(element, dict):
                continue
            description = str(element.get("description", "")).strip()
            if description:
                texts.append(description)
    return texts


def phase3_requirement_texts(phase3: Any) -> list[str]:
    texts: list[str] = []
    if not isinstance(phase3, dict):
        return texts
    elements = phase3.get("gsn_elements", [])
    if not isinstance(elements, list):
        return texts
    for element in elements:
        if not isinstance(element, dict):
            continue
        name = str(element.get("name", "")).strip()
        description = str(element.get("description", "")).strip()
        text = f"{name}. {description}".strip(" .")
        if text:
            texts.append(text)
    return texts


def compute_conflict_noise(
    phase2: dict[str, Any],
    relevant_agents: set[str] | None,
) -> tuple[int | None, float | None]:
    """Count detected conflict pairs involving agents outside ground-truth relevance."""

    if relevant_agents is None:
        return None, None

    negotiations = phase2.get("negotiations", {})
    if not isinstance(negotiations, dict):
        return 0, None

    detected_pairs = 0
    noisy_pairs = 0
    for negotiation in negotiations.values():
        if not isinstance(negotiation, dict):
            continue
        steps = negotiation.get("steps", [])
        if not isinstance(steps, list):
            continue
        conflict_steps = [
            step for step in steps if isinstance(step, dict) and bool(step.get("conflict_detected"))
        ]
        if not conflict_steps:
            continue
        detected_pairs += 1
        involved_agents = set()
        focus_agent = str(negotiation.get("focus_agent", "")).strip()
        if focus_agent:
            involved_agents.add(focus_agent)
        reviewer_agents = negotiation.get("reviewer_agents", [])
        if isinstance(reviewer_agents, list):
            involved_agents.update(str(agent).strip() for agent in reviewer_agents if str(agent).strip())
        for step in conflict_steps:
            for key in ("focus_agent", "reviewer_agent"):
                agent = str(step.get(key, "")).strip()
                if agent:
                    involved_agents.add(agent)
        if any(agent not in relevant_agents for agent in involved_agents):
            noisy_pairs += 1

    if detected_pairs == 0:
        return 0, 0.0
    return noisy_pairs, noisy_pairs / detected_pairs


def build_summary_rows(rows: list[dict[str, Any]]) -> list[dict[str, str]]:
    summary_rows: list[dict[str, str]] = []
    group_keys = sorted(
        {(row["case_id"], row["config_id"], row["config_name"]) for row in rows},
        key=lambda item: (item[0], CONFIG_ORDER.get(item[1], 999), item[1]),
    )
    for case_id, config_id, config_name in group_keys:
        config_rows = [
            row for row in rows if row["case_id"] == case_id and row["config_id"] == config_id
        ]
        summary: dict[str, str] = {
            "case_id": case_id,
            "config_id": config_id,
            "config_name": config_name,
            "runs": str(len(config_rows)),
        }
        for metric_name in METRIC_NAMES:
            values = [to_float(row.get(metric_name)) for row in config_rows]
            numeric_values = [value for value in values if value is not None]
            if numeric_values:
                summary[f"{metric_name}_mean"] = format_value(mean(numeric_values))
                summary[f"{metric_name}_std"] = format_value(pstdev(numeric_values))
            else:
                summary[f"{metric_name}_mean"] = "N/A"
                summary[f"{metric_name}_std"] = "N/A"
        summary_rows.append(summary)
    return summary_rows


def write_summary_csv(summary_rows: list[dict[str, str]]) -> None:
    SUMMARY_CSV.parent.mkdir(parents=True, exist_ok=True)
    columns = ["case_id", "config_id", "config_name", "runs"]
    for metric_name in METRIC_NAMES:
        columns.extend([f"{metric_name}_mean", f"{metric_name}_std"])

    with SUMMARY_CSV.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        for row in summary_rows:
            writer.writerow({column: row.get(column, "N/A") for column in columns})


def print_summary_table(summary_rows: list[dict[str, str]]) -> None:
    display_metrics = [
        "asp",
        "asr",
        "dfs",
        "phase0_tokens",
        "phase2_tokens",
        "total_tokens",
        "conflict_noise_rate",
        "compliance_coverage",
        "bertscore",
    ]
    headers = ["case", "config", "runs", *display_metrics]
    table_rows: list[list[str]] = []
    for row in summary_rows:
        table_rows.append(
            [
                row["case_id"],
                row["config_name"],
                row["runs"],
                *[
                    mean_std_text(row[f"{metric}_mean"], row[f"{metric}_std"])
                    for metric in display_metrics
                ],
            ]
        )

    widths = [
        max(len(headers[index]), *(len(table_row[index]) for table_row in table_rows))
        for index in range(len(headers))
    ]
    print(format_table_row(headers, widths))
    print(format_table_row(["-" * width for width in widths], widths))
    for table_row in table_rows:
        print(format_table_row(table_row, widths))


def read_json(path: Path) -> Any:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def find_first_numeric_by_key(node: Any, key_fragments: tuple[str, ...]) -> float | None:
    if isinstance(node, dict):
        for key, value in node.items():
            normalized_key = str(key).lower().replace("_", "").replace("-", "")
            if any(fragment.replace("_", "").replace("-", "") in normalized_key for fragment in key_fragments):
                numeric_value = to_float(value)
                if numeric_value is not None:
                    return numeric_value
            nested_value = find_first_numeric_by_key(value, key_fragments)
            if nested_value is not None:
                return nested_value
    elif isinstance(node, list):
        for item in node:
            nested_value = find_first_numeric_by_key(item, key_fragments)
            if nested_value is not None:
                return nested_value
    return None


def nested_get(node: Any, path: tuple[str, ...]) -> Any:
    cursor = node
    for key in path:
        if not isinstance(cursor, dict):
            return None
        cursor = cursor.get(key)
    return cursor


def to_float(value: Any) -> float | None:
    if isinstance(value, bool) or value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        try:
            return float(value)
        except ValueError:
            return None
    return None


def clamp01(value: float) -> float:
    return max(0.0, min(1.0, value))


def likert_from_ratio(value: float) -> float:
    return round(1.0 + 4.0 * clamp01(value), 6)


def format_value(value: float) -> str:
    return f"{value:.6f}".rstrip("0").rstrip(".")


def mean_std_text(mean_value: str, std_value: str) -> str:
    if mean_value == "N/A":
        return "N/A"
    return f"{mean_value} +/- {std_value}"


def format_table_row(values: list[str], widths: list[int]) -> str:
    return " | ".join(value.ljust(widths[index]) for index, value in enumerate(values))


if __name__ == "__main__":
    main()

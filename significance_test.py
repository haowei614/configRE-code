#!/usr/bin/env python3
"""Statistical significance tests for ConfigRE configuration experiments."""

from __future__ import annotations

import argparse
import csv
import json
import math
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from statistics import mean
from statistics import stdev
from typing import Any

from scipy.stats import wilcoxon


CONFIG_NAMES = {
    "config_a": "Fixed-5",
    "config_b": "Domain-opt",
    "config_c": "Full-15",
    "config_d": "Phase0-Auto",
}
CONFIG_ORDER = ["config_a", "config_c", "config_b", "config_d"]
CASE_ORDER = ["AD", "ATM", "Library", "RollCall", "Bookkeeping"]
METRICS = {
    "dfs": "DFS",
    "cnr": "CNR",
}
COMPARISONS = [
    ("config_d", "config_a"),
    ("config_d", "config_c"),
    ("config_d", "config_b"),
]


TABLE_IV_FALLBACK = [
    ("AD", "config_a", 0.55, 0.11),
    ("AD", "config_b", 0.83, 0.22),
    ("AD", "config_c", 0.57, 0.65),
    ("AD", "config_d", 0.86, 0.13),
    ("ATM", "config_a", 0.36, 0.00),
    ("ATM", "config_b", 0.83, 0.33),
    ("ATM", "config_c", 0.57, 0.67),
    ("ATM", "config_d", 0.77, 0.00),
    ("Bookkeeping", "config_a", 0.40, 0.60),
    ("Bookkeeping", "config_b", 0.73, 0.00),
    ("Bookkeeping", "config_c", 0.50, 0.80),
    ("Bookkeeping", "config_d", 0.78, 0.33),
    ("Library", "config_a", 0.00, 0.60),
    ("Library", "config_b", 0.73, 0.00),
    ("Library", "config_c", 0.50, 0.33),
    ("Library", "config_d", 0.64, 0.11),
    ("RollCall", "config_a", 0.00, 0.50),
    ("RollCall", "config_b", 0.73, 0.20),
    ("RollCall", "config_c", 0.50, 1.00),
    ("RollCall", "config_d", 0.66, 0.30),
]


@dataclass(frozen=True)
class RunMetric:
    case_id: str
    config_id: str
    seed: str
    dfs: float
    cnr: float


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run ConfigRE descriptive statistics and paired Wilcoxon tests."
    )
    parser.add_argument("--results-dir", type=Path, default=Path("experiments/results"))
    parser.add_argument(
        "--summary-csv",
        type=Path,
        default=Path("experiments/results/comparison_summary_paper_final.csv"),
    )
    parser.add_argument(
        "--ground-truth",
        type=Path,
        default=Path("experiments/ground_truth/domain_relevance.json"),
    )
    parser.add_argument("--output", type=Path, default=Path("significance_results.txt"))
    args = parser.parse_args()

    ground_truth = load_ground_truth(args.ground_truth)
    rows = collect_raw_metrics(args.results_dir, ground_truth)
    source = "raw per-seed phase artifacts"
    has_seed_data = True

    if not rows:
        rows = collect_summary_metrics(args.summary_csv)
        source = f"summary CSV fallback ({args.summary_csv})"
        has_seed_data = False

    if not rows:
        rows = collect_table_iv_fallback()
        source = "embedded Table IV fallback means"
        has_seed_data = False

    report = build_report(rows, source=source, has_seed_data=has_seed_data)
    print(report)
    args.output.write_text(report + "\n", encoding="utf-8")


def load_ground_truth(path: Path) -> dict[str, set[str]]:
    payload = read_json(path)
    if not isinstance(payload, dict):
        return {}

    result: dict[str, set[str]] = {}
    for case_id, case_payload in payload.items():
        if not isinstance(case_payload, dict):
            continue
        relevant_agents = case_payload.get("relevant_agents")
        if not isinstance(relevant_agents, list):
            continue
        result[str(case_id)] = {str(agent) for agent in relevant_agents if str(agent).strip()}
    return result


def collect_raw_metrics(results_dir: Path, ground_truth: dict[str, set[str]]) -> list[RunMetric]:
    rows: list[RunMetric] = []
    if not results_dir.exists():
        return rows

    for config_dir in sorted(path for path in results_dir.iterdir() if path.is_dir()):
        config_id = normalize_config_id(config_dir.name)
        if config_id not in CONFIG_NAMES:
            continue

        for seed_dir in sorted(config_dir.glob("seed_*")):
            run_record = read_json(seed_dir / "run_record.json")
            if not isinstance(run_record, dict):
                continue

            case_id = str(run_record.get("case_id", "")).strip()
            if not case_id:
                continue

            phase1 = read_json(seed_dir / "phase1_initial_models.json")
            phase2 = read_json(seed_dir / "phase2_negotiation_trace.json")
            phase0 = read_json(seed_dir / "phase0_agent_selection.json")
            relevant_agents = ground_truth.get(case_id)
            if not relevant_agents:
                continue

            activated_agents = activated_agents_for_run(phase0, phase1)
            dfs = compute_dfs(activated_agents, relevant_agents)
            cnr = compute_conflict_noise_rate(phase2, relevant_agents)
            if dfs is None or cnr is None:
                continue

            rows.append(
                RunMetric(
                    case_id=case_id,
                    config_id=config_id,
                    seed=seed_dir.name.removeprefix("seed_"),
                    dfs=dfs,
                    cnr=cnr,
                )
            )
    return rows


def normalize_config_id(config_dir_name: str) -> str:
    for config_id in CONFIG_NAMES:
        if config_dir_name == config_id or config_dir_name.endswith(f"_{config_id}"):
            return config_id
    return config_dir_name


def activated_agents_for_run(phase0: Any, phase1: Any) -> list[str]:
    if isinstance(phase0, dict):
        selected_agents = phase0.get("selected_agents")
        if isinstance(selected_agents, list):
            return [str(agent) for agent in selected_agents if str(agent).strip()]

    if isinstance(phase1, dict):
        return [str(agent) for agent in phase1 if str(agent).strip()]

    return []


def compute_dfs(activated_agents: list[str], relevant_agents: set[str]) -> float | None:
    if not relevant_agents:
        return None

    activated = set(activated_agents)
    precision = len(activated & relevant_agents) / len(activated) if activated else 0.0
    recall = len(activated & relevant_agents) / len(relevant_agents)
    if precision + recall == 0:
        return 0.0
    return 2 * precision * recall / (precision + recall)


def compute_conflict_noise_rate(phase2: Any, relevant_agents: set[str]) -> float | None:
    if not isinstance(phase2, dict):
        return None

    negotiations = phase2.get("negotiations", {})
    if not isinstance(negotiations, dict):
        return None

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

    return 0.0 if detected_pairs == 0 else noisy_pairs / detected_pairs


def collect_summary_metrics(summary_csv: Path) -> list[RunMetric]:
    if not summary_csv.exists():
        return []

    rows: list[RunMetric] = []
    with summary_csv.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for record in reader:
            config_id = str(record.get("config_id", "")).strip()
            if config_id not in CONFIG_NAMES:
                continue
            dfs = to_float(record.get("dfs_mean"))
            cnr = to_float(record.get("conflict_noise_rate_mean"))
            case_id = str(record.get("case_id", "")).strip()
            if case_id and dfs is not None and cnr is not None:
                rows.append(RunMetric(case_id=case_id, config_id=config_id, seed="mean", dfs=dfs, cnr=cnr))
    return rows


def collect_table_iv_fallback() -> list[RunMetric]:
    return [
        RunMetric(case_id=case_id, config_id=config_id, seed="mean", dfs=dfs, cnr=cnr)
        for case_id, config_id, dfs, cnr in TABLE_IV_FALLBACK
    ]


def build_report(rows: list[RunMetric], source: str, has_seed_data: bool) -> str:
    case_means = build_case_means(rows)
    lines = [
        "ConfigRE Statistical Significance Test",
        "=" * 42,
        f"Data source: {source}",
        "CNR is conflict_noise_rate. Wilcoxon tests are paired by case study (n=5).",
        "All SD values use sample standard deviation (ddof=1) when n > 1.",
        "",
        "Descriptive statistics",
        "----------------------",
    ]

    descriptive_rows = descriptive_statistics(rows, case_means)
    lines.extend(
        format_table(
            ["Config", "Metric", "Mean", "Across-case SD", "Mean seed SD", "Max seed SD"],
            descriptive_rows,
        )
    )

    lines.extend(["", "Paired Wilcoxon signed-rank tests", "---------------------------------"])
    test_rows = wilcoxon_statistics(case_means)
    lines.extend(
        format_table(
            [
                "Comparison",
                "Metric",
                "Auto mean",
                "Baseline mean",
                "Mean diff",
                "W",
                "p",
                "Cliff delta",
            ],
            test_rows,
        )
    )

    if has_seed_data:
        lines.extend(["", "Across-seed DFS stability", "-------------------------"])
        stability_rows = seed_stability_statistics(rows)
        lines.extend(format_table(["Case", "Config", "Seed DFS values", "Seed DFS SD"], stability_rows))
    else:
        lines.extend(
            [
                "",
                "Across-seed DFS stability",
                "-------------------------",
                "Not available because the script used case-level fallback means rather than per-seed artifacts.",
            ]
        )

    return "\n".join(lines)


def build_case_means(rows: list[RunMetric]) -> dict[tuple[str, str, str], float]:
    grouped: dict[tuple[str, str, str], list[float]] = defaultdict(list)
    for row in rows:
        grouped[(row.case_id, row.config_id, "dfs")].append(row.dfs)
        grouped[(row.case_id, row.config_id, "cnr")].append(row.cnr)
    return {key: mean(values) for key, values in grouped.items()}


def descriptive_statistics(
    rows: list[RunMetric],
    case_means: dict[tuple[str, str, str], float],
) -> list[list[str]]:
    table_rows: list[list[str]] = []
    for config_id in CONFIG_ORDER:
        for metric_key, metric_label in METRICS.items():
            values = [
                case_means[(case_id, config_id, metric_key)]
                for case_id in CASE_ORDER
                if (case_id, config_id, metric_key) in case_means
            ]
            seed_sds = per_case_seed_sds(rows, config_id, metric_key)
            table_rows.append(
                [
                    CONFIG_NAMES[config_id],
                    metric_label,
                    fmt(mean(values)) if values else "N/A",
                    fmt(sample_sd(values)) if len(values) > 1 else "N/A",
                    fmt(mean(seed_sds)) if seed_sds else "N/A",
                    fmt(max(seed_sds)) if seed_sds else "N/A",
                ]
            )
    return table_rows


def per_case_seed_sds(rows: list[RunMetric], config_id: str, metric_key: str) -> list[float]:
    grouped: dict[str, list[float]] = defaultdict(list)
    for row in rows:
        if row.config_id != config_id:
            continue
        grouped[row.case_id].append(getattr(row, metric_key))
    return [sample_sd(values) for values in grouped.values() if len(values) > 1]


def wilcoxon_statistics(case_means: dict[tuple[str, str, str], float]) -> list[list[str]]:
    table_rows: list[list[str]] = []
    for auto_config, baseline_config in COMPARISONS:
        for metric_key, metric_label in METRICS.items():
            paired = [
                (
                    case_means[(case_id, auto_config, metric_key)],
                    case_means[(case_id, baseline_config, metric_key)],
                )
                for case_id in CASE_ORDER
                if (case_id, auto_config, metric_key) in case_means
                and (case_id, baseline_config, metric_key) in case_means
            ]
            auto_values = [auto_value for auto_value, _ in paired]
            baseline_values = [baseline_value for _, baseline_value in paired]
            statistic, p_value = paired_wilcoxon(auto_values, baseline_values)
            diff = [auto - baseline for auto, baseline in paired]
            table_rows.append(
                [
                    f"{CONFIG_NAMES[auto_config]} vs {CONFIG_NAMES[baseline_config]}",
                    metric_label,
                    fmt(mean(auto_values)),
                    fmt(mean(baseline_values)),
                    fmt(mean(diff)),
                    fmt(statistic),
                    fmt(p_value),
                    fmt(cliffs_delta(auto_values, baseline_values)),
                ]
            )
    return table_rows


def paired_wilcoxon(auto_values: list[float], baseline_values: list[float]) -> tuple[float, float]:
    if not auto_values or len(auto_values) != len(baseline_values):
        return math.nan, math.nan

    if all(math.isclose(auto, baseline) for auto, baseline in zip(auto_values, baseline_values)):
        return 0.0, 1.0

    try:
        result = wilcoxon(auto_values, baseline_values, alternative="two-sided", zero_method="wilcox")
    except ValueError:
        return math.nan, math.nan
    return float(result.statistic), float(result.pvalue)


def cliffs_delta(left: list[float], right: list[float]) -> float:
    if not left or not right:
        return math.nan

    greater = 0
    less = 0
    for left_value in left:
        for right_value in right:
            if left_value > right_value:
                greater += 1
            elif left_value < right_value:
                less += 1
    return (greater - less) / (len(left) * len(right))


def seed_stability_statistics(rows: list[RunMetric]) -> list[list[str]]:
    grouped: dict[tuple[str, str], list[RunMetric]] = defaultdict(list)
    for row in rows:
        grouped[(row.case_id, row.config_id)].append(row)

    table_rows: list[list[str]] = []
    for case_id in CASE_ORDER:
        for config_id in CONFIG_ORDER:
            values = sorted(grouped.get((case_id, config_id), []), key=lambda item: item.seed)
            if not values:
                continue
            dfs_values = [row.dfs for row in values]
            table_rows.append(
                [
                    case_id,
                    CONFIG_NAMES[config_id],
                    ", ".join(fmt(value) for value in dfs_values),
                    fmt(sample_sd(dfs_values)) if len(dfs_values) > 1 else "N/A",
                ]
            )
    return table_rows


def read_json(path: Path) -> Any:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def to_float(value: Any) -> float | None:
    if value is None or isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        if value.strip().upper() == "N/A":
            return None
        try:
            return float(value)
        except ValueError:
            return None
    return None


def sample_sd(values: list[float]) -> float:
    return stdev(values) if len(values) > 1 else 0.0


def fmt(value: float) -> str:
    if math.isnan(value):
        return "N/A"
    return f"{value:.4f}".rstrip("0").rstrip(".")


def format_table(headers: list[str], rows: list[list[str]]) -> list[str]:
    widths = [
        max(len(headers[index]), *(len(row[index]) for row in rows)) if rows else len(headers[index])
        for index in range(len(headers))
    ]
    separator = ["-" * width for width in widths]
    return [
        format_table_row(headers, widths),
        format_table_row(separator, widths),
        *(format_table_row(row, widths) for row in rows),
    ]


def format_table_row(values: list[str], widths: list[int]) -> str:
    return " | ".join(value.ljust(widths[index]) for index, value in enumerate(values))


if __name__ == "__main__":
    main()

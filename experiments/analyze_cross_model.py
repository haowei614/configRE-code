#!/usr/bin/env python3
"""Analyze cross-model validation results and generate comparison table."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from statistics import mean, pstdev
from typing import Any

CROSS_MODEL_DIR = Path("experiments/results/cross_model")
GROUND_TRUTH_FILE = Path("experiments/ground_truth/domain_relevance.json")
OUTPUT_CSV = Path("experiments/results/cross_model_summary.csv")
OUTPUT_LATEX = Path("experiments/results/cross_model_table.tex")

ORIGINAL_MODEL = "gpt-4o-mini"


def load_ground_truth() -> dict[str, set[str]]:
    data = json.loads(GROUND_TRUTH_FILE.read_text())
    return {
        case_id: set(case_data["relevant_agents"])
        for case_id, case_data in data.items()
    }


def compute_dfs(activated: list[str], gt: set[str]) -> dict[str, float]:
    activated_set = set(activated)
    relevant = activated_set & gt
    precision = len(relevant) / len(activated_set) if activated_set else 0.0
    recall = len(relevant) / len(gt) if gt else 0.0
    dfs = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0
    return {"asp": precision, "asr": recall, "dfs": dfs, "n_agents": len(activated_set)}


def collect_results(gt_map: dict[str, set[str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for model_dir in sorted(CROSS_MODEL_DIR.iterdir()):
        if not model_dir.is_dir():
            continue
        model_name = model_dir.name

        for case_dir in sorted(model_dir.iterdir()):
            if not case_dir.is_dir():
                continue
            case_id = case_dir.name

            for config_dir in sorted(case_dir.iterdir()):
                if not config_dir.is_dir():
                    continue
                config = config_dir.name

                seed_metrics: list[dict[str, float]] = []
                for seed_dir in sorted(config_dir.glob("seed_*")):
                    phase0_file = seed_dir / "phase0_agent_selection.json"

                    if config == "auto" and phase0_file.exists():
                        phase0 = json.loads(phase0_file.read_text())
                        activated = phase0.get("selected_agents", [])
                    elif config == "fixed5":
                        activated = [
                            "SafetyAgent", "EfficiencyAgent", "GreenAgent",
                            "TrustworthinessAgent", "ResponsibilityAgent",
                        ]
                    else:
                        continue

                    metrics = compute_dfs(activated, gt_map.get(case_id, set()))
                    seed_metrics.append(metrics)

                if seed_metrics:
                    row: dict[str, Any] = {
                        "model": model_name,
                        "case_id": case_id,
                        "config": config,
                        "runs": len(seed_metrics),
                    }
                    for m in ["asp", "asr", "dfs", "n_agents"]:
                        vals = [s[m] for s in seed_metrics]
                        row[f"{m}_mean"] = mean(vals)
                        row[f"{m}_std"] = pstdev(vals)
                    rows.append(row)
    return rows


def write_csv(rows: list[dict[str, Any]]) -> None:
    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    columns = ["model", "case_id", "config", "runs"]
    for m in ["asp", "asr", "dfs", "n_agents"]:
        columns.extend([f"{m}_mean", f"{m}_std"])
    with OUTPUT_CSV.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        for row in rows:
            writer.writerow({c: f"{row.get(c, 'N/A')}" for c in columns})
    print(f"CSV saved: {OUTPUT_CSV} ({len(rows)} rows)")


def generate_latex_table(rows: list[dict[str, Any]]) -> None:
    models = sorted({r["model"] for r in rows})
    cases = sorted({r["case_id"] for r in rows})

    lines = [
        r"\begin{table*}[t]",
        r"\centering",
        r"\caption{Cross-Model Validation: Phase0-Auto DFS Across LLM Backbones (averaged over 3 seeds)}",
        r"\label{tab:cross_model}",
    ]

    col_spec = "l l" + " c" * len(cases) + " c"
    lines.append(r"\begin{tabular}{" + col_spec + "}")
    lines.append(r"\toprule")

    header = r"\textbf{Model} & \textbf{Config}"
    for case_id in cases:
        header += f" & \\textbf{{{case_id}}}"
    header += r" & \textbf{Avg} \\"
    lines.append(header)
    lines.append(r"\midrule")

    for model in models:
        for config in ["fixed5", "auto"]:
            config_label = "Fixed-5" if config == "fixed5" else "Phase0-Auto"
            row_str = f"{model} & {config_label}"
            case_dfs: list[float] = []
            for case_id in cases:
                matching = [
                    r for r in rows
                    if r["model"] == model and r["case_id"] == case_id and r["config"] == config
                ]
                if matching:
                    dfs_val = matching[0]["dfs_mean"]
                    row_str += f" & {dfs_val:.2f}"
                    case_dfs.append(dfs_val)
                else:
                    row_str += " & --"
            avg_dfs = f"{mean(case_dfs):.2f}" if case_dfs else "--"
            row_str += f" & \\textbf{{{avg_dfs}}} \\\\"
            lines.append(row_str)
        lines.append(r"\midrule")

    lines[-1] = r"\bottomrule"
    lines.extend([
        r"\end{tabular}",
        r"\end{table*}",
    ])

    OUTPUT_LATEX.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_LATEX.write_text("\n".join(lines))
    print(f"LaTeX table saved: {OUTPUT_LATEX}")


def print_summary(rows: list[dict[str, Any]]) -> None:
    models = sorted({r["model"] for r in rows})
    for model in models:
        auto_rows = [r for r in rows if r["model"] == model and r["config"] == "auto"]
        fixed_rows = [r for r in rows if r["model"] == model and r["config"] == "fixed5"]
        if auto_rows:
            avg_dfs = mean([r["dfs_mean"] for r in auto_rows])
            avg_agents = mean([r["n_agents_mean"] for r in auto_rows])
            print(f"{model} Phase0-Auto: avg DFS={avg_dfs:.3f}, avg |AG*|={avg_agents:.1f}")
        if fixed_rows:
            avg_dfs = mean([r["dfs_mean"] for r in fixed_rows])
            print(f"{model} Fixed-5:     avg DFS={avg_dfs:.3f}")


def main() -> None:
    gt_map = load_ground_truth()
    rows = collect_results(gt_map)
    if not rows:
        print("No results found. Run experiments/run_cross_model.sh first.")
        return
    write_csv(rows)
    generate_latex_table(rows)
    print_summary(rows)


if __name__ == "__main__":
    main()

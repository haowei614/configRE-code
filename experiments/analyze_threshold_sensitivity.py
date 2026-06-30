#!/usr/bin/env python3
"""Analyze threshold sensitivity results and generate LaTeX table + plot."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from statistics import mean, pstdev
from typing import Any

import matplotlib.pyplot as plt
import numpy as np

SENSITIVITY_DIR = Path("experiments/results/threshold_sensitivity")
GROUND_TRUTH_FILE = Path("experiments/ground_truth/domain_relevance.json")
OUTPUT_CSV = Path("experiments/results/threshold_sensitivity_summary.csv")
OUTPUT_PLOT = Path("experiments/results/threshold_sensitivity_plot.pdf")
OUTPUT_LATEX = Path("experiments/results/threshold_sensitivity_table.tex")

THRESHOLDS = [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
CASES = ["AD", "ATM", "Library", "RollCall", "Bookkeeping"]


def load_ground_truth() -> dict[str, set[str]]:
    data = json.loads(GROUND_TRUTH_FILE.read_text())
    return {
        case_id: set(case_data["relevant_agents"])
        for case_id, case_data in data.items()
    }


def compute_metrics(activated: list[str], gt: set[str]) -> dict[str, float]:
    activated_set = set(activated)
    relevant = activated_set & gt
    precision = len(relevant) / len(activated_set) if activated_set else 0.0
    recall = len(relevant) / len(gt) if gt else 0.0
    dfs = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0
    return {"asp": precision, "asr": recall, "dfs": dfs, "n_agents": len(activated_set)}


def collect_results(gt_map: dict[str, set[str]]) -> list[dict[str, Any]]:
    rows = []
    for threshold in THRESHOLDS:
        tau_label = f"tau_{str(threshold).replace('.', '_')}"
        tau_dir = SENSITIVITY_DIR / tau_label
        if not tau_dir.exists():
            continue
        for case_id in CASES:
            case_dir = tau_dir / case_id
            if not case_dir.exists():
                continue
            seed_metrics: list[dict[str, float]] = []
            for seed_dir in sorted(case_dir.glob("seed_*")):
                phase0_file = seed_dir / "phase0_agent_selection.json"
                if not phase0_file.exists():
                    continue
                phase0 = json.loads(phase0_file.read_text())
                activated = phase0.get("selected_agents", [])
                metrics = compute_metrics(activated, gt_map.get(case_id, set()))

                phase2_file = seed_dir / "phase2_negotiation_trace.json"
                cnr = compute_cnr(phase2_file, gt_map.get(case_id, set()))
                metrics["cnr"] = cnr

                phase1_file = seed_dir / "phase1_initial_models.json"
                phase3_file = seed_dir / "phase3_integrated_kaos_model.json"
                run_record_file = seed_dir / "run_record.json"
                tokens = extract_total_tokens(run_record_file)
                metrics["total_tokens"] = tokens
                seed_metrics.append(metrics)

            if seed_metrics:
                row: dict[str, Any] = {
                    "threshold": threshold,
                    "case_id": case_id,
                    "runs": len(seed_metrics),
                }
                for metric_name in ["asp", "asr", "dfs", "n_agents", "cnr", "total_tokens"]:
                    values = [m[metric_name] for m in seed_metrics if m[metric_name] is not None]
                    if values:
                        row[f"{metric_name}_mean"] = mean(values)
                        row[f"{metric_name}_std"] = pstdev(values)
                    else:
                        row[f"{metric_name}_mean"] = None
                        row[f"{metric_name}_std"] = None
                rows.append(row)
    return rows


def compute_cnr(phase2_file: Path, gt: set[str]) -> float | None:
    if not phase2_file.exists():
        return None
    phase2 = json.loads(phase2_file.read_text())
    negotiations = phase2.get("negotiations", {})
    if not isinstance(negotiations, dict):
        return None
    detected = 0
    noisy = 0
    for neg in negotiations.values():
        if not isinstance(neg, dict):
            continue
        steps = neg.get("steps", [])
        if not isinstance(steps, list):
            continue
        conflict_steps = [s for s in steps if isinstance(s, dict) and s.get("conflict_detected")]
        if not conflict_steps:
            continue
        detected += 1
        involved = set()
        for key in ("focus_agent",):
            a = str(neg.get(key, "")).strip()
            if a:
                involved.add(a)
        for s in conflict_steps:
            for key in ("focus_agent", "reviewer_agent"):
                a = str(s.get(key, "")).strip()
                if a:
                    involved.add(a)
        if any(a not in gt for a in involved):
            noisy += 1
    if detected == 0:
        return 0.0
    return noisy / detected


def extract_total_tokens(run_record_file: Path) -> float | None:
    if not run_record_file.exists():
        return None
    data = json.loads(run_record_file.read_text())
    usage = data.get("token_usage", {})
    if isinstance(usage, dict):
        total = usage.get("total", {})
        if isinstance(total, dict):
            return total.get("total_tokens")
    return None


def write_csv(rows: list[dict[str, Any]]) -> None:
    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    columns = ["threshold", "case_id", "runs"]
    for m in ["asp", "asr", "dfs", "n_agents", "cnr", "total_tokens"]:
        columns.extend([f"{m}_mean", f"{m}_std"])
    with OUTPUT_CSV.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        for row in rows:
            writer.writerow({c: row.get(c, "N/A") for c in columns})


def generate_plot(rows: list[dict[str, Any]]) -> None:
    fig, axes = plt.subplots(1, 3, figsize=(14, 4.5))

    for case_id in CASES:
        case_rows = [r for r in rows if r["case_id"] == case_id]
        if not case_rows:
            continue
        thresholds = [r["threshold"] for r in case_rows]
        dfs_vals = [r.get("dfs_mean", 0) or 0 for r in case_rows]
        cnr_vals = [r.get("cnr_mean", 0) or 0 for r in case_rows]
        n_agents_vals = [r.get("n_agents_mean", 0) or 0 for r in case_rows]

        axes[0].plot(thresholds, dfs_vals, "o-", label=case_id, markersize=5)
        axes[1].plot(thresholds, cnr_vals, "s-", label=case_id, markersize=5)
        axes[2].plot(thresholds, n_agents_vals, "^-", label=case_id, markersize=5)

    avg_rows: dict[float, dict[str, list[float]]] = {}
    for r in rows:
        t = r["threshold"]
        if t not in avg_rows:
            avg_rows[t] = {"dfs": [], "cnr": [], "n_agents": []}
        if r.get("dfs_mean") is not None:
            avg_rows[t]["dfs"].append(r["dfs_mean"])
        if r.get("cnr_mean") is not None:
            avg_rows[t]["cnr"].append(r["cnr_mean"])
        if r.get("n_agents_mean") is not None:
            avg_rows[t]["n_agents"].append(r["n_agents_mean"])

    avg_thresholds = sorted(avg_rows.keys())
    avg_dfs = [mean(avg_rows[t]["dfs"]) if avg_rows[t]["dfs"] else 0 for t in avg_thresholds]
    avg_cnr = [mean(avg_rows[t]["cnr"]) if avg_rows[t]["cnr"] else 0 for t in avg_thresholds]
    avg_n = [mean(avg_rows[t]["n_agents"]) if avg_rows[t]["n_agents"] else 0 for t in avg_thresholds]

    axes[0].plot(avg_thresholds, avg_dfs, "k--", linewidth=2, label="Average", markersize=0)
    axes[1].plot(avg_thresholds, avg_cnr, "k--", linewidth=2, label="Average", markersize=0)
    axes[2].plot(avg_thresholds, avg_n, "k--", linewidth=2, label="Average", markersize=0)

    axes[0].set_xlabel(r"Threshold $\tau_1$")
    axes[0].set_ylabel("Domain Fit Score (DFS)")
    axes[0].set_title("(a) DFS vs. Threshold")
    axes[0].set_ylim(-0.05, 1.05)
    axes[0].legend(fontsize=7, ncol=2)
    axes[0].grid(True, alpha=0.3)

    axes[1].set_xlabel(r"Threshold $\tau_1$")
    axes[1].set_ylabel("Conflict Noise Rate (CNR)")
    axes[1].set_title("(b) CNR vs. Threshold")
    axes[1].set_ylim(-0.05, 1.05)
    axes[1].legend(fontsize=7, ncol=2)
    axes[1].grid(True, alpha=0.3)

    axes[2].set_xlabel(r"Threshold $\tau_1$")
    axes[2].set_ylabel("Number of Agents $|AG^*|$")
    axes[2].set_title("(c) Agent Count vs. Threshold")
    axes[2].legend(fontsize=7, ncol=2)
    axes[2].grid(True, alpha=0.3)

    plt.tight_layout()
    OUTPUT_PLOT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT_PLOT, bbox_inches="tight", dpi=300)
    fig.savefig(OUTPUT_PLOT.with_suffix(".png"), bbox_inches="tight", dpi=300)
    plt.close(fig)
    print(f"Plot saved: {OUTPUT_PLOT}")


def generate_latex_table(rows: list[dict[str, Any]]) -> None:
    lines = [
        r"\begin{table*}[t]",
        r"\centering",
        r"\caption{Threshold Sensitivity Analysis: Effect of $\tau_1$ on Agent Selection and Negotiation Quality (averaged over 5 case studies $\times$ 3 seeds)}",
        r"\label{tab:threshold_sensitivity}",
        r"\begin{tabular}{l ccccc c}",
        r"\toprule",
        r"$\tau_1$ & $|AG^*|$ & ASP$\uparrow$ & ASR$\uparrow$ & DFS$\uparrow$ & CNR$\downarrow$ & Tokens (K) \\",
        r"\midrule",
    ]
    for threshold in THRESHOLDS:
        t_rows = [r for r in rows if r["threshold"] == threshold]
        if not t_rows:
            continue
        def avg_metric(metric: str) -> str:
            vals = [r.get(f"{metric}_mean") for r in t_rows if r.get(f"{metric}_mean") is not None]
            return f"{mean(vals):.2f}" if vals else "N/A"
        def avg_tokens() -> str:
            vals = [r.get("total_tokens_mean") for r in t_rows if r.get("total_tokens_mean") is not None]
            return f"{mean(vals)/1000:.0f}" if vals else "N/A"

        bold = r"\textbf" if threshold == 0.6 else ""
        tau_str = f"{bold}{{{threshold}}}" if bold else f"{threshold}"
        line = f"{tau_str} & {avg_metric('n_agents')} & {avg_metric('asp')} & {avg_metric('asr')} & {avg_metric('dfs')} & {avg_metric('cnr')} & {avg_tokens()} \\\\"
        lines.append(line)

    lines.extend([
        r"\bottomrule",
        r"\end{tabular}",
        r"\begin{minipage}{\textwidth}",
        r"\vspace{4pt}",
        r"\footnotesize",
        r"Bold row indicates the default threshold used in the main experiments. Results averaged over 3 seeds per case study.",
        r"\end{minipage}",
        r"\end{table*}",
    ])

    OUTPUT_LATEX.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_LATEX.write_text("\n".join(lines))
    print(f"LaTeX table saved: {OUTPUT_LATEX}")


def main() -> None:
    gt_map = load_ground_truth()
    rows = collect_results(gt_map)
    if not rows:
        print("No results found. Run experiments/run_threshold_sensitivity.sh first.")
        return
    write_csv(rows)
    print(f"CSV saved: {OUTPUT_CSV} ({len(rows)} rows)")
    generate_plot(rows)
    generate_latex_table(rows)


if __name__ == "__main__":
    main()

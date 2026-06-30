#!/usr/bin/env python3
"""Analyze human evaluation results and generate LaTeX table.

Expected input: experiments/results/human_evaluation_scores.csv
CSV format: evaluator_id,case_id,config,D1_completeness,D2_relevance,D3_actionability,D4_consistency
"""

from __future__ import annotations

import csv
from pathlib import Path
from statistics import mean, pstdev
from typing import Any

INPUT_CSV = Path("experiments/results/human_evaluation_scores.csv")
OUTPUT_LATEX = Path("experiments/results/human_evaluation_table.tex")

DIMENSIONS = ["D1_completeness", "D2_relevance", "D3_actionability", "D4_consistency"]
DIM_LABELS = {
    "D1_completeness": "Completeness",
    "D2_relevance": "Relevance",
    "D3_actionability": "Actionability",
    "D4_consistency": "Consistency",
}
CONFIGS = ["Fixed-5", "Full-15", "Domain-opt", "Phase0-Auto"]


def load_scores() -> list[dict[str, Any]]:
    rows = []
    with INPUT_CSV.open() as f:
        reader = csv.DictReader(f)
        for row in reader:
            parsed = {
                "evaluator_id": row["evaluator_id"],
                "case_id": row["case_id"],
                "config": row["config"],
            }
            for dim in DIMENSIONS:
                parsed[dim] = int(row[dim])
            rows.append(parsed)
    return rows


def compute_krippendorff_alpha(rows: list[dict[str, Any]]) -> float | None:
    """Nominal Krippendorff's alpha (simplified ordinal approximation)."""
    try:
        import numpy as np
    except ImportError:
        return None

    evaluators = sorted({r["evaluator_id"] for r in rows})
    items = sorted({(r["case_id"], r["config"], d) for r in rows for d in DIMENSIONS})

    if len(evaluators) < 2:
        return None

    matrix = np.full((len(evaluators), len(items)), np.nan)
    item_idx = {item: i for i, item in enumerate(items)}

    for r in rows:
        e_idx = evaluators.index(r["evaluator_id"])
        for dim in DIMENSIONS:
            key = (r["case_id"], r["config"], dim)
            if key in item_idx:
                matrix[e_idx, item_idx[key]] = r[dim]

    pairs_observed = 0
    disagreement_observed = 0.0
    for j in range(matrix.shape[1]):
        vals = matrix[:, j][~np.isnan(matrix[:, j])]
        n = len(vals)
        if n < 2:
            continue
        for a in range(n):
            for b in range(a + 1, n):
                pairs_observed += 1
                disagreement_observed += (vals[a] - vals[b]) ** 2

    if pairs_observed == 0:
        return None
    D_o = disagreement_observed / pairs_observed

    all_vals = matrix[~np.isnan(matrix)]
    n_total = len(all_vals)
    disagreement_expected = 0.0
    count = 0
    for a in range(n_total):
        for b in range(a + 1, n_total):
            disagreement_expected += (all_vals[a] - all_vals[b]) ** 2
            count += 1
    if count == 0:
        return None
    D_e = disagreement_expected / count

    if D_e == 0:
        return 1.0
    return 1.0 - D_o / D_e


def generate_latex(rows: list[dict[str, Any]], alpha: float | None) -> None:
    lines = [
        r"\begin{table}[t]",
        r"\centering",
        r"\caption{Human Evaluation of Downstream Requirements Quality (Likert 1--5, higher is better)}",
        r"\label{tab:human_eval}",
        r"\begin{tabular}{l cccc c}",
        r"\toprule",
        r"\textbf{Config} & \textbf{Compl.} & \textbf{Relev.} & \textbf{Action.} & \textbf{Consist.} & \textbf{Avg} \\",
        r"\midrule",
    ]

    for config in CONFIGS:
        config_rows = [r for r in rows if r["config"] == config]
        if not config_rows:
            continue
        dim_means = []
        cells = []
        for dim in DIMENSIONS:
            vals = [r[dim] for r in config_rows]
            m = mean(vals)
            s = pstdev(vals) if len(vals) > 1 else 0.0
            cells.append(f"{m:.2f}")
            dim_means.append(m)
        avg = mean(dim_means)
        line = f"{config} & {' & '.join(cells)} & \\textbf{{{avg:.2f}}} \\\\"
        lines.append(line)

    alpha_str = f"{alpha:.3f}" if alpha is not None else "N/A"
    lines.extend([
        r"\bottomrule",
        r"\end{tabular}",
        r"\begin{minipage}{\columnwidth}",
        r"\vspace{4pt}",
        r"\footnotesize",
        f"Krippendorff's $\\alpha$ = {alpha_str}. Scores averaged across evaluators and case studies.",
        r"\end{minipage}",
        r"\end{table}",
    ])

    OUTPUT_LATEX.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_LATEX.write_text("\n".join(lines))
    print(f"LaTeX table saved: {OUTPUT_LATEX}")


def main() -> None:
    if not INPUT_CSV.exists():
        print(f"Input file not found: {INPUT_CSV}")
        print("Create this CSV with columns: evaluator_id,case_id,config,D1_completeness,D2_relevance,D3_actionability,D4_consistency")
        return
    rows = load_scores()
    print(f"Loaded {len(rows)} evaluation records")
    alpha = compute_krippendorff_alpha(rows)
    print(f"Krippendorff's alpha: {alpha:.3f}" if alpha else "Krippendorff's alpha: N/A")

    for config in CONFIGS:
        config_rows = [r for r in rows if r["config"] == config]
        if config_rows:
            avg = mean([mean([r[d] for d in DIMENSIONS]) for r in config_rows])
            print(f"  {config}: avg={avg:.2f} (n={len(config_rows)})")

    generate_latex(rows, alpha)


if __name__ == "__main__":
    main()

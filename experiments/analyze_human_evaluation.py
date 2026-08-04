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
OUTPUT_SUMMARY = Path("experiments/results/human_evaluation_summary.txt")

DIMENSIONS = ["D1_completeness", "D2_relevance", "D3_actionability", "D4_consistency"]
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
    """Ordinal Krippendorff's alpha with squared-difference metric."""
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


def config_means_by_evaluator(rows: list[dict[str, Any]]) -> dict[str, dict[str, float]]:
    """evaluator -> config -> overall mean (across cases and dimensions)."""
    out: dict[str, dict[str, float]] = {}
    evaluators = sorted({r["evaluator_id"] for r in rows})
    for e in evaluators:
        out[e] = {}
        for c in CONFIGS:
            cr = [r for r in rows if r["evaluator_id"] == e and r["config"] == c]
            if not cr:
                continue
            out[e][c] = mean(mean(r[d] for d in DIMENSIONS) for r in cr)
    return out


def kendalls_w_config_ranking(rows: list[dict[str, Any]]) -> float | None:
    """Kendall's W over configuration rankings across evaluators."""
    try:
        import numpy as np
        from scipy.stats import rankdata
    except ImportError:
        return None

    by_e = config_means_by_evaluator(rows)
    evaluators = sorted(by_e)
    if len(evaluators) < 2:
        return None
    M = np.array([[by_e[e][c] for c in CONFIGS] for e in evaluators])
    R = np.array([rankdata(-row) for row in M])  # higher score → better (rank 1)
    k, n = R.shape
    R_sum = R.sum(axis=0)
    S = ((R_sum - R_sum.mean()) ** 2).sum()
    return float(12 * S / (k**2 * (n**3 - n)))


def friedman_p(rows: list[dict[str, Any]]) -> tuple[float, float] | None:
    """Friedman test on per-case overall means across the four configs."""
    try:
        from scipy.stats import friedmanchisquare
    except ImportError:
        return None

    cases = sorted({r["case_id"] for r in rows})
    scores: dict[tuple[str, str], float] = {}
    for case in cases:
        for cfg in CONFIGS:
            vals = [
                mean(r[d] for d in DIMENSIONS)
                for r in rows
                if r["case_id"] == case and r["config"] == cfg
            ]
            if vals:
                scores[(case, cfg)] = mean(vals)
    if len(cases) < 3:
        return None
    data = [[scores[(case, cfg)] for case in cases] for cfg in CONFIGS]
    stat, p = friedmanchisquare(*data)
    return float(stat), float(p)


def generate_latex(
    rows: list[dict[str, Any]],
    alpha: float | None,
    kendall_w: float | None,
    friedman: tuple[float, float] | None,
) -> None:
    lines = [
        r"\begin{table}[t]",
        r"\centering",
        r"\caption{Human Evaluation of Phase~5 Requirement Specifications (mean Likert 1--5, averaged over 4 case studies and 3 evaluators).}",
        r"\label{tab:humaneval}",
        r"\begin{tabular}{l ccccc}",
        r"\toprule",
        r"\textbf{Config} & \textbf{Compl.} & \textbf{Relev.} & \textbf{Action.} & \textbf{Consist.} & \textbf{Avg} \\",
        r"\midrule",
    ]

    best_avg = -1.0
    config_avgs: dict[str, float] = {}
    for config in CONFIGS:
        config_rows = [r for r in rows if r["config"] == config]
        if not config_rows:
            continue
        dim_means = [mean(r[dim] for r in config_rows) for dim in DIMENSIONS]
        config_avgs[config] = mean(dim_means)
        best_avg = max(best_avg, config_avgs[config])

    for config in CONFIGS:
        config_rows = [r for r in rows if r["config"] == config]
        if not config_rows:
            continue
        cells = []
        dim_means = []
        for dim in DIMENSIONS:
            vals = [r[dim] for r in config_rows]
            m = mean(vals)
            cells.append(f"{m:.2f}")
            dim_means.append(m)
        avg = mean(dim_means)
        avg_cell = f"\\textbf{{{avg:.2f}}}" if abs(avg - best_avg) < 1e-9 else f"{avg:.2f}"
        lines.append(f"{config} & {' & '.join(cells)} & {avg_cell} \\\\")

    alpha_str = f"{alpha:.3f}" if alpha is not None else "N/A"
    w_str = f"{kendall_w:.3f}" if kendall_w is not None else "N/A"
    if friedman is not None:
        fri_str = f"Friedman $\\chi^2={friedman[0]:.2f}$, $p={friedman[1]:.3f}$"
    else:
        fri_str = "Friedman N/A"

    lines.extend([
        r"\bottomrule",
        r"\end{tabular}",
        r"\begin{minipage}{\columnwidth}",
        r"\vspace{4pt}",
        r"\footnotesize",
        f"Compl.: Completeness; Relev.: Relevance; Action.: Actionability; Consist.: Consistency. "
        f"Krippendorff's~$\\alpha$ (ordinal) = {alpha_str}; Kendall's~$W$ on configuration rankings = {w_str}. "
        f"{fri_str}.",
        r"\end{minipage}",
        r"\end{table}",
    ])

    OUTPUT_LATEX.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_LATEX.write_text("\n".join(lines) + "\n")
    print(f"LaTeX table saved: {OUTPUT_LATEX}")


def write_summary(
    rows: list[dict[str, Any]],
    alpha: float | None,
    kendall_w: float | None,
    friedman: tuple[float, float] | None,
) -> None:
    lines = [
        f"n_records={len(rows)}",
        f"n_evaluators={len({r['evaluator_id'] for r in rows})}",
        f"n_cases={len({r['case_id'] for r in rows})}",
        f"krippendorff_alpha={alpha}",
        f"kendalls_W={kendall_w}",
        f"friedman={friedman}",
        "",
        "Per-evaluator configuration ranking (overall mean):",
    ]
    by_e = config_means_by_evaluator(rows)
    for e, avgs in by_e.items():
        ordered = sorted(avgs, key=avgs.get, reverse=True)
        lines.append(f"  {e}: " + ", ".join(f"{c}={avgs[c]:.2f}" for c in ordered))
    lines.append("")
    for config in CONFIGS:
        config_rows = [r for r in rows if r["config"] == config]
        if not config_rows:
            continue
        dim_m = {dim: mean(r[dim] for r in config_rows) for dim in DIMENSIONS}
        avg = mean(dim_m.values())
        lines.append(
            f"{config}: Compl={dim_m['D1_completeness']:.2f} "
            f"Relev={dim_m['D2_relevance']:.2f} "
            f"Action={dim_m['D3_actionability']:.2f} "
            f"Consist={dim_m['D4_consistency']:.2f} "
            f"Avg={avg:.2f} (n={len(config_rows)})"
        )
    OUTPUT_SUMMARY.write_text("\n".join(lines) + "\n")
    print(f"Summary saved: {OUTPUT_SUMMARY}")


def main() -> None:
    if not INPUT_CSV.exists():
        print(f"Input file not found: {INPUT_CSV}")
        print(
            "Create this CSV with columns: evaluator_id,case_id,config,"
            "D1_completeness,D2_relevance,D3_actionability,D4_consistency"
        )
        return
    rows = load_scores()
    print(f"Loaded {len(rows)} evaluation records")
    alpha = compute_krippendorff_alpha(rows)
    kendall_w = kendalls_w_config_ranking(rows)
    friedman = friedman_p(rows)
    print(f"Krippendorff's alpha: {alpha:.3f}" if alpha is not None else "Krippendorff's alpha: N/A")
    print(f"Kendall's W: {kendall_w:.3f}" if kendall_w is not None else "Kendall's W: N/A")
    if friedman is not None:
        print(f"Friedman: chi2={friedman[0]:.3f} p={friedman[1]:.4f}")

    for config in CONFIGS:
        config_rows = [r for r in rows if r["config"] == config]
        if config_rows:
            avg = mean(mean(r[d] for d in DIMENSIONS) for r in config_rows)
            print(f"  {config}: avg={avg:.2f} (n={len(config_rows)})")

    generate_latex(rows, alpha, kendall_w, friedman)
    write_summary(rows, alpha, kendall_w, friedman)


if __name__ == "__main__":
    main()

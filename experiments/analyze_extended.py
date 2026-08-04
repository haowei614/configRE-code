#!/usr/bin/env python3
"""Aggregate extended (per-case/config/seed) experiment artifacts into a summary.

Directory layout expected:
    experiments/results/extended/<CASE>/<config_x>/seed_<n>/<phase files>

Reuses metric extraction from compare_results.py.
"""

from __future__ import annotations

import csv
from pathlib import Path
from statistics import mean, pstdev

import compare_results as cr

EXTENDED_DIR = Path("experiments/results/extended")
OUT_CSV = Path("experiments/results/extended_summary.csv")

CONFIG_NAMES = {
    "config_a": "Fixed-5",
    "config_b": "Domain-opt",
    "config_c": "Full-15",
    "config_d": "Phase0-Auto",
}

METRICS = ["n_agents", "asp", "asr", "dfs", "conflict_noise_rate", "bertscore", "total_tokens"]


def main() -> None:
    rows = []
    for case_dir in sorted(EXTENDED_DIR.iterdir()):
        if not case_dir.is_dir():
            continue
        case_id = case_dir.name
        for config_id, config_name in CONFIG_NAMES.items():
            config_dir = case_dir / config_id
            if not config_dir.is_dir():
                continue
            seed_metrics: dict[str, list[float]] = {m: [] for m in METRICS}
            n_seeds = 0
            for seed_dir in sorted(config_dir.glob("seed_*")):
                if not seed_dir.is_dir():
                    continue
                n_seeds += 1
                metrics = cr.extract_metrics(seed_dir)
                for m in METRICS:
                    v = cr.to_float(metrics.get(m))
                    if v is not None:
                        seed_metrics[m].append(v)
            row = {"case_id": case_id, "config_id": config_id, "config_name": config_name, "runs": n_seeds}
            for m in METRICS:
                vals = seed_metrics[m]
                row[f"{m}_mean"] = round(mean(vals), 4) if vals else ""
                row[f"{m}_std"] = round(pstdev(vals), 4) if vals else ""
            rows.append(row)

    cols = ["case_id", "config_id", "config_name", "runs"]
    for m in METRICS:
        cols += [f"{m}_mean", f"{m}_std"]
    with OUT_CSV.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow(r)

    # Pretty print
    for r in rows:
        print(
            f"{r['case_id']:<12} {r['config_name']:<12} "
            f"agents={r['n_agents_mean']!s:<5} DFS={r['dfs_mean']!s:<7} "
            f"CNR={r['conflict_noise_rate_mean']!s:<7} tok={r['total_tokens_mean']!s:<9}"
        )
    print(f"\nWrote {OUT_CSV}")


if __name__ == "__main__":
    main()

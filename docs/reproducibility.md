# Reproducibility Guide

This guide describes how to reproduce the ConfigRE experiment summaries used by the paper tables.

## Environment

Install dependencies with `uv`:

```bash
uv sync --all-groups
```

Run local validation:

```bash
uv run ruff check .
uv run pytest
```

LLM-backed experiment runs require an OpenAI-compatible API key through `OPENAI_API_KEY`, `.env`, or `.api_key`.

## Running The ConfigRE Matrix

Run all ConfigRE configurations across the five case studies and three seeds:

```bash
bash experiments/run_config_comparison.sh
```

The script evaluates:

- `Fixed-5`: the original five-agent baseline.
- `Domain-optimized-6`: six domain-selected agents.
- `Full-15`: the full extended agent pool.
- `Phase0-Auto`: dynamic Phase 0 agent selection.

Generated per-run phase artifacts are written under `experiments/results/`, but only final summary CSV files are tracked in git.

## Regenerating Aggregated Metrics

Aggregate run artifacts into the working summary:

```bash
python experiments/compare_results.py
```

This regenerates:

- `experiments/results/comparison_summary.csv`

This file is intentionally treated as a working, reproducible aggregation output. Running the aggregation script may overwrite it.

## Paper-Final Results

The paper-final frozen summary is stored separately:

- `experiments/results/comparison_summary_paper_final.csv`

Use this file when checking the final values reported in the paper tables. It preserves the submitted table values and is not overwritten by `experiments/compare_results.py`.

## Table Mapping

Table V, agent selection metrics:

- `ASP` -> `asp_mean`
- `ASR` -> `asr_mean`
- `DFS` -> `dfs_mean`

Table IV, cross-domain comparison metrics:

- `Agents` -> `n_agents_mean`
- `DFS` -> `dfs_mean`
- `Noise` -> `conflict_noise_rate_mean`
- `BERTScore` -> `bertscore_mean`
- `Tokens (K)` -> `total_tokens_mean / 1000`

## Ground Truth

Domain relevance labels for ASP, ASR, DFS, and conflict-noise analysis are stored in:

- `experiments/ground_truth/domain_relevance.json`

These labels should be treated as part of the evaluation protocol.

## Legacy Baselines

Compact historical QUARE, MARE, and iReDev summaries are retained under:

- `legacy_results/`

Per-run legacy phase artifacts are intentionally excluded from the public repository to keep the artifact compact.

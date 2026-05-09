# ConfigRE Experiments

This directory contains the scripts, labels, and final summaries used for the ConfigRE paper experiments.

## Contents

- `run_config_comparison.sh` runs the cross-domain ConfigRE matrix.
- `compare_results.py` aggregates per-run artifacts into summary metrics.
- `ground_truth/domain_relevance.json` stores domain relevance labels for agent-selection evaluation.
- `independent_annotation_protocol.md` stores the independent annotation protocol, completed second annotation, and agreement summary for the domain-relevance labels.
- `results/comparison_summary.csv` is the regenerated working summary.
- `results/comparison_summary_paper_final.csv` is the frozen paper-final summary.

## Running Experiments

From the repository root:

```bash
bash experiments/run_config_comparison.sh
python experiments/compare_results.py
```

The run script requires OpenAI-compatible credentials and writes per-run phase artifacts below `experiments/results/`.

## Tracked vs Ignored Artifacts

Tracked:

- Experiment scripts.
- Ground-truth relevance labels.
- Independent annotation evidence.
- Final summary CSV files.

Ignored:

- Per-seed phase artifacts.
- Run records.
- Smoke-test outputs.
- Local caches.

This keeps the repository focused on source code, protocol files, and compact final results while allowing full reruns locally.

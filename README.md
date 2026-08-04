# ConfigRE — Does Agent Configuration Matter?

[![CI](https://github.com/haowei614/configRE-code/actions/workflows/ci.yml/badge.svg)](https://github.com/haowei614/configRE-code/actions/workflows/ci.yml)

Replication package for the paper:

> **Does Agent Configuration Matter? An Empirical Study of Process-Level Quality Adaptation in Multi-Agent Requirements Engineering**
>
> Haowei Cheng, Milhan Kim, Bowen Jiang, Weixing Zhang, Yuhong Fu, Truong Vinh Truong Duy, Phan Thi Huyen Thanh, Foutse Khomh, Nobukazu Yoshioka, Naoyasu Ubayashi, Hironori Washizaki

ConfigRE extends the [OpenRE-Bench / QUARE](https://github.com/QUARE-benchmark) pipeline with a **Phase 0 (Domain-Adaptive Agent Configuration)** step that selects domain-relevant quality agents before requirements negotiation begins. The selection uses a three-tier mechanism: LLM relevance scoring (Tier 1), deterministic domain-regulatory mapping (Tier 2), and project-level constraint extraction (Tier 3).

---

## Repository Structure

```
configRE-code/
│
├── src/openre_bench/            # Core implementation
│   ├── cli.py                   #   CLI entry point (configre / openre_bench)
│   ├── llm.py / llm_client.py   #   LLM inference (litellm-based)
│   ├── schemas.py               #   Pydantic data schemas
│   ├── settings.py              #   Configuration & environment
│   ├── pipeline/                #   Phase 0–5 pipeline logic
│   ├── comparison_harness.py    #   Multi-config comparison runner
│   ├── comparison_validator.py  #   ASP / ASR / DFS / CNR metric computation
│   └── auto_report.py           #   Automated result reporting
│
├── data/
│   ├── case_studies/            # Input descriptions for all 9 case studies
│   │   ├── AD_input.json        #   Autonomous Driving (primary)
│   │   ├── ATM_input.json       #   ATM System (primary)
│   │   ├── Library_input.json   #   Library System (primary)
│   │   ├── RollCall_input.json  #   RollCall System (primary)
│   │   ├── Bookkeeping_input.json  # Bookkeeping System (primary)
│   │   ├── EHR_input.json       #   Electronic Health Records (external)
│   │   ├── SmartGrid_input.json #   Smart Grid (external)
│   │   ├── LoanApproval_input.json # Loan Approval (external)
│   │   └── W-Mobility_input.json   # W-Mobility / Aisin (industrial)
│   ├── ground_truth/            # Expert ground-truth labels
│   ├── knowledge_base/          # RAG corpus for domain knowledge
│   └── vector_store/            # Chroma vector store
│
├── experiments/
│   ├── ground_truth/
│   │   └── domain_relevance.json    # Per-case expert agent labels + rationale
│   │
│   ├── results/                     # Reproducible experiment outputs
│   │   ├── comparison_summary.csv              # Main 5-case results (Table 2)
│   │   ├── comparison_summary_paper_final.csv  # Frozen paper-final values
│   │   ├── extended_summary.csv                # 3 external cases (EHR, SmartGrid, Loan)
│   │   ├── threshold_sensitivity_summary.csv   # τ₁ sensitivity (Figure 3)
│   │   ├── cross_model_summary.csv             # Cross-model Phase 0 (Section 4.4)
│   │   ├── human_evaluation_scores.csv         # Blinded human evaluation (Table 4)
│   │   ├── human_evaluation_summary.txt        # Aggregated α / W statistics
│   │   ├── human_evaluation_table.tex          # LaTeX table
│   │   ├── phase0_cross_model/                 # Per-model Phase 0 selection results
│   │   │   ├── claude-sonnet-4-5-20250929/
│   │   │   ├── gemma2_9b/
│   │   │   ├── llama3.1_8b/
│   │   │   └── qwen2.5_7b/
│   │   └── *.pdf / *.png / *.tex               # Figures and LaTeX tables
│   │
│   ├── compare_results.py           # Aggregate main comparison results
│   ├── analyze_extended.py          # Aggregate external-case results
│   ├── analyze_human_evaluation.py  # Human evaluation analysis (α, W, Friedman)
│   ├── analyze_cross_model.py       # Cross-model summary
│   ├── analyze_threshold_sensitivity.py  # τ₁ sweep analysis
│   ├── plot_dfs_token_cnr_scatter.py     # Figure 2 scatter plot
│   ├── human_evaluation_rubric.json      # 4-dimension Likert rubric
│   ├── independent_annotation_protocol.md
│   └── run_*.sh / run_*.py              # Experiment runner scripts
│
├── run_matrix.py                # Run full 5-case × 4-config matrix
├── run_w_mobility_matrix.py     # Run W-Mobility (industrial) matrix
├── significance_test.py         # Wilcoxon signed-rank tests
│
├── tests/                       # Regression tests
├── docs/                        # Technical notes & reproducibility guide
├── scripts/                     # Utility scripts (e.g. path anonymization)
│
├── pyproject.toml               # Project metadata & dependencies
├── LICENSE                      # AGPL-3.0
└── CITATION.cff
```

## Paper ↔ Artifact Mapping

| Paper Section | Artifact |
|---|---|
| Table 2 (Main results) | `experiments/results/comparison_summary_paper_final.csv` |
| Table 3 (Industrial W-Mobility) | `run_w_mobility_matrix.py` → `experiment_outputs/w-mobility/` |
| Table 4 (Human evaluation) | `experiments/results/human_evaluation_scores.csv` |
| Figure 1 (Overview) | See [ConfigRE-paper](https://github.com/haowei614/ConfigRE-paper) |
| Figure 2 (DFS–Token–CNR scatter) | `experiments/results/dfs_token_cnr_scatter.pdf` |
| Figure 3 (Threshold sensitivity) | `experiments/results/threshold_sensitivity_plot.pdf` |
| Section 4.4 (Cross-model) | `experiments/results/phase0_cross_model/` |
| Ground truth | `experiments/ground_truth/domain_relevance.json` |

## Installation

Requires Python ≥ 3.11 and [uv](https://docs.astral.sh/uv/).

```bash
git clone https://github.com/haowei614/configRE-code.git
cd configRE-code
uv sync --all-groups
```

Provide LLM credentials via one of:
- `OPENAI_API_KEY` environment variable
- `.api_key` file
- `.env` file (see `.env.example`)

## Quick Start

```bash
# Verify installation
uv run configre --version
uv run pytest

# Run a single case
uv run configre --run-case \
  --case-input data/case_studies/ATM_input.json \
  --artifacts-dir artifacts/atm-run \
  --run-record artifacts/atm-run/run_record.json \
  --system quare

# Run the full experiment matrix (5 primary cases × 4 configs × 3 seeds)
python run_matrix.py

# Aggregate results
python experiments/compare_results.py
```

### Key Pipeline Artifacts

Each run produces the following phase outputs:

| File | Description |
|---|---|
| `phase0_agent_selection.json` | Selected agents and relevance scores |
| `phase0_external_spec_rules.json` | Domain-regulatory mapping output |
| `phase1_initial_models.json` | Initial KAOS models per agent |
| `phase2_negotiation_trace.json` | Pairwise negotiation trace |
| `phase3_integrated_kaos_model.json` | Merged KAOS model |
| `phase4_verification_report.json` | Verification against input requirements |
| `phase5_software_materials.json` | Final software requirement specification |
| `run_record.json` | Reproducibility metadata (model, seed, tokens) |

## Reproducing Paper Results

### Main Comparison (Table 2)

```bash
bash experiments/run_config_comparison.sh
python experiments/compare_results.py
# Output: experiments/results/comparison_summary.csv
```

### External Cases (Table 2, right columns)

```bash
bash experiments/run_extended_evaluation.sh
python experiments/analyze_extended.py
# Output: experiments/results/extended_summary.csv
```

### Industrial Case — W-Mobility (Table 3)

```bash
python run_w_mobility_matrix.py
# Output: experiment_outputs/w-mobility/
```

### Threshold Sensitivity (Figure 3)

```bash
bash experiments/run_threshold_sensitivity.sh
python experiments/analyze_threshold_sensitivity.py
# Output: experiments/results/threshold_sensitivity_*.csv/.pdf
```

### Cross-Model Validation (Section 4.4)

```bash
python experiments/run_phase0_claude_cross_model.py
python experiments/run_phase0_ollama_cross_model.py
python experiments/analyze_cross_model.py
# Output: experiments/results/phase0_cross_model/
```

### Human Evaluation (Table 4)

```bash
python experiments/analyze_human_evaluation.py
# Input:  experiments/results/human_evaluation_scores.csv
# Output: human_evaluation_summary.txt, human_evaluation_table.tex
```

### Statistical Tests

```bash
python significance_test.py
# Output: significance_results.txt
```

## License

AGPL-3.0. See [LICENSE](LICENSE).

## Citation

```bibtex
@inproceedings{cheng2026configre,
  title     = {Does Agent Configuration Matter? An Empirical Study of
               Process-Level Quality Adaptation in Multi-Agent
               Requirements Engineering},
  author    = {Cheng, Haowei and Kim, Milhan and Jiang, Bowen and
               Zhang, Weixing and Fu, Yuhong and
               Truong Duy, Truong Vinh and
               Phan Thi, Huyen Thanh and Khomh, Foutse and
               Yoshioka, Nobukazu and Ubayashi, Naoyasu and
               Washizaki, Hironori},
  year      = {2026}
}
```

#!/usr/bin/env bash
# Threshold Sensitivity Analysis: τ₁ = 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9
set -e
set -a; source .env; set +a

SYSTEM="quare"
SETTING="negotiation_integration_verification"
ROUND_CAP=3
BASE_DIR="experiments/results/threshold_sensitivity"
RAG_ARGS="--rag-corpus-dir data/knowledge_base --rag-backend local_tfidf"

CASES="AD:data/case_studies/AD_input.json
ATM:data/case_studies/ATM_input.json
Library:data/case_studies/Library_input.json
RollCall:data/case_studies/RollCall_input.json
Bookkeeping:data/case_studies/Bookkeeping_input.json"

total=0
for threshold in 0.3 0.4 0.5 0.6 0.7 0.8 0.9; do
  tau_label=$(echo "$threshold" | tr '.' '_')
  echo "=== τ₁ = ${threshold} ==="
  echo "$CASES" | while IFS=: read -r case_id case_input; do
    for seed in 101 202 303; do
      dir="${BASE_DIR}/tau_${tau_label}/${case_id}/seed_${seed}"
      if [ -f "$dir/run_record.json" ]; then
        echo "  SKIP: τ=${threshold} ${case_id} seed=${seed}"
        continue
      fi
      mkdir -p "$dir"
      echo "  RUN: τ=${threshold} ${case_id} seed=${seed}"
      uv run configre --run-case \
        --case-input "$case_input" \
        --artifacts-dir "$dir" \
        --run-record "$dir/run_record.json" \
        --system "$SYSTEM" --setting "$SETTING" \
        --seed "$seed" --round-cap "$ROUND_CAP" \
        --agent-config auto \
        --tier1-threshold "$threshold" \
        $RAG_ARGS
    done
  done
done

echo "=== Threshold sensitivity complete ==="

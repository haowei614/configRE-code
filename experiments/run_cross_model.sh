#!/bin/bash
# Cross-Model Validation: Run Phase0-Auto with alternative LLM backbone.
# Default comparison model: gpt-4o (can override via $ALT_MODEL env var)
#
# Usage:
#   bash experiments/run_cross_model.sh                    # uses gpt-4o
#   ALT_MODEL=claude-3-5-sonnet-20241022 bash experiments/run_cross_model.sh
set -e

MODEL="${ALT_MODEL:-gpt-4o}"
MODEL_LABEL=$(echo "$MODEL" | tr '/:.' '_')
SYSTEM="quare"
SETTING="negotiation_integration_verification"
ROUND_CAP=3
BASE_DIR="experiments/results/cross_model/${MODEL_LABEL}"

CASES=(
  "AD:data/case_studies/AD_input.json"
  "ATM:data/case_studies/ATM_input.json"
  "Library:data/case_studies/Library_input.json"
  "RollCall:data/case_studies/RollCall_input.json"
  "Bookkeeping:data/case_studies/Bookkeeping_input.json"
  "EHR:data/case_studies/EHR_input.json"
  "SmartGrid:data/case_studies/SmartGrid_input.json"
  "LoanApproval:data/case_studies/LoanApproval_input.json"
)

SEEDS=(101 202 303)
CONFIGS=("fixed5" "auto")

total=$((${#CASES[@]} * ${#SEEDS[@]} * ${#CONFIGS[@]}))
current=0

echo "=== Cross-Model Validation: ${MODEL} ==="

for case_entry in "${CASES[@]}"; do
  case_id="${case_entry%%:*}"
  case_input="${case_entry##*:}"

  for config in "${CONFIGS[@]}"; do
    for seed in "${SEEDS[@]}"; do
      current=$((current + 1))
      dir="${BASE_DIR}/${case_id}/${config}/seed_${seed}"
      mkdir -p "$dir"
      echo "[${current}/${total}] ${MODEL} | ${case_id} | ${config} | seed=${seed}"

      agent_config_arg=""
      if [ "$config" = "auto" ]; then
        agent_config_arg="--agent-config auto"
      fi

      uv run configre --run-case \
        --case-input "$case_input" \
        --artifacts-dir "$dir" \
        --run-record "$dir/run_record.json" \
        --system "$SYSTEM" \
        --setting "$SETTING" \
        --seed "$seed" \
        --round-cap "$ROUND_CAP" \
        --model "$MODEL" \
        $agent_config_arg
    done
  done
done

echo "=== Cross-model runs complete (${MODEL}) ==="
echo "Run: python experiments/analyze_cross_model.py"

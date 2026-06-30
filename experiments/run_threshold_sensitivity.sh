#!/bin/bash
# Threshold Sensitivity Analysis: τ₁ = 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9
# Runs Phase0-Auto across all 5 case studies × 3 seeds for each threshold.
set -e

SYSTEM="quare"
SETTING="negotiation_integration_verification"
ROUND_CAP=3
BASE_DIR="experiments/results/threshold_sensitivity"

CASES=(
  "AD:data/case_studies/AD_input.json"
  "ATM:data/case_studies/ATM_input.json"
  "Library:data/case_studies/Library_input.json"
  "RollCall:data/case_studies/RollCall_input.json"
  "Bookkeeping:data/case_studies/Bookkeeping_input.json"
)

THRESHOLDS=(0.3 0.4 0.5 0.6 0.7 0.8 0.9)
SEEDS=(101 202 303)

total=$((${#CASES[@]} * ${#THRESHOLDS[@]} * ${#SEEDS[@]}))
current=0

for threshold in "${THRESHOLDS[@]}"; do
  tau_label=$(echo "$threshold" | tr '.' '_')
  for case_entry in "${CASES[@]}"; do
    case_id="${case_entry%%:*}"
    case_input="${case_entry##*:}"
    for seed in "${SEEDS[@]}"; do
      current=$((current + 1))
      dir="${BASE_DIR}/tau_${tau_label}/${case_id}/seed_${seed}"
      mkdir -p "$dir"
      echo "[${current}/${total}] τ₁=${threshold} | ${case_id} | seed=${seed}"
      uv run configre --run-case \
        --case-input "$case_input" \
        --artifacts-dir "$dir" \
        --run-record "$dir/run_record.json" \
        --system "$SYSTEM" \
        --setting "$SETTING" \
        --seed "$seed" \
        --round-cap "$ROUND_CAP" \
        --agent-config auto \
        --tier1-threshold "$threshold"
    done
  done
done

echo "=== Threshold sensitivity runs complete ==="
echo "Run: python experiments/analyze_threshold_sensitivity.py"

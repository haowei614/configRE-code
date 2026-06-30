#!/bin/bash
# Extended evaluation: run all 8 case studies (original 5 + 3 new) with all 4 configs.
# This produces the full result set for the revised paper.
set -e

SYSTEM="quare"
SETTING="negotiation_integration_verification"
ROUND_CAP=3
BASE_DIR="experiments/results/extended"

FULL_15='["SafetyAgent","EfficiencyAgent","GreenAgent","TrustworthinessAgent","ResponsibilityAgent","ReliabilityAgent","UsabilityAgent","SecurityAgent","MaintainabilityAgent","CompatibilityAgent","FlexibilityAgent","PerformanceAgent","FunctionalSafetyAgent","ExplainabilityAgent","PrivacyAgent"]'

declare -A DOMAIN_OPT
DOMAIN_OPT["AD"]='["SafetyAgent","EfficiencyAgent","ReliabilityAgent","FunctionalSafetyAgent","GreenAgent","ResponsibilityAgent"]'
DOMAIN_OPT["ATM"]='["SecurityAgent","TrustworthinessAgent","ReliabilityAgent","EfficiencyAgent","ResponsibilityAgent","PrivacyAgent"]'
DOMAIN_OPT["Library"]='["UsabilityAgent","ReliabilityAgent","MaintainabilityAgent","SecurityAgent","EfficiencyAgent","ResponsibilityAgent"]'
DOMAIN_OPT["RollCall"]='["UsabilityAgent","ReliabilityAgent","SecurityAgent","TrustworthinessAgent","PrivacyAgent","ResponsibilityAgent"]'
DOMAIN_OPT["Bookkeeping"]='["SecurityAgent","ReliabilityAgent","TrustworthinessAgent","ResponsibilityAgent","EfficiencyAgent","PrivacyAgent"]'
DOMAIN_OPT["EHR"]='["SecurityAgent","PrivacyAgent","ReliabilityAgent","UsabilityAgent","CompatibilityAgent","PerformanceAgent"]'
DOMAIN_OPT["SmartGrid"]='["SafetyAgent","PerformanceAgent","ReliabilityAgent","SecurityAgent","GreenAgent","EfficiencyAgent"]'
DOMAIN_OPT["LoanApproval"]='["ExplainabilityAgent","SecurityAgent","PrivacyAgent","ReliabilityAgent","ResponsibilityAgent","PerformanceAgent"]'

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

run_config() {
  local case_id="$1" case_input="$2" config_name="$3" agent_config="$4"
  for seed in "${SEEDS[@]}"; do
    dir="${BASE_DIR}/${case_id}/${config_name}/seed_${seed}"
    mkdir -p "$dir"
    echo "  [${config_name}] ${case_id} seed=${seed}"
    if [ "$agent_config" = "none" ]; then
      uv run configre --run-case \
        --case-input "$case_input" \
        --artifacts-dir "$dir" \
        --run-record "$dir/run_record.json" \
        --system "$SYSTEM" --setting "$SETTING" \
        --seed "$seed" --round-cap "$ROUND_CAP"
    elif [ "$agent_config" = "auto" ]; then
      uv run configre --run-case \
        --case-input "$case_input" \
        --artifacts-dir "$dir" \
        --run-record "$dir/run_record.json" \
        --system "$SYSTEM" --setting "$SETTING" \
        --seed "$seed" --round-cap "$ROUND_CAP" \
        --agent-config auto
    else
      uv run configre --run-case \
        --case-input "$case_input" \
        --artifacts-dir "$dir" \
        --run-record "$dir/run_record.json" \
        --system "$SYSTEM" --setting "$SETTING" \
        --seed "$seed" --round-cap "$ROUND_CAP" \
        --agent-config "$agent_config"
    fi
  done
}

for case_entry in "${CASES[@]}"; do
  case_id="${case_entry%%:*}"
  case_input="${case_entry##*:}"
  echo "=== ${case_id} ==="
  run_config "$case_id" "$case_input" "config_a" "none"
  run_config "$case_id" "$case_input" "config_b" "${DOMAIN_OPT[$case_id]}"
  run_config "$case_id" "$case_input" "config_c" "$FULL_15"
  run_config "$case_id" "$case_input" "config_d" "auto"
done

echo "=== Extended evaluation complete ==="
echo "Total runs: $((${#CASES[@]} * 4 * ${#SEEDS[@]}))"

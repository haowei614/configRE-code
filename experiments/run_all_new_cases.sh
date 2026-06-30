#!/usr/bin/env bash
# Run all 3 new case studies × 4 configs × 3 seeds = 36 runs
set -e
set -a; source .env; set +a

SYSTEM="quare"
SETTING="negotiation_integration_verification"
ROUND_CAP=3
BASE_DIR="experiments/results/extended"
RAG_ARGS="--rag-corpus-dir data/knowledge_base --rag-backend local_tfidf"
FULL_15='["SafetyAgent","EfficiencyAgent","GreenAgent","TrustworthinessAgent","ResponsibilityAgent","ReliabilityAgent","UsabilityAgent","SecurityAgent","MaintainabilityAgent","CompatibilityAgent","FlexibilityAgent","PerformanceAgent","FunctionalSafetyAgent","ExplainabilityAgent","PrivacyAgent"]'

run_one() {
  local case_id="$1" case_input="$2" config_name="$3" seed="$4"
  local agent_config="$5"
  local dir="${BASE_DIR}/${case_id}/${config_name}/seed_${seed}"
  if [ -f "$dir/run_record.json" ]; then
    echo "  SKIP: ${case_id}/${config_name}/seed_${seed}"
    return 0
  fi
  mkdir -p "$dir"
  echo "  RUN: ${case_id}/${config_name}/seed_${seed}"
  if [ "$agent_config" = "none" ]; then
    uv run configre --run-case \
      --case-input "$case_input" --artifacts-dir "$dir" \
      --run-record "$dir/run_record.json" \
      --system "$SYSTEM" --setting "$SETTING" \
      --seed "$seed" --round-cap "$ROUND_CAP" $RAG_ARGS
  elif [ "$agent_config" = "auto" ]; then
    uv run configre --run-case \
      --case-input "$case_input" --artifacts-dir "$dir" \
      --run-record "$dir/run_record.json" \
      --system "$SYSTEM" --setting "$SETTING" \
      --seed "$seed" --round-cap "$ROUND_CAP" \
      --agent-config auto $RAG_ARGS
  else
    uv run configre --run-case \
      --case-input "$case_input" --artifacts-dir "$dir" \
      --run-record "$dir/run_record.json" \
      --system "$SYSTEM" --setting "$SETTING" \
      --seed "$seed" --round-cap "$ROUND_CAP" \
      --agent-config "$agent_config" $RAG_ARGS
  fi
}

run_case() {
  local case_id="$1" case_input="$2" domain_opt="$3"
  echo "=== ${case_id} ==="
  for seed in 101 202 303; do
    run_one "$case_id" "$case_input" "config_a" "$seed" "none"
    run_one "$case_id" "$case_input" "config_b" "$seed" "$domain_opt"
    run_one "$case_id" "$case_input" "config_c" "$seed" "$FULL_15"
    run_one "$case_id" "$case_input" "config_d" "$seed" "auto"
  done
}

run_case "EHR" "data/case_studies/EHR_input.json" \
  '["SecurityAgent","PrivacyAgent","ReliabilityAgent","UsabilityAgent","CompatibilityAgent","PerformanceAgent"]'

run_case "SmartGrid" "data/case_studies/SmartGrid_input.json" \
  '["SafetyAgent","PerformanceAgent","ReliabilityAgent","SecurityAgent","GreenAgent","EfficiencyAgent"]'

run_case "LoanApproval" "data/case_studies/LoanApproval_input.json" \
  '["ExplainabilityAgent","SecurityAgent","PrivacyAgent","ReliabilityAgent","ResponsibilityAgent","PerformanceAgent"]'

echo "=== All new case study runs complete ==="

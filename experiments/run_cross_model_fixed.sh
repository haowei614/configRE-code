#!/usr/bin/env bash
# Cross-Model Validation with Claude 3.5 Sonnet
# Runs Fixed-5 and Phase0-Auto across all 5 original case studies × 3 seeds
set -e
set -a; source .env; set +a

MODEL="${ALT_MODEL:-gpt-4o}"
MODEL_LABEL=$(echo "$MODEL" | tr '/:.' '_')
SYSTEM="quare"
SETTING="negotiation_integration_verification"
ROUND_CAP=3
BASE_DIR="experiments/results/cross_model/${MODEL_LABEL}"
RAG_ARGS="--rag-corpus-dir data/knowledge_base --rag-backend local_tfidf"

CASES="AD:data/case_studies/AD_input.json
ATM:data/case_studies/ATM_input.json
Library:data/case_studies/Library_input.json
RollCall:data/case_studies/RollCall_input.json
Bookkeeping:data/case_studies/Bookkeeping_input.json"

echo "=== Cross-Model Validation: ${MODEL} ==="

echo "$CASES" | while IFS=: read -r case_id case_input; do
  echo "--- ${case_id} ---"
  for config in fixed5 auto; do
    for seed in 101 202 303; do
      dir="${BASE_DIR}/${case_id}/${config}/seed_${seed}"
      if [ -f "$dir/run_record.json" ]; then
        echo "  SKIP: ${case_id}/${config}/seed_${seed}"
        continue
      fi
      mkdir -p "$dir"
      echo "  RUN: ${case_id}/${config}/seed_${seed}"

      agent_arg=""
      if [ "$config" = "auto" ]; then
        agent_arg="--agent-config auto"
      fi

      uv run configre --run-case \
        --case-input "$case_input" \
        --artifacts-dir "$dir" \
        --run-record "$dir/run_record.json" \
        --system "$SYSTEM" --setting "$SETTING" \
        --seed "$seed" --round-cap "$ROUND_CAP" \
        --model "$MODEL" \
        $agent_arg $RAG_ARGS
    done
  done
done

echo "=== Cross-model (${MODEL}) complete ==="

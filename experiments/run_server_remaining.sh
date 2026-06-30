#!/usr/bin/env bash
# Run only remaining experiments on lab server (skip completed runs).
set -euo pipefail
set -a; source .env; set +a

echo "=== ConfigRE: Server Remaining Experiments ==="
echo "Time: $(date -Iseconds)"
echo ""

# 1. Open-weight Phase 0 cross-model (local Ollama, no API cost)
if command -v ollama &>/dev/null; then
  OLLAMA_MODEL="${OLLAMA_MODEL:-llama3.1:8b}"
  if ollama list | grep -q "$OLLAMA_MODEL"; then
    echo ">>> Phase 0 cross-model: $OLLAMA_MODEL"
    uv run python experiments/run_phase0_ollama_cross_model.py --model "$OLLAMA_MODEL"
  else
    echo ">>> Pulling $OLLAMA_MODEL ..."
    ollama pull "$OLLAMA_MODEL"
    uv run python experiments/run_phase0_ollama_cross_model.py --model "$OLLAMA_MODEL"
  fi
else
  echo "SKIP: ollama not installed (open-weight Phase 0)"
fi

# 2. Claude cross-model (only if API works)
if [ -n "${ANTHROPIC_API_KEY:-}" ]; then
  echo ">>> Testing Anthropic API ..."
  HTTP_CODE=$(curl -s -o /tmp/anthropic_test.json -w "%{http_code}" \
    https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{"model":"claude-3-5-haiku-latest","max_tokens":5,"messages":[{"role":"user","content":"hi"}]}')

  if [ "$HTTP_CODE" = "200" ]; then
    echo ">>> Claude cross-model"
    ALT_MODEL=anthropic/claude-sonnet-4-20250514 bash experiments/run_cross_model_fixed.sh
    uv run python experiments/analyze_cross_model.py
  else
    echo "SKIP: Anthropic API unavailable (HTTP $HTTP_CODE)"
    cat /tmp/anthropic_test.json 2>/dev/null | head -3
  fi
else
  echo "SKIP: ANTHROPIC_API_KEY not set"
fi

echo ""
echo "=== Done ==="
echo "Results in experiments/results/"

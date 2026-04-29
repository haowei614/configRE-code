#!/bin/bash
set -e

CASE_INPUT="data/case_studies/AD_input.json"
BASE_DIR="experiments/results"
SYSTEM="quare"
SETTING="negotiation_integration_verification"
ROUND_CAP=3

# Config A: Fixed-5 (baseline)
echo "=== Running Config A: Fixed-5 ==="
for SEED in 101 202 303; do
  DIR="${BASE_DIR}/config_a/seed_${SEED}"
  mkdir -p "$DIR"
  uv run configre --run-case \
    --case-input "$CASE_INPUT" \
    --artifacts-dir "$DIR" \
    --run-record "$DIR/run_record.json" \
    --system "$SYSTEM" \
    --setting "$SETTING" \
    --seed "$SEED" \
    --round-cap "$ROUND_CAP"
  echo "Config A seed $SEED done"
done

# Config B: Domain-optimized for AD (6 agents)
echo "=== Running Config B: Domain-optimized ==="
CONFIG_B='["SafetyAgent","EfficiencyAgent","ReliabilityAgent","FunctionalSafetyAgent","GreenAgent","ResponsibilityAgent"]'
for SEED in 101 202 303; do
  DIR="${BASE_DIR}/config_b/seed_${SEED}"
  mkdir -p "$DIR"
  uv run configre --run-case \
    --case-input "$CASE_INPUT" \
    --artifacts-dir "$DIR" \
    --run-record "$DIR/run_record.json" \
    --system "$SYSTEM" \
    --setting "$SETTING" \
    --seed "$SEED" \
    --round-cap "$ROUND_CAP" \
    --agent-config "$CONFIG_B"
  echo "Config B seed $SEED done"
done

# Config C: Full-15 (all agents)
echo "=== Running Config C: Full-15 ==="
CONFIG_C='["SafetyAgent","EfficiencyAgent","GreenAgent","TrustworthinessAgent","ResponsibilityAgent","ReliabilityAgent","UsabilityAgent","SecurityAgent","MaintainabilityAgent","CompatibilityAgent","FlexibilityAgent","PerformanceAgent","FunctionalSafetyAgent","ExplainabilityAgent","PrivacyAgent"]'
for SEED in 101 202 303; do
  DIR="${BASE_DIR}/config_c/seed_${SEED}"
  mkdir -p "$DIR"
  uv run configre --run-case \
    --case-input "$CASE_INPUT" \
    --artifacts-dir "$DIR" \
    --run-record "$DIR/run_record.json" \
    --system "$SYSTEM" \
    --setting "$SETTING" \
    --seed "$SEED" \
    --round-cap "$ROUND_CAP" \
    --agent-config "$CONFIG_C"
  echo "Config C seed $SEED done"
done

# Config D-AD: Phase 0 Auto Selection
echo "=== Running Config D-AD: Phase 0 Auto ==="
for SEED in 101 202 303; do
  DIR="${BASE_DIR}/config_d/seed_${SEED}"
  mkdir -p "$DIR"
  uv run configre --run-case \
    --case-input "$CASE_INPUT" \
    --artifacts-dir "$DIR" \
    --run-record "$DIR/run_record.json" \
    --system "$SYSTEM" \
    --setting "$SETTING" \
    --seed "$SEED" \
    --round-cap "$ROUND_CAP" \
    --agent-config auto
  echo "Config D-AD seed $SEED done"
done

# ======== ATM Case Study ========
ATM_CASE_INPUT="data/case_studies/ATM_input.json"

# Config A-ATM: Fixed-5 (baseline)
echo "=== Running ATM Config A: Fixed-5 ==="
for SEED in 101 202 303; do
  DIR="${BASE_DIR}/atm_config_a/seed_${SEED}"
  mkdir -p "$DIR"
  uv run configre --run-case \
    --case-input "$ATM_CASE_INPUT" \
    --artifacts-dir "$DIR" \
    --run-record "$DIR/run_record.json" \
    --system "$SYSTEM" \
    --setting "$SETTING" \
    --seed "$SEED" \
    --round-cap "$ROUND_CAP"
  echo "ATM Config A seed $SEED done"
done

# Config B-ATM: Domain-optimized for ATM (6 agents)
echo "=== Running ATM Config B: Domain-optimized ==="
CONFIG_B_ATM='["SecurityAgent","TrustworthinessAgent","ReliabilityAgent","EfficiencyAgent","ResponsibilityAgent","PrivacyAgent"]'
for SEED in 101 202 303; do
  DIR="${BASE_DIR}/atm_config_b/seed_${SEED}"
  mkdir -p "$DIR"
  uv run configre --run-case \
    --case-input "$ATM_CASE_INPUT" \
    --artifacts-dir "$DIR" \
    --run-record "$DIR/run_record.json" \
    --system "$SYSTEM" \
    --setting "$SETTING" \
    --seed "$SEED" \
    --round-cap "$ROUND_CAP" \
    --agent-config "$CONFIG_B_ATM"
  echo "ATM Config B seed $SEED done"
done

# Config C-ATM: Full-15
echo "=== Running ATM Config C: Full-15 ==="
for SEED in 101 202 303; do
  DIR="${BASE_DIR}/atm_config_c/seed_${SEED}"
  mkdir -p "$DIR"
  uv run configre --run-case \
    --case-input "$ATM_CASE_INPUT" \
    --artifacts-dir "$DIR" \
    --run-record "$DIR/run_record.json" \
    --system "$SYSTEM" \
    --setting "$SETTING" \
    --seed "$SEED" \
    --round-cap "$ROUND_CAP" \
    --agent-config "$CONFIG_C"
  echo "ATM Config C seed $SEED done"
done

# Config D-ATM: Phase 0 Auto Selection
echo "=== Running Config D-ATM: Phase 0 Auto ==="
for SEED in 101 202 303; do
  DIR="${BASE_DIR}/atm_config_d/seed_${SEED}"
  mkdir -p "$DIR"
  uv run configre --run-case \
    --case-input "$ATM_CASE_INPUT" \
    --artifacts-dir "$DIR" \
    --run-record "$DIR/run_record.json" \
    --system "$SYSTEM" \
    --setting "$SETTING" \
    --seed "$SEED" \
    --round-cap "$ROUND_CAP" \
    --agent-config auto
  echo "Config D-ATM seed $SEED done"
done

# ======== Library Case Study ========
LIB_CASE_INPUT="data/case_studies/Library_input.json"

# Config A-Library: Fixed-5
echo "=== Running Library Config A: Fixed-5 ==="
for SEED in 101 202 303; do
  DIR="${BASE_DIR}/lib_config_a/seed_${SEED}"
  mkdir -p "$DIR"
  uv run configre --run-case \
    --case-input "$LIB_CASE_INPUT" \
    --artifacts-dir "$DIR" \
    --run-record "$DIR/run_record.json" \
    --system "$SYSTEM" \
    --setting "$SETTING" \
    --seed "$SEED" \
    --round-cap "$ROUND_CAP"
  echo "Library Config A seed $SEED done"
done

# Config B-Library: Domain-optimized-6
echo "=== Running Library Config B: Domain-optimized ==="
CONFIG_B_LIB='["UsabilityAgent","ReliabilityAgent","MaintainabilityAgent","SecurityAgent","EfficiencyAgent","ResponsibilityAgent"]'
for SEED in 101 202 303; do
  DIR="${BASE_DIR}/lib_config_b/seed_${SEED}"
  mkdir -p "$DIR"
  uv run configre --run-case \
    --case-input "$LIB_CASE_INPUT" \
    --artifacts-dir "$DIR" \
    --run-record "$DIR/run_record.json" \
    --system "$SYSTEM" \
    --setting "$SETTING" \
    --seed "$SEED" \
    --round-cap "$ROUND_CAP" \
    --agent-config "$CONFIG_B_LIB"
  echo "Library Config B seed $SEED done"
done

# Config C-Library: Full-15
echo "=== Running Library Config C: Full-15 ==="
for SEED in 101 202 303; do
  DIR="${BASE_DIR}/lib_config_c/seed_${SEED}"
  mkdir -p "$DIR"
  uv run configre --run-case \
    --case-input "$LIB_CASE_INPUT" \
    --artifacts-dir "$DIR" \
    --run-record "$DIR/run_record.json" \
    --system "$SYSTEM" \
    --setting "$SETTING" \
    --seed "$SEED" \
    --round-cap "$ROUND_CAP" \
    --agent-config "$CONFIG_C"
  echo "Library Config C seed $SEED done"
done

# Config D-Library: Phase 0 Auto
echo "=== Running Library Config D: Phase 0 Auto ==="
for SEED in 101 202 303; do
  DIR="${BASE_DIR}/lib_config_d/seed_${SEED}"
  mkdir -p "$DIR"
  uv run configre --run-case \
    --case-input "$LIB_CASE_INPUT" \
    --artifacts-dir "$DIR" \
    --run-record "$DIR/run_record.json" \
    --system "$SYSTEM" \
    --setting "$SETTING" \
    --seed "$SEED" \
    --round-cap "$ROUND_CAP" \
    --agent-config auto
  echo "Library Config D seed $SEED done"
done

# ======== RollCall Case Study ========
RC_CASE_INPUT="data/case_studies/RollCall_input.json"

# Config A-RollCall: Fixed-5
echo "=== Running RollCall Config A: Fixed-5 ==="
for SEED in 101 202 303; do
  DIR="${BASE_DIR}/rc_config_a/seed_${SEED}"
  mkdir -p "$DIR"
  uv run configre --run-case \
    --case-input "$RC_CASE_INPUT" \
    --artifacts-dir "$DIR" \
    --run-record "$DIR/run_record.json" \
    --system "$SYSTEM" \
    --setting "$SETTING" \
    --seed "$SEED" \
    --round-cap "$ROUND_CAP"
  echo "RollCall Config A seed $SEED done"
done

# Config B-RollCall: Domain-optimized-6
echo "=== Running RollCall Config B: Domain-optimized ==="
CONFIG_B_RC='["UsabilityAgent","ReliabilityAgent","SecurityAgent","TrustworthinessAgent","PrivacyAgent","ResponsibilityAgent"]'
for SEED in 101 202 303; do
  DIR="${BASE_DIR}/rc_config_b/seed_${SEED}"
  mkdir -p "$DIR"
  uv run configre --run-case \
    --case-input "$RC_CASE_INPUT" \
    --artifacts-dir "$DIR" \
    --run-record "$DIR/run_record.json" \
    --system "$SYSTEM" \
    --setting "$SETTING" \
    --seed "$SEED" \
    --round-cap "$ROUND_CAP" \
    --agent-config "$CONFIG_B_RC"
  echo "RollCall Config B seed $SEED done"
done

# Config C-RollCall: Full-15
echo "=== Running RollCall Config C: Full-15 ==="
for SEED in 101 202 303; do
  DIR="${BASE_DIR}/rc_config_c/seed_${SEED}"
  mkdir -p "$DIR"
  uv run configre --run-case \
    --case-input "$RC_CASE_INPUT" \
    --artifacts-dir "$DIR" \
    --run-record "$DIR/run_record.json" \
    --system "$SYSTEM" \
    --setting "$SETTING" \
    --seed "$SEED" \
    --round-cap "$ROUND_CAP" \
    --agent-config "$CONFIG_C"
  echo "RollCall Config C seed $SEED done"
done

# Config D-RollCall: Phase 0 Auto
echo "=== Running RollCall Config D: Phase 0 Auto ==="
for SEED in 101 202 303; do
  DIR="${BASE_DIR}/rc_config_d/seed_${SEED}"
  mkdir -p "$DIR"
  uv run configre --run-case \
    --case-input "$RC_CASE_INPUT" \
    --artifacts-dir "$DIR" \
    --run-record "$DIR/run_record.json" \
    --system "$SYSTEM" \
    --setting "$SETTING" \
    --seed "$SEED" \
    --round-cap "$ROUND_CAP" \
    --agent-config auto
  echo "RollCall Config D seed $SEED done"
done

# ======== Bookkeeping Case Study ========
BK_CASE_INPUT="data/case_studies/Bookkeeping_input.json"

# Config A-Bookkeeping: Fixed-5
echo "=== Running Bookkeeping Config A: Fixed-5 ==="
for SEED in 101 202 303; do
  DIR="${BASE_DIR}/bk_config_a/seed_${SEED}"
  mkdir -p "$DIR"
  uv run configre --run-case \
    --case-input "$BK_CASE_INPUT" \
    --artifacts-dir "$DIR" \
    --run-record "$DIR/run_record.json" \
    --system "$SYSTEM" \
    --setting "$SETTING" \
    --seed "$SEED" \
    --round-cap "$ROUND_CAP"
  echo "Bookkeeping Config A seed $SEED done"
done

# Config B-Bookkeeping: Domain-optimized-6
echo "=== Running Bookkeeping Config B: Domain-optimized ==="
CONFIG_B_BK='["SecurityAgent","ReliabilityAgent","TrustworthinessAgent","ResponsibilityAgent","EfficiencyAgent","PrivacyAgent"]'
for SEED in 101 202 303; do
  DIR="${BASE_DIR}/bk_config_b/seed_${SEED}"
  mkdir -p "$DIR"
  uv run configre --run-case \
    --case-input "$BK_CASE_INPUT" \
    --artifacts-dir "$DIR" \
    --run-record "$DIR/run_record.json" \
    --system "$SYSTEM" \
    --setting "$SETTING" \
    --seed "$SEED" \
    --round-cap "$ROUND_CAP" \
    --agent-config "$CONFIG_B_BK"
  echo "Bookkeeping Config B seed $SEED done"
done

# Config C-Bookkeeping: Full-15
echo "=== Running Bookkeeping Config C: Full-15 ==="
for SEED in 101 202 303; do
  DIR="${BASE_DIR}/bk_config_c/seed_${SEED}"
  mkdir -p "$DIR"
  uv run configre --run-case \
    --case-input "$BK_CASE_INPUT" \
    --artifacts-dir "$DIR" \
    --run-record "$DIR/run_record.json" \
    --system "$SYSTEM" \
    --setting "$SETTING" \
    --seed "$SEED" \
    --round-cap "$ROUND_CAP" \
    --agent-config "$CONFIG_C"
  echo "Bookkeeping Config C seed $SEED done"
done

# Config D-Bookkeeping: Phase 0 Auto
echo "=== Running Bookkeeping Config D: Phase 0 Auto ==="
for SEED in 101 202 303; do
  DIR="${BASE_DIR}/bk_config_d/seed_${SEED}"
  mkdir -p "$DIR"
  uv run configre --run-case \
    --case-input "$BK_CASE_INPUT" \
    --artifacts-dir "$DIR" \
    --run-record "$DIR/run_record.json" \
    --system "$SYSTEM" \
    --setting "$SETTING" \
    --seed "$SEED" \
    --round-cap "$ROUND_CAP" \
    --agent-config auto
  echo "Bookkeeping Config D seed $SEED done"
done

echo "=== All runs complete ==="

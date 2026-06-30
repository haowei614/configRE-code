# 实验室服务器部署指南

Mac 上已完成大部分 API 实验（172 runs，~105MB）。服务器上**只需补跑剩余实验**，不必全部重跑。

## 已完成（Mac 本地，可同步到服务器）

| 实验 | Runs | 目录 |
|---|---|---|
| 新 case studies (EHR/SmartGrid/LoanApproval) | 36 | `experiments/results/extended/` |
| τ₁ Sensitivity | 105 | `experiments/results/threshold_sensitivity/` |
| Cross-model GPT-4o | 30 | `experiments/results/cross_model/gpt-4o/` |

## 服务器上还需跑

| 实验 | 脚本 | 说明 |
|---|---|---|
| Open-weight Phase 0 (Llama/Qwen) | `run_phase0_ollama_cross_model.py` | 仅 Phase 0，不跑完整 pipeline，GPU 上很快 |
| Claude cross-model（可选） | `run_cross_model_fixed.sh` | 充值 Anthropic 后运行 |
| Human evaluation | 手动 | 见 `human_evaluation_rubric.json` |

---

## 1. 从 Mac 同步到服务器

在 **Mac** 上执行（替换 `USER@SERVER` 和路径）：

```bash
# 同步代码（不含 .venv 和巨大 artifact）
rsync -avz --progress \
  --exclude '.venv' \
  --exclude '__pycache__' \
  --exclude '.git' \
  /Users/haowei/Downloads/ConfigRE/configRE-code/ \
  USER@SERVER:~/configRE-code/

# 同步已有实验结果（避免重跑）
rsync -avz --progress \
  /Users/haowei/Downloads/ConfigRE/configRE-code/experiments/results/ \
  USER@SERVER:~/configRE-code/experiments/results/
```

在 **服务器** 上创建 `.env`（不要通过 git 传 key）：

```bash
cd ~/configRE-code
cat > .env << 'EOF'
OPENAI_API_KEY=sk-proj-...
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_MODEL=gpt-4o-mini
EOF
chmod 600 .env
```

---

## 2. 服务器环境安装

```bash
cd ~/configRE-code

# 安装 uv（如未安装）
curl -LsSf https://astral.sh/uv/install.sh | sh

# Python 3.13 + 依赖
echo "3.13" > .python-version
uv sync --all-groups

# 验证
uv run configre --version
uv run configre --check-openai
```

---

## 3. Ollama + Llama（Open-weight 实验）

```bash
# 安装 Ollama（Linux 示例）
curl -fsSL https://ollama.com/install.sh | sh

# 拉取模型（推荐 Llama 3.1 8B，论文里写 open-weight validation）
ollama pull llama3.1:8b

# 可选：Qwen（你 Mac 上已有，服务器也可拉）
# ollama pull qwen3.5:9b

# 确认服务运行
ollama list
curl http://localhost:11434/api/tags
```

### 跑 Phase 0 cross-model（轻量，推荐）

```bash
cd ~/configRE-code

# Llama 3.1 8B — 8 cases × 3 seeds，GPU 上约 30-60 分钟
uv run python experiments/run_phase0_ollama_cross_model.py --model llama3.1:8b

# 如果要用 Qwen，加 --think（Qwen3 是 thinking model）
# uv run python experiments/run_phase0_ollama_cross_model.py --model qwen3.5:9b --think
```

结果保存在：`experiments/results/phase0_cross_model/<model>/`

---

## 4. Claude cross-model（Anthropic 充值后）

```bash
cd ~/configRE-code
ALT_MODEL=anthropic/claude-sonnet-4-20250514 \
  bash experiments/run_cross_model_fixed.sh

uv run python experiments/analyze_cross_model.py
```

---

## 5. 用 screen/tmux 后台跑（防止 SSH 断开）

```bash
screen -S configre
cd ~/configRE-code
uv run python experiments/run_phase0_ollama_cross_model.py --model llama3.1:8b
# Ctrl+A, D  detach

# 重新连接
screen -r configre
```

---

## 6. 结果同步回 Mac

```bash
# 在 Mac 上执行
rsync -avz --progress \
  USER@SERVER:~/configRE-code/experiments/results/ \
  /Users/haowei/Downloads/ConfigRE/configRE-code/experiments/results/
```

---

## 7. 生成论文表格

在任一机器上（有 results 即可）：

```bash
cd ~/configRE-code
uv run python experiments/analyze_threshold_sensitivity.py
uv run python experiments/analyze_cross_model.py
uv run python experiments/compare_results.py
```

LaTeX 表格输出：
- `experiments/results/threshold_sensitivity_table.tex`
- `experiments/results/cross_model_table.tex`

---

## 注意事项

1. **Mac 上 Qwen3.5:9b 的问题**：Qwen3 是 thinking model，LiteLLM 调用会返回空 content。服务器上请用本仓库的 `run_phase0_ollama_cross_model.py`（原生 Ollama API + `think=false`），或直接用 **Llama 3.1**。
2. **不要重跑已完成实验**：同步 `experiments/results/` 后脚本会自动 SKIP 已有 `run_record.json`。
3. **RAG 参数**：完整 pipeline 需要 `--rag-corpus-dir data/knowledge_base --rag-backend local_tfidf`（脚本里已内置）。
4. **Python 版本**：用 3.13，不要用 3.14 free-threaded（tokenizers 编译会失败）。

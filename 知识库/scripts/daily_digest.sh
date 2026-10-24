#!/bin/bash
# 每日 07:00 由 launchd 调用，生成当天的 IT 时事速递草稿。
#
# 手动测试：
#   bash 知识库/scripts/daily_digest.sh
#
# 日志：
#   知识库/scripts/logs/digest.log        正常输出
#   知识库/scripts/logs/digest.error.log  错误输出

set -euo pipefail

KB_DIR="/Users/tonydongbo/Documents/deepseek-harness/default-workspace/知识库"
LOG_DIR="$KB_DIR/scripts/logs"
PYTHON="/usr/bin/python3"

mkdir -p "$LOG_DIR"

# 日志由 launchd 的 StandardOutPath / StandardErrorPath 重定向到
#   $LOG_DIR/digest.log 与 $LOG_DIR/digest.error.log
# 手动运行时直接输出到终端。
# 日志超过 1MB 时截断，避免无限增长。
LOG_FILE="$LOG_DIR/digest.log"
if [ -f "$LOG_FILE" ] && [ "$(wc -c < "$LOG_FILE")" -gt 1048576 ]; then
    tail -n 500 "$LOG_FILE" > "$LOG_FILE.tmp" && mv "$LOG_FILE.tmp" "$LOG_FILE"
fi

stamp() { date "+%Y-%m-%d %H:%M:%S"; }

echo "[$(stamp)] ===== 开始生成时事速递 ====="

if [ ! -d "$KB_DIR" ]; then
    echo "[$(stamp)] 错误：知识库目录不存在：$KB_DIR" >&2
    exit 1
fi

cd "$KB_DIR"

# new_digest.py 幂等：当天已存在则跳过，不会覆盖已填写的内容
if "$PYTHON" scripts/new_digest.py; then
    echo "[$(stamp)] 完成"
else
    code=$?
    echo "[$(stamp)] 失败，退出码 $code" >&2
    exit "$code"
fi

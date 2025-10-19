#!/bin/bash
# IEEE専用研究調査スクリプト（安定版）

set -euo pipefail

echo "🔍 IEEE Xplore専用研究調査"
echo ""

# ゾンビプロセスクリーンアップ
echo "🧹 ブラウザプロセスをクリーンアップ中..."
pkill -9 chromium 2>/dev/null || true
rm -rf /tmp/browser-use-user-data-dir-* 2>/dev/null || true
echo "✅ クリーンアップ完了"
echo ""

# 環境変数設定（タイムアウト延長）
export TIMEOUT_BrowserStartEvent=300
export TIMEOUT_BrowserLaunchEvent=300
export TIMEOUT_CDP_URL_WAIT=300
export TIMEOUT_NavigateToUrlEvent=120

# Chromium KWallet問題を回避（KDE環境）
export CHROMIUM_PASSWORD_STORE="basic"
export CHROME_PASSWORD_STORE="basic"

# デフォルト値
PROVIDER="${1:-deepseek}"
MAX_PAPERS="${2:-10}"

echo "📊 設定:"
echo "  LLM: ${PROVIDER}"
echo "  最大論文数: ${MAX_PAPERS}"
echo "  ヘッドレス: False（安定性優先）"
echo "  データベース: IEEE Xplore"
echo ""

# 実行
echo "🚀 研究調査を開始..."
echo ""

uv run python -m automated_research.main \
	--provider "${PROVIDER}" \
	--max-papers "${MAX_PAPERS}" \
	--no-headless \
	--non-interactive

echo ""
echo "🎉 完了！"

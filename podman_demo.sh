#!/bin/bash
# Podmanデモ実行スクリプト（簡易版）
# Usage: ./podman_demo.sh [provider]
# Example: ./podman_demo.sh claude

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# LLMプロバイダーを引数から取得（デフォルト: deepseek）
PROVIDER="${1:-deepseek}"

echo "======================================================================================================"
echo "🐳 Podman デモ実行 - $PROVIDER プロバイダー"
echo "======================================================================================================"
echo ""

# .envファイルの確認
if [ ! -f .env ]; then
	echo "❌ .envファイルが見つかりません"
	echo ""
	echo "以下のコマンドで.envファイルを作成してください:"
	echo "  cp .env.example .env"
	echo "  nano .env  # APIキーを設定"
	exit 1
fi

# イメージが存在するか確認
IMAGE_NAME="browser-use-research"
if ! podman image exists "$IMAGE_NAME:latest"; then
	echo "⚠️  イメージが見つかりません。ビルドします..."
	echo ""
	podman build -t "$IMAGE_NAME:latest" -f Containerfile .
	echo ""
fi

# デモ実行
echo "🚀 デモを実行中..."
echo "   プロバイダー: $PROVIDER"
echo "   論文数: 3-5件"
echo ""

LLM_PROVIDER="$PROVIDER" USE_DEMO=true exec ./run_podman.sh

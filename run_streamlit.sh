#!/bin/bash
# Streamlit Web UI 起動スクリプト

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# カラー出力
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}=====================================================================================================${NC}"
echo -e "${BLUE}🤖 完全自動化研究支援システム - Streamlit Web UI${NC}"
echo -e "${BLUE}=====================================================================================================${NC}"
echo ""

# .envファイルの確認
if [ ! -f .env ]; then
	echo -e "${RED}❌ .envファイルが見つかりません${NC}"
	echo -e "${YELLOW}以下のコマンドで.envファイルを作成してください:${NC}"
	echo "  cp .env.example .env"
	echo "  nano .env  # APIキーを設定"
	exit 1
fi

echo -e "${GREEN}✅ .envファイルを検出${NC}"
echo ""

# 環境変数を読み込み
set -a
source .env
set +a

echo -e "${BLUE}🚀 Streamlit Webアプリを起動中...${NC}"
echo ""
echo -e "${GREEN}アクセスURL: http://localhost:8501${NC}"
echo ""
echo -e "${YELLOW}終了するには Ctrl+C を押してください${NC}"
echo ""

# Streamlit起動
uv run streamlit run streamlit_app.py \
	--server.port 8501 \
	--server.address localhost \
	--browser.gatherUsageStats false \
	--theme.base light

#!/bin/bash
# Podman実行スクリプト - .env環境変数を使用
# マルチLLMプロバイダー対応版

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# カラー出力
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=====================================================================================================${NC}"
echo -e "${BLUE}🐳 Podman自動研究システム - マルチLLMプロバイダー対応${NC}"
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

# イメージ名とタグ
IMAGE_NAME="browser-use-research"
IMAGE_TAG="latest"

# イメージが存在するか確認
if ! podman image exists "$IMAGE_NAME:$IMAGE_TAG"; then
	echo -e "${YELLOW}⚠️  イメージが見つかりません。ビルドを開始します...${NC}"
	echo ""

	echo -e "${BLUE}🔨 Podmanイメージをビルド中...${NC}"
	podman build -t "$IMAGE_NAME:$IMAGE_TAG" -f Containerfile .

	if [ $? -eq 0 ]; then
		echo -e "${GREEN}✅ イメージビルド完了${NC}"
	else
		echo -e "${RED}❌ イメージビルド失敗${NC}"
		exit 1
	fi
	echo ""
else
	echo -e "${GREEN}✅ イメージが存在します: $IMAGE_NAME:$IMAGE_TAG${NC}"
	echo ""
fi

# 実行オプション
PROVIDER="${LLM_PROVIDER:-deepseek}"
MAX_PAPERS="${MAX_PAPERS:-20}"
HEADLESS="${HEADLESS:-false}"

echo -e "${BLUE}実行設定:${NC}"
echo "  LLMプロバイダー: $PROVIDER"
echo "  最大論文数: $MAX_PAPERS"
echo "  ヘッドレスモード: $HEADLESS"
echo ""

# ディレクトリ作成（存在しない場合）
mkdir -p automated_research/data
mkdir -p automated_research/reports
mkdir -p automated_research/logs
mkdir -p papers

echo -e "${BLUE}📁 データディレクトリを準備${NC}"
echo "  automated_research/data/"
echo "  automated_research/reports/"
echo "  automated_research/logs/"
echo "  papers/"
echo ""

# Podman実行
echo -e "${BLUE}=====================================================================================================${NC}"
echo -e "${BLUE}🚀 Podmanコンテナを起動中...${NC}"
echo -e "${BLUE}=====================================================================================================${NC}"
echo ""

# デモスクリプトを使用する場合（対話なし）
if [ "${USE_DEMO:-false}" = "true" ]; then
	echo -e "${YELLOW}📝 デモモードで実行（対話型インタビューなし）${NC}"
	echo ""

	podman run --rm -it \
		--env-file .env \
		-e LLM_PROVIDER="$PROVIDER" \
		-v ./automated_research/data:/app/automated_research/data:z \
		-v ./automated_research/reports:/app/automated_research/reports:z \
		-v ./automated_research/logs:/app/automated_research/logs:z \
		-v ./papers:/app/papers:z \
		"$IMAGE_NAME:$IMAGE_TAG" \
		python demo_llm_research.py
else
	# 完全版実行（対話型）
	echo -e "${YELLOW}📝 完全版で実行（対話型インタビューあり）${NC}"
	echo -e "${YELLOW}※ 対話型は現在サポートされていません。代わりにデモモードを使用してください。${NC}"
	echo ""
	echo "デモモードで実行するには:"
	echo "  USE_DEMO=true ./run_podman.sh"
	exit 1

	# podman run --rm -it \
	# 	--env-file .env \
	# 	-e LLM_PROVIDER="$PROVIDER" \
	# 	-v ./automated_research/data:/app/automated_research/data:z \
	# 	-v ./automated_research/reports:/app/automated_research/reports:z \
	# 	-v ./automated_research/logs:/app/automated_research/logs:z \
	# 	-v ./papers:/app/papers:z \
	# 	"$IMAGE_NAME:$IMAGE_TAG" \
	# 	python -m automated_research.main --provider "$PROVIDER" --max-papers "$MAX_PAPERS" $([ "$HEADLESS" = "true" ] && echo "--headless" || echo "")
fi

EXIT_CODE=$?

echo ""
echo -e "${BLUE}=====================================================================================================${NC}"
if [ $EXIT_CODE -eq 0 ]; then
	echo -e "${GREEN}✅ 処理が完了しました${NC}"
	echo ""
	echo -e "${BLUE}生成されたファイル:${NC}"
	echo "  📁 データ: automated_research/data/"
	echo "  📁 レポート: automated_research/reports/"
	echo "  📁 ログ: automated_research/logs/"
	echo "  📁 論文: papers/"
else
	echo -e "${RED}❌ 処理が失敗しました (終了コード: $EXIT_CODE)${NC}"
fi
echo -e "${BLUE}=====================================================================================================${NC}"

exit $EXIT_CODE

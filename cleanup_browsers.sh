#!/bin/bash
# ゾンビChromiumプロセスと一時ファイルをクリーンアップ

set -euo pipefail

# カラー出力
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}🧹 ブラウザプロセスとテンポラリファイルをクリーンアップ中...${NC}"
echo ""

# Chromiumプロセス数をカウント
CHROME_COUNT=$(ps aux | grep -i chromium | grep -v grep | grep -v "systemsettings" | wc -l)

if [ "$CHROME_COUNT" -gt 0 ]; then
	echo -e "${RED}⚠️  ${CHROME_COUNT}個のChromiumプロセスを検出${NC}"
	echo "以下のプロセスを終了します:"
	ps aux | grep -i chromium | grep -v grep | grep -v "systemsettings" | head -5
	echo ""

	# Chromiumプロセスを強制終了
	pkill -9 chromium || true
	sleep 1

	NEW_COUNT=$(ps aux | grep -i chromium | grep -v grep | grep -v "systemsettings" | wc -l)
	if [ "$NEW_COUNT" -eq 0 ]; then
		echo -e "${GREEN}✅ すべてのChromiumプロセスを終了しました${NC}"
	else
		echo -e "${YELLOW}⚠️  ${NEW_COUNT}個のプロセスが残っています${NC}"
	fi
else
	echo -e "${GREEN}✅ Chromiumプロセスは実行されていません${NC}"
fi

echo ""

# 一時ディレクトリをクリーンアップ
TEMP_DIRS=$(find /tmp -maxdepth 1 -name "browser-use-user-data-dir-*" 2>/dev/null | wc -l)

if [ "$TEMP_DIRS" -gt 0 ]; then
	echo -e "${YELLOW}🗑️  ${TEMP_DIRS}個の一時ディレクトリを削除中...${NC}"
	rm -rf /tmp/browser-use-user-data-dir-* || true
	echo -e "${GREEN}✅ 一時ディレクトリをクリーンアップしました${NC}"
else
	echo -e "${GREEN}✅ クリーンアップが必要な一時ディレクトリはありません${NC}"
fi

echo ""
echo -e "${GREEN}🎉 クリーンアップ完了！${NC}"

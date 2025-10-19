#!/bin/bash
# Chromium KWallet修正テスト

pkill -9 chromium 2>/dev/null || true

export CHROMIUM_PASSWORD_STORE="basic"
export CHROME_PASSWORD_STORE="basic"

echo "🧪 Chromium起動テスト（KWallet無効化）"
chromium --headless=new --remote-debugging-port=9666 --disable-dev-shm-usage > /tmp/chromium_kwallet_fix.log 2>&1 &
CHROME_PID=$!

echo "⏳ 10秒待機..."
sleep 10

echo "🔍 CDP URLテスト..."
CDP_RESPONSE=$(curl -s http://localhost:9666/json/version 2>&1)

if echo "$CDP_RESPONSE" | grep -q "webSocketDebuggerUrl"; then
	echo "✅ 成功！CDPポートが応答しています"
	echo "$CDP_RESPONSE" | head -5
else
	echo "❌ 失敗：CDPポート無応答"
	echo "応答: $CDP_RESPONSE"
fi

kill $CHROME_PID 2>/dev/null || true
pkill -9 chromium

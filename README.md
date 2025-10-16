# Browser-Use Automation with IEEE Xplore Integration

Browser-Useライブラリをベースにした、**IEEE Xplore論文自動検索・引用抽出システム**。

LLM駆動のブラウザ自動化により、学術論文の検索・メタデータ抽出・引用収集を完全自動化します。

---

## 主な機能

### ✅ IEEE Xplore統合
- **自動論文検索** - キーワードベースの論文検索
- **メタデータ抽出** - タイトル、著者、DOI、URLの自動取得
- **引用・抜粋記録** - 論文からの引用をセクション別に抽出
- **PDF本文解析** - PDFから各セクション（Abstract, Introduction等）を自動抽出
- **進捗表示** - リアルタイム検索進捗の可視化
- **対話的インターフェース** - チャット形式での検索・引用抽出操作

### ✅ マルチLLM対応
サポートするLLMプロバイダー：
- **Claude** (Anthropic)
- **OpenAI** (GPT-4o, GPT-4o-mini)
- **DeepSeek** (deepseek-chat, deepseek-coder) - OpenAI互換API
- **Google Gemini**
- **Groq**
- **OpenRouter**

### ✅ コンテナ対応
- **Podman/Docker** フルサポート
- **ヘッドレス/GUI** 両モード対応
- **X11転送** によるGUIアプリケーション実行

---

## クイックスタート

### 1. セットアップ

```bash
# リポジトリのクローン
git clone <repository-url>
cd browser-use-automation

# 依存関係のインストール（uv使用）
uv sync

# 環境変数の設定
cp .env.example .env
# .envファイルにAPI keyを設定
```

### 2. 基本的な使用方法

**論文検索（コマンドライン）:**

```bash
# デフォルト設定で検索
uv run python examples/ieee_paper_search.py

# カスタムクエリで検索
uv run python examples/ieee_paper_search.py -q "machine learning" -n 10

# 出力先を指定
uv run python examples/ieee_paper_search.py -q "deep learning" -o ./my_papers
```

**対話的インターフェース（推奨）:**

```bash
uv run python examples/ieee_chat_interface.py
```

対話モード内で使用可能なコマンド：
- `search <query> [max_results]` - 論文検索
- `extract <paper_number>` - 引用抽出
- `list` - 検索結果一覧
- `save [filename]` - JSON保存
- `quit` - 終了

**Podmanコンテナで実行:**

```bash
# コンテナビルド
podman-compose build

# 検索実行
podman run --rm \
  --env-file .env \
  -e LLM_PROVIDER=deepseek \
  -e HEADLESS=false \
  -e DISPLAY=:0 \
  -v /tmp/.X11-unix:/tmp/.X11-unix:ro \
  -v ./papers:/app/papers:z \
  --network host \
  localhost/browser-use-automation_ieee-search:latest \
  uv run python examples/ieee_paper_search.py -q "neural networks" -n 5
```

### 3. Pythonコードでの使用

```python
import asyncio
from browser_use.browser import BrowserSession
from browser_use.browser.profile import BrowserProfile
from browser_use.integrations.ieee_search import IEEESearchService

async def search_papers():
    # ブラウザセッション作成
    profile = BrowserProfile(headless=False)  # IEEE検索にはheadless=False推奨
    browser_session = BrowserSession(browser_profile=profile)
    await browser_session.start()

    # IEEE検索サービス初期化
    ieee_service = IEEESearchService()

    # 論文検索
    results = await ieee_service.search(
        query="machine learning security",
        max_results=10,
        browser_session=browser_session
    )

    # 結果表示
    for paper in results:
        print(f"Title: {paper['title']}")
        print(f"Authors: {', '.join(paper['authors'])}")
        print(f"URL: {paper['url']}\n")

    await browser_session.kill()

asyncio.run(search_papers())
```

---

## 詳細ドキュメント

**IEEE検索機能の詳細**: [`IEEE_SEARCH_README.md`](./IEEE_SEARCH_README.md)を参照してください。

以下の内容が含まれています：
- 全コマンドラインオプション
- 対話的インターフェースの詳細
- 引用抽出のAPI使用方法
- トラブルシューティング
- 技術詳細・アーキテクチャ

---

## 最近の改善

### 2025-01-16: EventBus APIバグ修正 & DeepSeekテスト追加

**修正内容:**
- **EventBus API不一致の修正** (`browser_use/integrations/ieee_search/service.py:360`)
  - `bubus` library (v1.5.6+) の正しいAPI（`.on()`）に更新
  - PDF ダウンロード機能が正常動作するように修正

- **DeepSeekテストケース追加** (`browser_use/llm/tests/test_chat_models.py`)
  - 通常テキスト応答テスト: `test_deepseek_ainvoke_normal()`
  - 構造化出力テスト: `test_deepseek_ainvoke_structured()`

**検証結果:**
- IEEE統合テスト: 4/4 passed
- Podmanコンテナ実行テスト: 成功
- PDF抽出機能: 正常動作（サブスクリプション論文は予想通りタイムアウト）

**実績:**
- "associative memory database" 検索: 3件の論文抽出成功
- "machine learning" 検索: 3件の論文抽出成功
- 引用抽出: Abstract・Introduction等のセクション抽出成功

---

## 環境変数

`.env`ファイルに以下を設定：

```bash
# LLMプロバイダー選択（claude, openai, deepseek, google, groq）
LLM_PROVIDER=deepseek

# API Keys
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
DEEPSEEK_API_KEY=sk-...
GOOGLE_API_KEY=...
GROQ_API_KEY=...

# ブラウザ設定
HEADLESS=false  # IEEE検索にはfalse推奨
```

---

## 技術スタック

- **Python 3.11+**
- **Browser-Use** - LLM駆動ブラウザ自動化ライブラリ
- **Chromium/Chrome** - CDP (Chrome DevTools Protocol) 経由制御
- **BeautifulSoup4** - HTML解析
- **PyPDF2** - PDF本文抽出
- **Podman/Docker** - コンテナ化実行環境
- **pytest** - テストフレームワーク

---

## 開発

### テスト実行

```bash
# CI用テスト実行
uv run pytest -vxs tests/ci

# 全テスト実行
uv run pytest -vxs tests/

# 特定のテスト
uv run pytest -vxs tests/ci/test_ieee_search.py
```

### コード品質チェック

```bash
# 型チェック
uv run pyright

# Linting & フォーマット
uv run ruff check --fix
uv run ruff format

# Pre-commit hooks
uv run pre-commit run --all-files
```

---

## アーキテクチャ

Browser-Useの**イベント駆動アーキテクチャ**をベースに構築：

- **Agent** (`browser_use/agent/service.py`) - タスク実行オーケストレーター
- **BrowserSession** (`browser_use/browser/session.py`) - CDP接続・ブラウザライフサイクル管理
- **IEEESearchService** (`browser_use/integrations/ieee_search/service.py`) - IEEE検索・引用抽出
- **EventBus** (`bubus`) - 各種Watchdog間の通信（Downloads, Popups, Security, DOM）

---

## トラブルシューティング

### IEEE XploreでBot検出される

**症状**: "Request Rejected" エラー

**解決方法**:
```bash
# ヘッドレスモードを無効化
export HEADLESS=false

# Xサーバーを確認
echo $DISPLAY  # :0 などが表示されるはず
```

### PDF抽出がタイムアウトする

**原因**: 論文がIEEE購読または機関アクセス制限付き

**解決方法**:
1. IEEE会員の場合: ブラウザでログイン後に実行
2. 機関ネットワーク経由で実行
3. オープンアクセス論文を検索対象にする

### Chromiumが見つからない

```bash
# Debian/Ubuntu
sudo apt install chromium chromium-driver

# Fedora/RHEL
sudo dnf install chromium
```

---

## ライセンス

本プロジェクトは [Browser-Use](https://github.com/browser-use/browser-use) をベースに構築されています。

---

## リンク

- **Browser-Use**: https://github.com/browser-use/browser-use
- **Browser-Use Docs**: https://docs.browser-use.com
- **DeepSeek API**: https://platform.deepseek.com/api-docs/

---

**開発**: Test-Driven Development (TDD) with Claude Code
**最終更新**: 2025-01-16

# IEEE Paper Search Tool

専用のIEEE Xplore論文検索ツール。複数のLLMプロバイダー（Claude、OpenAI、DeepSeek等）をサポートし、Podman/Dockerでコンテナ化されています。

## 特徴

✅ **IEEE Xplore自動検索** - キーワードで論文を自動検索
✅ **メタデータ抽出** - タイトル、著者、URLを自動抽出
✅ **マルチLLM対応** - Claude、OpenAI、DeepSeek、Google、Grokから選択可能
✅ **コンテナ化** - Podman/Dockerで簡単にデプロイ
✅ **JSON出力** - 検索結果をJSON形式で保存

## セットアップ

### 1. 環境変数の設定

`.env`ファイルを作成（`.env.example`をコピー）:

```bash
cp .env.example .env
```

`.env`ファイルを編集して、使用するLLMプロバイダーとAPIキーを設定:

```bash
# LLMプロバイダーを選択（claude, openai, deepseek, google, grok）
LLM_PROVIDER=claude

# 使用するプロバイダーのAPIキーを設定
ANTHROPIC_API_KEY=sk-ant-...  # Claude使用時
# OPENAI_API_KEY=sk-...       # OpenAI使用時
# DEEPSEEK_API_KEY=sk-...     # DeepSeek使用時
```

### 2. インストール

#### ローカル実行

```bash
# uvのインストール
curl -LsSf https://astral.sh/uv/install.sh | sh

# 依存関係のインストール
uv sync

# 仮想環境の有効化
source .venv/bin/activate
```

#### Podmanコンテナ

```bash
# コンテナイメージのビルド
podman build -t ieee-search -f Containerfile .

# コンテナの実行
podman-compose up -d
```

#### Docker

```bash
# コンテナイメージのビルド
docker build -t ieee-search -f Containerfile .

# コンテナの実行
docker-compose up -d
```

## 使用方法

### 基本的な使い方

```bash
# 論文検索の実行
uv run python examples/ieee_paper_search.py

# カスタムクエリで検索
SEARCH_QUERY="deep learning security" uv run python examples/ieee_paper_search.py
```

### Pythonコードでの使用

```python
import asyncio
from browser_use.browser import BrowserSession
from browser_use.browser.profile import BrowserProfile
from browser_use.integrations.ieee_search import IEEESearchService

async def search_papers():
    # ブラウザセッションの作成
    profile = BrowserProfile(headless=True)
    browser_session = BrowserSession(browser_profile=profile)
    await browser_session.start()

    # IEEE検索サービスの初期化
    ieee_service = IEEESearchService()

    # 論文検索
    results = await ieee_service.search(
        query="machine learning",
        max_results=10,
        browser_session=browser_session
    )

    # 結果の表示
    for paper in results:
        print(f"Title: {paper['title']}")
        print(f"Authors: {', '.join(paper['authors'])}")
        print(f"URL: {paper['url']}")
        print()

    await browser_session.kill()

asyncio.run(search_papers())
```

## 検索結果の保存

検索結果は自動的に`./papers/`ディレクトリにJSON形式で保存されます:

```json
{
  "query": "machine learning",
  "results": [
    {
      "title": "Deep Learning for Network Traffic Classification",
      "authors": ["John Smith", "Jane Doe"],
      "url": "https://ieeexplore.ieee.org/document/12345"
    }
  ],
  "count": 1
}
```

## LLMプロバイダーの切り替え

`.env`ファイルで`LLM_PROVIDER`を変更するだけ:

```bash
# Claudeを使用
LLM_PROVIDER=claude
ANTHROPIC_API_KEY=sk-ant-...

# OpenAIに切り替え
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-...

# DeepSeekに切り替え
LLM_PROVIDER=deepseek
DEEPSEEK_API_KEY=sk-...
```

## 開発者向け

### テストの実行

```bash
# IEEE検索テストの実行
uv run pytest -xvs tests/ci/test_ieee_search.py

# すべてのテストの実行
uv run pytest -xvs tests/ci/
```

### アーキテクチャ

- `browser_use/integrations/ieee_search/service.py` - 検索サービス本体
- `browser_use/integrations/ieee_search/llm_config.py` - LLM設定ヘルパー
- `tests/ci/test_ieee_search.py` - TDDテスト
- `examples/ieee_paper_search.py` - 使用例

### TDD開発プロセス

このプロジェクトはt-wada流TDD（テスト駆動開発）で構築されています:

1. **Red** - 失敗するテストを書く
2. **Green** - テストを通す最小限の実装
3. **Refactor** - リファクタリング
4. **Commit** - 小さくコミット

## トラブルシューティング

### Chromiumが見つからない

```bash
# Chromiumのインストール（Debian/Ubuntu）
sudo apt install chromium chromium-driver

# Chromiumのインストール（Fedora/RHEL）
sudo dnf install chromium
```

### APIキーエラー

`.env`ファイルが正しく設定されているか確認:

```bash
# .envファイルの確認
cat .env | grep API_KEY
```

## ライセンス

このツールはbrowser-useライブラリ上に構築されています。

## 貢献

Pull Requestを歓迎します！開発の際は:

1. テストを書く（t-wada流TDD）
2. `uv run pytest`でテストを実行
3. `uv run ruff check --fix`でフォーマット
4. コミットメッセージは明確に

---

**開発:** t-wada流TDD with Claude Code
**日付:** 2025-10-16

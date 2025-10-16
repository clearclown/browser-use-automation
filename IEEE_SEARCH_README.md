# IEEE Paper Search Tool

専用のIEEE Xplore論文検索ツール。複数のLLMプロバイダー（Claude、OpenAI、DeepSeek等）をサポートし、Podman/Dockerでコンテナ化されています。

## 特徴

✅ **IEEE Xplore自動検索** - キーワードで論文を自動検索
✅ **メタデータ抽出** - タイトル、著者、URL、DOIを自動抽出
✅ **引用・抜粋記録** - 論文の引用をセクション名・ページ番号付きで保存
✅ **PDFテキスト抽出** - PDF本文から各セクション（Introduction、Methodology等）を自動抽出
✅ **進捗状況表示** - リアルタイムで検索進捗を可視化
✅ **対話的インターフェース** - チャット形式で検索・引用抽出を操作
✅ **マルチLLM対応** - Claude、OpenAI、DeepSeek、Google、Grokから選択可能
✅ **コンテナ化** - Podman/Dockerで簡単にデプロイ
✅ **JSON出力** - 検索結果と引用をJSON形式で保存

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
# 論文検索の実行（ブラウザが表示されます）
DISPLAY=:0 uv run python examples/ieee_paper_search.py

# カスタムクエリで検索
SEARCH_QUERY="deep learning security" DISPLAY=:0 uv run python examples/ieee_paper_search.py

# ヘッドレスモードで実行（IEEE Xploreがブロックする可能性あり）
HEADLESS=true uv run python examples/ieee_paper_search.py
```

**注意**: IEEE Xploreはヘッドレスブラウザをブロックするため、デフォルトではブラウザウィンドウが表示されます。`DISPLAY=:0` を指定してください。

### 対話的インターフェース（チャット形式）

```bash
# 対話的に検索・引用抽出を実行
uv run python examples/ieee_chat_interface.py

# 使用可能なコマンド:
#   search <query> [max_results]  - 論文検索
#   extract <paper_number> [sections] - 引用抽出
#   list - 検索結果一覧
#   citations - 収集した引用一覧
#   save [filename] - JSONファイルに保存
#   quit - 終了
```

### 全機能デモ

```bash
# 検索・引用・進捗表示の全機能デモ
uv run python examples/ieee_comprehensive_example.py
```

### Pythonコードでの使用

#### 基本的な検索

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

    await browser_session.kill()

asyncio.run(search_papers())
```

#### 進捗表示付き検索

```python
async def search_with_progress():
    # 進捗コールバック関数
    def progress(status: str, current: int, total: int):
        print(f"Progress: {status} [{current}/{total}]")

    ieee_service = IEEESearchService()
    browser_session = BrowserSession(browser_profile=BrowserProfile(headless=True))
    await browser_session.start()

    # 進捗表示付き検索
    results = await ieee_service.search(
        query="deep learning",
        max_results=5,
        browser_session=browser_session,
        progress_callback=progress  # 進捗コールバックを渡す
    )

    await browser_session.kill()
```

#### 引用・抜粋の抽出

```python
async def extract_citations():
    ieee_service = IEEESearchService()
    browser_session = BrowserSession(browser_profile=BrowserProfile(headless=True))
    await browser_session.start()

    # 論文から引用を抽出
    citations = await ieee_service.extract_citations(
        paper_url="https://ieeexplore.ieee.org/document/12345",
        sections=["Abstract", "Introduction", "Methodology"],
        browser_session=browser_session
    )

    # 引用の表示
    for citation in citations:
        print(f"Section: {citation.section}")
        print(f"Text: {citation.text}")
        print(f"Paper: {citation.paper_title}")
        print(f"URL: {citation.paper_url}")
        print(f"Authors: {', '.join(citation.authors)}")
        print()

    await browser_session.kill()
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

**コアモジュール:**
- `browser_use/integrations/ieee_search/service.py` - 検索・引用抽出サービス本体
- `browser_use/integrations/ieee_search/views.py` - データモデル（Citation, PaperMetadata, SearchProgress）
- `browser_use/integrations/ieee_search/llm_config.py` - LLM設定ヘルパー

**テスト:**
- `tests/ci/test_ieee_search.py` - TDDテスト（4テストケース、全てPass）
  - `TestIEEESearchBasicFunctionality` - 基本検索
  - `TestCitationExtraction` - 引用抽出
  - `TestProgressTracking` - 進捗追跡

**使用例:**
- `examples/ieee_paper_search.py` - 基本的な論文検索
- `examples/ieee_chat_interface.py` - 対話的インターフェース
- `examples/ieee_comprehensive_example.py` - 全機能デモ

### TDD開発プロセス

このプロジェクトはt-wada流TDD（テスト駆動開発）で構築されています:

1. **Red** - 失敗するテストを書く
2. **Green** - テストを通す最小限の実装
3. **Refactor** - リファクタリング
4. **Commit** - 小さくコミット

## トラブルシューティング

### IEEE Xploreアクセスがブロックされる

**症状**: "Request Rejected" エラーが表示される

**原因**: IEEE Xploreがヘッドレスブラウザを検出してブロックしています。

**解決方法**:
1. デフォルト設定（headless=False）を使用する:
   ```bash
   DISPLAY=:0 uv run python examples/ieee_paper_search.py
   ```
2. Xサーバーが起動していることを確認:
   ```bash
   # Linuxの場合
   echo $DISPLAY  # :0 などが表示されるはず
   ```

### Chromiumが見つからない

```bash
# Chromiumのインストール（Debian/Ubuntu）
sudo apt install chromium chromium-driver

# Chromiumのインストール（Fedora/RHEL）
sudo dnf install chromium
```

### 検索結果が0件

**原因**: HTMLパースのタイミング問題の可能性

**解決方法**:
- `service.py` の待機時間を増やす（現在5秒）
- ブラウザウィンドウを確認してページが完全に読み込まれているか確認

### PDF抽出が失敗する

**症状**: "This paper may require IEEE subscription or institutional access" というメッセージが表示される

**原因**: 論文のPDFダウンロードにIEEE契約や機関アクセスが必要

**解決方法**:
1. IEEE会員の場合: ブラウザでIEEE Xploreにログインしてから実行
2. 機関アクセスの場合: 大学・企業ネットワーク経由で実行
3. オープンアクセス論文を検索対象にする

**注意**:
- 古い論文や一部の論文はPDFが利用できない場合があります
- その場合はHTML版のAbstractのみが抽出されます
- `use_pdf=False` を設定することでPDF抽出をスキップできます

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

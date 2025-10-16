# Browser-Use Automation with IEEE Xplore Integration

Browser-Useライブラリをベースにした、**IEEE Xplore論文自動検索・引用抽出システム**。

LLM駆動のブラウザ自動化により、学術論文の検索・メタデータ抽出・引用収集を完全自動化します。

---

## 📋 目次

- [主な機能](#主な機能)
- [システム要件](#システム要件)
- [詳細セットアップ手順](#詳細セットアップ手順)
- [基本的な使用方法](#基本的な使用方法)
- [トラブルシューティング](#トラブルシューティング)
- [開発者向け情報](#開発者向け情報)

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

## システム要件

### 必須要件

| 項目 | 最小バージョン | 推奨バージョン | 確認コマンド |
|------|--------------|--------------|------------|
| **OS** | Linux (Ubuntu 20.04+, Fedora 35+) | Ubuntu 22.04+ | `lsb_release -a` |
| **Python** | 3.11 | 3.13 | `python3 --version` |
| **uv** | 0.4.0+ | 最新版 | `uv --version` |
| **Chromium** | 90+ | 最新版 | `chromium --version` |
| **X Server** | 任意 | Xorg | `echo $DISPLAY` |

### オプション要件（コンテナ使用時）

| 項目 | バージョン | 確認コマンド |
|------|-----------|------------|
| **Podman** | 3.0+ | `podman --version` |
| **Docker** | 20.10+ | `docker --version` |

---

## 詳細セットアップ手順

### ステップ1: システム依存関係のインストール

#### Ubuntu/Debian系

```bash
# システムパッケージ更新
sudo apt update && sudo apt upgrade -y

# Python 3.13インストール（必要な場合）
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.13 python3.13-venv python3.13-dev -y

# Chromiumインストール
sudo apt install chromium chromium-driver -y

# 追加ツール
sudo apt install git curl -y
```

#### Fedora/RHEL系

```bash
# システムパッケージ更新
sudo dnf update -y

# Python 3.13インストール
sudo dnf install python3.13 python3.13-devel -y

# Chromiumインストール
sudo dnf install chromium -y

# 追加ツール
sudo dnf install git curl -y
```

### ステップ2: uv (パッケージマネージャー) インストール

```bash
# uvインストール
curl -LsSf https://astral.sh/uv/install.sh | sh

# シェル設定を再読み込み
source $HOME/.cargo/env

# インストール確認
uv --version
# 出力例: uv 0.9.3
```

### ステップ3: プロジェクトのクローンとセットアップ

```bash
# プロジェクトのクローン
git clone <repository-url>
cd browser-use-automation

# 依存関係のインストール（初回は数分かかります）
uv sync

# インストール確認
uv run python -c "from browser_use.integrations.ieee_search import IEEESearchService; print('✓ Setup successful')"
```

**期待される出力**:
```
✓ Setup successful
```

### ステップ4: 環境変数の設定

```bash
# .envファイル作成
cp .env.example .env

# .envファイルを編集（任意のエディタで開く）
nano .env
# または
vim .env
# または
code .env  # VS Code使用時
```

**最小限の設定例** (`.env`):

```bash
# ブラウザ設定
HEADLESS=false  # IEEE検索には必須: falseに設定

# ログ設定
BROWSER_USE_LOGGING_LEVEL=info
BROWSER_USE_DEBUG_LOG_FILE=debug.log
BROWSER_USE_INFO_LOG_FILE=info.log

# X Server設定（自動検出されるが、明示的に設定も可能）
DISPLAY=:0
```

**LLM使用時の追加設定** (対話的インターフェース使用時):

```bash
# LLMプロバイダー選択
LLM_PROVIDER=deepseek  # または claude, openai, google, groq

# API Keys（使用するプロバイダーのみ設定）
DEEPSEEK_API_KEY=sk-...
# ANTHROPIC_API_KEY=sk-ant-...
# OPENAI_API_KEY=sk-...
# GOOGLE_API_KEY=...
# GROQ_API_KEY=...
```

### ステップ5: 動作確認

#### 5-1. Chromium起動確認

```bash
# X Serverが起動しているか確認
echo $DISPLAY
# 出力例: :0 または :1（空の場合は設定が必要）

# Chromiumを手動起動してテスト
chromium --version
chromium --headless --disable-gpu --dump-dom https://example.com | head -5
```

**期待される出力**: HTMLの一部が表示される

#### 5-2. 簡単な検索テスト

```bash
# 1件だけ検索してテスト（30秒程度）
uv run python examples/ieee_paper_search.py -q "test" -n 1 -o /tmp/test_papers
```

**期待される出力**:
```
INFO     [__main__] 🚀 IEEE Paper Search Tool
INFO     [__main__] 🔍 Starting IEEE paper search for: "test"
INFO     [__main__] 🌐 Browser session started
INFO     [service] ✅ Found 1 papers
INFO     [__main__] 💾 Results saved to: /tmp/test_papers/search_results_test.json
INFO     [__main__] 🔚 Browser session closed
```

---

## 基本的な使用方法

### 方法1: コマンドライン論文検索（最もシンプル）

```bash
# デフォルト設定で検索
uv run python examples/ieee_paper_search.py

# カスタムクエリで検索
uv run python examples/ieee_paper_search.py -q "machine learning" -n 10

# 出力先を指定
uv run python examples/ieee_paper_search.py -q "deep learning" -o ./my_papers

# ヘルプ表示
uv run python examples/ieee_paper_search.py --help
```

**コマンドラインオプション**:

| オプション | 短縮形 | 説明 | デフォルト |
|-----------|-------|------|-----------|
| `--query` | `-q` | 検索クエリ | `machine learning cybersecurity` |
| `--max-results` | `-n` | 取得する論文数 | `5` |
| `--headless` | - | ヘッドレスモード | `False` |
| `--output` | `-o` | 出力ディレクトリ | `./papers` |

### 方法2: 対話的インターフェース（推奨）

```bash
# 対話モード起動
uv run python examples/ieee_chat_interface.py
```

**対話モード内のコマンド**:

| コマンド | 説明 | 例 |
|---------|------|-----|
| `search <query> [max_results]` | 論文検索 | `search deep learning 5` |
| `extract <paper_number> [sections]` | 引用抽出 | `extract 1 Abstract Introduction` |
| `list` | 検索結果一覧 | `list` |
| `citations` | 収集した引用一覧 | `citations` |
| `save [filename]` | JSONファイルに保存 | `save my_citations.json` |
| `quit` または `exit` | 終了 | `quit` |

### 方法3: Pythonコードで直接使用

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

### 方法4: Podman/Dockerコンテナで実行

```bash
# コンテナビルド（初回のみ、10分程度）
podman-compose build
# または
docker-compose build

# 検索実行（X11転送でGUI表示）
podman run --rm \
  --env-file .env \
  -e HEADLESS=false \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix:ro \
  -v ./papers:/app/papers:z \
  --network host \
  localhost/browser-use-automation_ieee-search:latest \
  uv run python examples/ieee_paper_search.py -q "neural networks" -n 5
```

---

## トラブルシューティング

### 問題1: `uv: command not found`

**原因**: uvがインストールされていない、またはPATHが通っていない

**解決方法**:
```bash
# uvインストール
curl -LsSf https://astral.sh/uv/install.sh | sh

# PATHを通す
echo 'source $HOME/.cargo/env' >> ~/.bashrc
source ~/.bashrc

# 確認
uv --version
```

### 問題2: `ModuleNotFoundError: No module named 'browser_use'`

**原因**: 依存関係がインストールされていない

**解決方法**:
```bash
# プロジェクトディレクトリで実行
cd /path/to/browser-use-automation

# 依存関係を再インストール
uv sync

# 仮想環境が正しくアクティベートされているか確認
uv run python -c "import browser_use; print(browser_use.__file__)"
```

### 問題3: `Chromium not found` または `Browser initialization failed`

**原因**: Chromiumがインストールされていない、またはPATHが通っていない

**解決方法**:
```bash
# Chromiumのインストール確認
which chromium
chromium --version

# インストールされていない場合
# Ubuntu/Debian
sudo apt install chromium chromium-driver -y

# Fedora/RHEL
sudo dnf install chromium -y

# 環境変数で明示的に指定（.env）
echo 'CHROME_BIN=/usr/bin/chromium' >> .env
echo 'CHROME_PATH=/usr/bin/chromium' >> .env
```

### 問題4: `Request Rejected` エラー (IEEE Xploreのbot検出)

**症状**: IEEE Xploreに接続できず"Request Rejected"エラーが表示される

**原因**: ヘッドレスモードでbot検出を受けている

**解決方法**:
```bash
# .envファイルを編集
nano .env

# HEADLESS=false に設定（必須）
HEADLESS=false

# X Serverが起動しているか確認
echo $DISPLAY
# :0 などが表示されるはず

# 表示されない場合、X Serverを起動するか環境変数を設定
export DISPLAY=:0
```

### 問題5: `PDF download timed out`

**症状**: PDF抽出時に「PDF download timed out after 30 seconds」メッセージ

**原因**: 論文がIEEE購読または機関アクセス制限付き（正常な動作）

**解決方法**:
```
これは予想される動作です。
- IEEE会員の場合: ブラウザでIEEE Xploreにログイン後に実行
- 機関ネットワーク経由で実行
- オープンアクセス論文を検索対象にする
- Abstractのみの抽出は問題なく動作します
```

### 問題6: `DISPLAY environment variable not set`

**原因**: X Serverが起動していない、またはDISPLAY環境変数が設定されていない

**解決方法**:
```bash
# 現在のDISPLAY確認
echo $DISPLAY

# 設定されていない場合
export DISPLAY=:0

# または.envに追加
echo 'DISPLAY=:0' >> .env

# X Serverが起動しているか確認（GUI環境の場合）
ps aux | grep X
```

### 問題7: Permission denied エラー（コンテナ使用時）

**症状**: `Permission denied` when accessing `/app/papers`

**解決方法**:
```bash
# SELinux有効時（Fedora/RHEL）
# -v オプションに :z を追加
podman run --rm \
  -v ./papers:/app/papers:z \
  ...

# または papers ディレクトリの権限を変更
chmod 777 ./papers
```

### 問題8: 検索結果が0件

**原因**: 検索クエリが具体的すぎる、またはHTML解析のタイミング問題

**解決方法**:
```bash
# より一般的なクエリで試す
uv run python examples/ieee_paper_search.py -q "machine learning" -n 5

# ブラウザウィンドウを確認（HEADLESS=false時）
# ページが完全に読み込まれているか確認

# デバッグログを確認
cat debug.log | grep "Found.*papers"
```

---

## 詳細ドキュメント

### IEEE検索機能の詳細

**[`IEEE_SEARCH_README.md`](./IEEE_SEARCH_README.md)** を参照してください。

以下の内容が含まれています：
- 全コマンドラインオプション詳細
- 対話的インターフェースの完全ガイド
- 引用抽出のAPI使用方法
- PDF抽出の仕組み
- 技術詳細・アーキテクチャ

---

## 環境変数リファレンス

### 必須環境変数

```bash
# ブラウザ設定（必須）
HEADLESS=false  # IEEE検索にはfalse必須（bot検出回避）
```

### 推奨環境変数

```bash
# ログ設定
BROWSER_USE_LOGGING_LEVEL=info  # debug, info, warning, error
BROWSER_USE_DEBUG_LOG_FILE=debug.log
BROWSER_USE_INFO_LOG_FILE=info.log

# Display設定（自動検出されるが、明示的設定も可能）
DISPLAY=:0

# Chromiumパス（自動検出されるが、カスタムパスの場合）
CHROME_BIN=/usr/bin/chromium
CHROME_PATH=/usr/bin/chromium
```

### LLM使用時の環境変数（対話的インターフェース用）

```bash
# LLMプロバイダー選択
LLM_PROVIDER=deepseek  # または claude, openai, google, groq

# API Keys（使用するプロバイダーのみ設定）
DEEPSEEK_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
GOOGLE_API_KEY=...
GROQ_API_KEY=...
```

---

## 出力ファイル

### 検索結果JSON

**ファイル名**: `./papers/search_results_<query>.json`

**形式**:
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

### 引用データJSON

**ファイル名**: `./papers/citations.json` または指定したファイル名

**形式**:
```json
[
  {
    "text": "This paper presents...",
    "paper_title": "Deep Learning for Network Traffic Classification",
    "paper_url": "https://ieeexplore.ieee.org/document/12345",
    "section": "Abstract",
    "authors": ["John Smith", "Jane Doe"],
    "page_number": null
  }
]
```

---

## 開発者向け情報

### テスト実行

```bash
# CI用テスト実行
uv run pytest -vxs tests/ci

# 全テスト実行
uv run pytest -vxs tests/

# 特定のテスト
uv run pytest -vxs tests/ci/test_ieee_search.py

# カバレッジ付き
uv run pytest --cov=browser_use tests/
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

### アーキテクチャ

Browser-Useの**イベント駆動アーキテクチャ**をベースに構築：

- **Agent** (`browser_use/agent/service.py`) - タスク実行オーケストレーター
- **BrowserSession** (`browser_use/browser/session.py`) - CDP接続・ブラウザライフサイクル管理
- **IEEESearchService** (`browser_use/integrations/ieee_search/service.py`) - IEEE検索・引用抽出
- **EventBus** (`bubus`) - 各種Watchdog間の通信（Downloads, Popups, Security, DOM）

---

## 技術スタック

- **Python 3.11+** (推奨: 3.13)
- **Browser-Use** - LLM駆動ブラウザ自動化ライブラリ
- **Chromium/Chrome** - CDP (Chrome DevTools Protocol) 経由制御
- **BeautifulSoup4** - HTML解析
- **PyPDF2** - PDF本文抽出
- **Podman/Docker** - コンテナ化実行環境
- **pytest** - テストフレームワーク

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

## FAQ（よくある質問）

### Q1: LLM APIキーは必須ですか？

**A**: いいえ、**基本的な論文検索にはLLM APIキーは不要です**。
- `examples/ieee_paper_search.py`: LLM不要（キーワード検索のみ）
- `examples/ieee_chat_interface.py`: LLM必要（対話的インターフェース）

### Q2: ヘッドレスモードで実行できますか？

**A**: IEEE Xplore検索では**ヘッドレスモード非推奨**です。
- IEEE XploreはヘッドレスブラウザをBot検出する可能性が高い
- `HEADLESS=false` の設定を推奨
- X Serverが必要（GUIまたはXvfb）

### Q3: コンテナなしで実行できますか？

**A**: はい、**ローカル環境で直接実行可能**です。
- Python 3.11+、uv、Chromiumがインストールされていれば実行可能
- コンテナは便利ですが必須ではありません

### Q4: 大量の論文を一度に検索できますか？

**A**: はい、`--max-results` オプションで指定可能です。
```bash
uv run python examples/ieee_paper_search.py -q "machine learning" -n 100
```
ただし、IEEE Xploreのrate limitに注意してください。

### Q5: 検索結果をどこで確認できますか？

**A**: デフォルトでは `./papers/` ディレクトリにJSON形式で保存されます。
- ファイル名: `search_results_<query>.json`
- `-o` オプションで出力先を変更可能

---

## ライセンス

本プロジェクトは [Browser-Use](https://github.com/browser-use/browser-use) をベースに構築されています。

---

## リンク

- **Browser-Use**: https://github.com/browser-use/browser-use
- **Browser-Use Docs**: https://docs.browser-use.com
- **DeepSeek API**: https://platform.deepseek.com/api-docs/
- **IEEE Xplore**: https://ieeexplore.ieee.org/

---

## サポート

問題が発生した場合：

1. **ログを確認**: `debug.log` と `info.log` を確認
2. **トラブルシューティングセクション**: 上記の問題解決方法を確認
3. **Issue報告**: GitHub Issuesで報告（再現手順を含めて）

---

**開発**: Test-Driven Development (TDD) with Claude Code
**最終更新**: 2025-10-16

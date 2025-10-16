# IEEE Paper Search Tool

IEEE Xplore専用の論文検索・引用抽出ツール。コマンドライン引数で柔軟に操作可能。

## 特徴

✅ **IEEE Xplore自動検索** - キーワードで論文を自動検索
✅ **メタデータ抽出** - タイトル、著者、URL、DOIを自動抽出
✅ **引用・抜粋記録** - 論文の引用をセクション名付きで保存
✅ **PDFテキスト抽出** - PDF本文から各セクション（Introduction、Methodology等）を自動抽出
✅ **進捗状況表示** - リアルタイムで検索進捗を可視化
✅ **対話的インターフェース** - チャット形式で検索・引用抽出を操作
✅ **コマンドライン対応** - 引数で検索クエリや結果数を指定可能
✅ **JSON出力** - 検索結果と引用をJSON形式で保存

---

## セットアップ

### 1. 依存関係のインストール

```bash
# uvのインストール
curl -LsSf https://astral.sh/uv/install.sh | sh

# 依存関係のインストール
uv sync

# 仮想環境の有効化
source .venv/bin/activate
```

### 2. 環境確認

```bash
# Chromiumのインストール（必要な場合）
# Debian/Ubuntu
sudo apt install chromium chromium-driver

# Fedora/RHEL
sudo dnf install chromium

# Xサーバーが起動していることを確認（GUI必要）
echo $DISPLAY  # :0 などが表示されればOK
```

---

## 使用方法

### 📚 基本的な論文検索

最もシンプルな使い方：

```bash
# デフォルト設定で検索（クエリ: "machine learning cybersecurity", 5件）
uv run python examples/ieee_paper_search.py

# カスタムクエリで検索
uv run python examples/ieee_paper_search.py --query "deep learning"

# 短縮オプション
uv run python examples/ieee_paper_search.py -q "neural networks" -n 10
```

**利用可能なオプション:**

| オプション | 短縮 | 説明 | デフォルト |
|-----------|------|------|-----------|
| `--query` | `-q` | 検索クエリ | `machine learning cybersecurity` |
| `--max-results` | `-n` | 取得する論文数 | `5` |
| `--headless` | - | ヘッドレスモード（IEEEでブロックされる可能性あり） | `False` |
| `--output` | `-o` | 出力ディレクトリ | `./papers` |

**使用例:**

```bash
# 10件の論文を検索
uv run python examples/ieee_paper_search.py -q "machine learning security" -n 10

# 出力先を指定
uv run python examples/ieee_paper_search.py -q "deep learning" -o ./my_papers

# ヘルプを表示
uv run python examples/ieee_paper_search.py --help
```

---

### 💬 対話的インターフェース（推奨）

チャット形式で検索・引用抽出を実行：

```bash
# 対話的モードを起動
uv run python examples/ieee_chat_interface.py

# 出力先を指定して起動
uv run python examples/ieee_chat_interface.py -o ./my_citations
```

**対話モード内で使用できるコマンド:**

| コマンド | 説明 | 例 |
|---------|------|-----|
| `search <query> [max_results]` | 論文検索 | `search deep learning 5` |
| `extract <paper_number> [sections]` | 引用抽出 | `extract 1 Abstract Introduction` |
| `list` | 検索結果一覧 | `list` |
| `citations` | 収集した引用一覧 | `citations` |
| `save [filename]` | JSONファイルに保存 | `save my_citations.json` |
| `quit` / `exit` | 終了 | `quit` |

**実行例:**

```
🔎 > search neural networks 3
📚 Searching for papers...
✅ Found 3 papers

🔎 > extract 1 Abstract Introduction
📄 Extracting citations...
✅ Extracted 2 citations

🔎 > save results.json
💾 Saved 2 citations to: ./papers/results.json

🔎 > quit
```

---

### 🎯 全機能デモ

検索・引用抽出・進捗表示のすべてを一度に実行：

```bash
# デフォルト設定でデモ実行
uv run python examples/ieee_comprehensive_example.py

# カスタム設定
uv run python examples/ieee_comprehensive_example.py -q "deep learning" -n 5 -o ./results
```

**オプション:**

| オプション | 短縮 | 説明 | デフォルト |
|-----------|------|------|-----------|
| `--query` | `-q` | 検索クエリ | `machine learning security` |
| `--max-results` | `-n` | 取得する論文数 | `3` |
| `--headless` | - | ヘッドレスモード | `False` |
| `--output` | `-o` | 出力ディレクトリ | `./papers` |

---

## Pythonコードでの使用

### 基本的な検索

```python
import asyncio
from browser_use.browser import BrowserSession
from browser_use.browser.profile import BrowserProfile
from browser_use.integrations.ieee_search import IEEESearchService

async def search_papers():
    # ブラウザセッションの作成
    profile = BrowserProfile(headless=False)  # IEEEはheadless=Falseを推奨
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
        print(f"URL: {paper['url']}\n")

    await browser_session.kill()

asyncio.run(search_papers())
```

### 進捗表示付き検索

```python
async def search_with_progress():
    def progress(status: str, current: int, total: int):
        print(f"Progress: {status} [{current}/{total}]")

    ieee_service = IEEESearchService()
    browser_session = BrowserSession(browser_profile=BrowserProfile(headless=False))
    await browser_session.start()

    results = await ieee_service.search(
        query="deep learning",
        max_results=5,
        browser_session=browser_session,
        progress_callback=progress  # 進捗コールバック
    )

    await browser_session.kill()
```

### 引用・抜粋の抽出（PDF対応）

```python
async def extract_citations():
    ieee_service = IEEESearchService()
    browser_session = BrowserSession(browser_profile=BrowserProfile(headless=False))
    await browser_session.start()

    # 論文から引用を抽出（PDFから本文抽出）
    citations = await ieee_service.extract_citations(
        paper_url="https://ieeexplore.ieee.org/document/12345",
        sections=["Abstract", "Introduction", "Methodology"],
        browser_session=browser_session,
        use_pdf=True  # PDF本文からセクション抽出
    )

    # 引用の表示
    for citation in citations:
        print(f"Section: {citation.section}")
        print(f"Text: {citation.text[:200]}...")
        print(f"Paper: {citation.paper_title}")
        print(f"Authors: {', '.join(citation.authors)}\n")

    await browser_session.kill()
```

---

## 出力形式

### 検索結果（JSON）

`./papers/search_results_<query>.json`:

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

### 引用データ（JSON）

`./papers/citations.json`:

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

## トラブルシューティング

### IEEE Xploreアクセスがブロックされる

**症状**: "Request Rejected" エラーが表示される

**解決方法**:
1. ヘッドレスモードを無効化（デフォルトは無効）
2. Xサーバーが起動していることを確認:
   ```bash
   echo $DISPLAY  # :0 などが表示されるはず
   ```

### Chromiumが見つからない

```bash
# Debian/Ubuntu
sudo apt install chromium chromium-driver

# Fedora/RHEL
sudo dnf install chromium
```

### 検索結果が0件

**原因**: HTMLパースのタイミング問題

**解決方法**:
- ブラウザウィンドウを確認してページが完全に読み込まれているか確認
- `service.py` の待機時間を増やす（現在5秒）

### PDF抽出が失敗する

**症状**: "This paper may require IEEE subscription" メッセージ

**原因**: 論文のPDFダウンロードにIEEE契約や機関アクセスが必要

**解決方法**:
1. IEEE会員の場合: ブラウザでIEEE Xploreにログインしてから実行
2. 機関アクセスの場合: 大学・企業ネットワーク経由で実行
3. オープンアクセス論文を検索対象にする
4. `use_pdf=False` でPDF抽出をスキップ（HTML版Abstractのみ）

---

## 技術詳細

### アーキテクチャ

**コアモジュール:**
- `browser_use/integrations/ieee_search/service.py` - 検索・引用抽出サービス
- `browser_use/integrations/ieee_search/views.py` - データモデル（Citation, PaperMetadata）

**コマンドラインツール:**
- `examples/ieee_paper_search.py` - 基本的な論文検索
- `examples/ieee_chat_interface.py` - 対話的インターフェース
- `examples/ieee_comprehensive_example.py` - 全機能デモ

### 動作環境

- Python 3.11+
- Chromium/Chrome
- Xサーバー（Linux GUI環境）

---

## ライセンス

このツールはbrowser-useライブラリ上に構築されています。

---

**開発:** TDD (Test-Driven Development) with Claude Code
**日付:** 2025-01-16

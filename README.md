# Browser-Use Automation Research System

PRISMA 2020準拠の自動化文献調査システム + マルチソース検索

## 概要

LLM駆動のブラウザ自動化とAPI検索を組み合わせた研究支援システム。

**主な機能:**
- PRISMA準拠の体系的文献レビュー
- マルチデータベース検索（arXiv, IEEE, J-STAGE, 政府文書）
- プラグイン型情報源システム（国際機関、シンクタンク、人権団体）
- 落合陽一式レポート生成
- Claude Agent SDK統合

---

## クイックスタート

### 1. 環境構築

```bash
# クローン
git clone <repository-url>
cd browser-use-automation

# 依存関係インストール
uv sync

# 環境変数設定
cp .env.example .env
```

### 2. 必須設定 (.env)

```bash
# ===== LLM設定（必須）=====
LLM_PROVIDER=openai  # openai, claude, deepseek, google, groq から選択

# 使用するプロバイダーのAPIキーを設定
OPENAI_API_KEY=sk-...
# ANTHROPIC_API_KEY=sk-ant-...
# DEEPSEEK_API_KEY=sk-...
# GOOGLE_API_KEY=...
# GROQ_API_KEY=...

# ===== Perplexity API（マルチソース検索用）=====
# UNHCR, Amnesty, シンクタンク等の検索に必要
PERPLEXITY_API_KEY=pplx-...
```

### 3. 実行

```bash
# PRISMA研究システム（フル版）
uv run python -m automated_research.main

# 軽量版（ブラウザ不使用）
uv run python -c "
from automated_research_lightweight import HybridResearchSystem
# ... (使用例は下記参照)
"
```

---

## プロジェクト構造

```
browser-use-automation/
├── automated_research/              # PRISMA準拠フル研究システム
│   ├── main.py                      # メインエントリーポイント
│   ├── arxiv_search.py              # arXiv API検索
│   ├── jstage_search.py             # J-STAGE検索
│   ├── ieee_automated_search.py     # IEEE Xplore検索
│   ├── government_documents_search.py
│   ├── prisma_search_strategy.py    # PRISMA検索戦略
│   ├── prisma_flow_diagram.py       # PRISMAフロー図生成
│   ├── ochiai_report_generator.py   # 落合式レポート
│   ├── screening_criteria.py        # スクリーニング基準
│   ├── risk_of_bias.py              # Cochrane RoB 2評価
│   ├── multiple_reviewers.py        # 複数レビュアー対応
│   └── llm_provider.py              # マルチLLMプロバイダー
│
├── automated_research_lightweight/  # 軽量版（API専用）
│   ├── hybrid_system.py             # 統合検索システム
│   ├── arxiv_searcher.py
│   ├── ieee_searcher.py
│   ├── semantic_scholar_searcher.py
│   └── sources/                     # プラグイン型情報源
│       ├── base.py                  # BaseSource, SearchResult
│       ├── registry.py              # SourceRegistry
│       ├── perplexity.py            # Perplexity API
│       └── organizations.py         # 国際機関・シンクタンク等
│
├── browser_use/                     # Browser-Use コアライブラリ
├── result/                          # 実行結果出力先（.gitignore）
└── .env.example                     # 環境変数テンプレート
```

---

## 出力先

すべての実行結果は `result/` ディレクトリに保存されます（`.gitignore`で除外）:

```
result/
├── automated_research/              # フル版の出力
│   ├── data/                        # 研究情報、検索戦略
│   ├── reports/                     # 個別・統合レポート
│   └── logs/
└── automated_research_lightweight/  # 軽量版の出力
    ├── result_*.json
    └── summary_*.md
```

---

## 使用方法

### 方法1: PRISMA研究システム（フル版）

```bash
# 対話型（デフォルト）
uv run python -m automated_research.main

# 非対話型
uv run python -m automated_research.main --non-interactive \
  --research-topic "Machine Learning" --max-papers 20

# LLMプロバイダー指定
uv run python -m automated_research.main --provider claude
uv run python -m automated_research.main --provider deepseek --model deepseek-chat

# ヘッドレスモード
uv run python -m automated_research.main --headless
```

### 方法2: Streamlit Web UI

```bash
./run_streamlit.sh
# http://localhost:8501
```

### 方法3: 軽量版（API専用、ブラウザ不使用）

```python
import asyncio
from langchain_openai import ChatOpenAI
from automated_research_lightweight import HybridResearchSystem

async def main():
    llm = ChatOpenAI(model="gpt-4o-mini")
    system = HybridResearchSystem(llm=llm, max_papers=10)

    results = await system.search("machine learning healthcare")
    summary = await system.generate_summary(results)
    print(summary)

asyncio.run(main())
```

### 方法4: プラグイン型ソース検索

```python
import asyncio
from automated_research_lightweight.sources import (
    SourceRegistry, PerplexitySource, UNHCRSource, AmnestySource,
    get_all_sources, SourceCategory
)

async def main():
    registry = SourceRegistry()

    # 個別登録
    registry.register(PerplexitySource(api_key="pplx-..."))
    registry.register(UNHCRSource(perplexity_api_key="pplx-..."))
    registry.register(AmnestySource(perplexity_api_key="pplx-..."))

    # または全ソース一括登録
    # for source in get_all_sources(api_key="pplx-..."):
    #     registry.register(source)

    # 検索
    results = await registry.search("refugee crisis")

    # 特定ソースのみ
    results = await registry.search("human rights", source_ids=["amnesty", "hrw"])

    # カテゴリで検索
    results = await registry.search_by_category(
        "climate migration",
        SourceCategory.INTERNATIONAL_ORG
    )

asyncio.run(main())
```

#### 利用可能ソース（19種）

| カテゴリ | ソース |
|---------|--------|
| **国際機関** | UNHCR, IOM, WHO, World Bank, OECD, UN |
| **人権団体** | Amnesty International, HRW, ICRC |
| **シンクタンク** | Brookings, RAND, CFR, Chatham House, Carnegie |
| **政府** | US Gov, EU, UK Gov, 日本政府 |

---

## Claude Agent SDK 統合

Claude Agent SDK を使って、このプロジェクトをプログラマティックに操作できます。

### インストール

```bash
pip install claude-agent-sdk
```

### 基本的な使い方

```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions

async def main():
    options = ClaudeAgentOptions(
        allowed_tools=["Read", "Write", "Bash", "Glob", "Grep"],
        permission_mode='acceptEdits',
        cwd="/path/to/browser-use-automation"
    )

    # ワンショットクエリ
    async for message in query(
        prompt="arXiv で machine learning の論文を10件検索して",
        options=options
    ):
        print(message)

asyncio.run(main())
```

### 連続会話（セッション保持）

```python
import asyncio
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions, AssistantMessage, TextBlock

async def main():
    options = ClaudeAgentOptions(
        allowed_tools=["Read", "Write", "Bash", "Glob", "Grep", "WebSearch"],
        permission_mode='acceptEdits',
        cwd="/path/to/browser-use-automation"
    )

    async with ClaudeSDKClient(options=options) as client:
        # 最初のクエリ
        await client.query("PRISMA研究システムで 'deep learning' を調査して")
        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(block.text)

        # フォローアップ（コンテキスト保持）
        await client.query("結果をMarkdownでまとめて")
        async for message in client.receive_response():
            # ...

asyncio.run(main())
```

### カスタムツール定義

```python
from claude_agent_sdk import tool, create_sdk_mcp_server

@tool("search_papers", "Search academic papers", {"query": str, "max_results": int})
async def search_papers(args):
    from automated_research_lightweight import HybridResearchSystem
    from langchain_openai import ChatOpenAI

    llm = ChatOpenAI(model="gpt-4o-mini")
    system = HybridResearchSystem(llm=llm, max_papers=args.get("max_results", 10))
    results = await system.search(args["query"])

    return {
        "content": [{
            "type": "text",
            "text": f"Found {len(results)} papers"
        }]
    }

# MCP サーバーとして公開
server = create_sdk_mcp_server(
    name="research-tools",
    version="1.0.0",
    tools=[search_papers]
)
```

### 権限モード

| モード | 説明 |
|--------|------|
| `default` | 標準（確認あり） |
| `acceptEdits` | ファイル編集を自動承認 |
| `plan` | プランニングのみ（実行しない） |
| `bypassPermissions` | すべて自動承認（注意） |

---

## 環境変数一覧

| 変数名 | 必須 | 説明 |
|--------|------|------|
| `LLM_PROVIDER` | ○ | `openai`, `claude`, `deepseek`, `google`, `groq` |
| `OPENAI_API_KEY` | △ | OpenAI APIキー |
| `ANTHROPIC_API_KEY` | △ | Claude APIキー |
| `DEEPSEEK_API_KEY` | △ | DeepSeek APIキー |
| `GOOGLE_API_KEY` | △ | Google Gemini APIキー |
| `GROQ_API_KEY` | △ | Groq APIキー |
| `PERPLEXITY_API_KEY` | △ | マルチソース検索用 |
| `BROWSER_USE_LOGGING_LEVEL` | - | `debug`, `info`, `warning`, `error` |
| `HEADLESS` | - | `true`/`false` (IEEE検索は`false`推奨) |

△ = 使用するプロバイダーに応じて設定

---

## 開発

### テスト

```bash
# CIテスト
uv run pytest -vxs tests/ci

# 全テスト
uv run pytest -vxs tests/
```

### コード品質

```bash
# 型チェック
uv run pyright

# Lint & Format
uv run ruff check --fix
uv run ruff format

# Pre-commit
uv run pre-commit run --all-files
```

### 新規ソースの追加

`DomainFilteredSource` を継承して簡単に追加:

```python
from automated_research_lightweight.sources import DomainFilteredSource, SourceCategory

class MyOrgSource(DomainFilteredSource):
    SOURCE_ID = "my_org"
    SOURCE_NAME = "My Organization"
    CATEGORY = SourceCategory.THINK_TANK
    DESCRIPTION = "Description of the organization"
    DOMAINS = ["myorg.org", "myorg.com"]
```

---

## システム要件

| 項目 | 最小 | 推奨 |
|------|------|------|
| OS | Linux (Ubuntu 20.04+) | Ubuntu 22.04+ |
| Python | 3.11 | 3.13 |
| uv | 0.4.0+ | 最新 |
| Chromium | 90+ | 最新 |

---

## トラブルシューティング

### ブラウザが起動しない

```bash
# ゾンビプロセスをクリーンアップ
./cleanup_browsers.sh
```

### IEEE Xplore で "Request Rejected"

```bash
# .env で HEADLESS=false に設定
HEADLESS=false
```

### ModuleNotFoundError

```bash
cd /path/to/browser-use-automation
uv sync
uv run python -m automated_research.main
```

---

## ライセンス

[Browser-Use](https://github.com/browser-use/browser-use) をベースに構築

---

## リンク

- [Browser-Use](https://github.com/browser-use/browser-use)
- [Claude Agent SDK](https://docs.anthropic.com/en/docs/agents-and-tools/claude-agent-sdk)
- [Perplexity API](https://docs.perplexity.ai/)
- [PRISMA 2020](https://www.prisma-statement.org/)

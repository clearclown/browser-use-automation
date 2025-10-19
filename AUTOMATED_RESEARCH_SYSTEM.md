# 自動研究支援システム - 完全ガイド

## 📊 概要

本システムは**2つのモード**を提供します：

### 1. **軽量版（推奨）** ⚡
- **リソース**: 20-30MB メモリ, 2-5% CPU
- **起動時間**: 0.1秒
- **技術**: httpx + BeautifulSoup + 公式API
- **カバレッジ**:
  - arXiv API (50%): 機械学習・AI・物理・数学分野
  - Semantic Scholar API (30%): 引用情報、影響力分析
  - IEEE Xplore軽量版 (20%): 電気・電子・コンピュータサイエンス
- **メリット**: **96%リソース削減**、安定性、高速

### 2. **ブラウザ自動化版** 🌐
- **リソース**: 500-800MB メモリ, 50-90% CPU
- **起動時間**: 15-180秒
- **技術**: browser-use (Chromium + CDP + AI Agent)
- **カバレッジ**: IEEE Xplore完全自動化
- **メリット**: 完全な画面操作、複雑な認証対応
- **デメリット**: 高リソース消費、不安定（環境依存）

---

## 🚀 使い方

### Streamlit Web UI（推奨）

```bash
# Streamlit起動
./run_streamlit.sh

# ブラウザでアクセス
http://localhost:8501
# または
http://100.104.61.108:8501 (Tailscale経由)
```

#### UI操作手順

1. **モード選択**（サイドバー）
   - 「軽量版（推奨）」または「ブラウザ自動化版」を選択
   - ⚡ 軽量版: リソース使用量96%削減
   - ⚠️ ブラウザ版: 高リソース消費

2. **LLM設定**（サイドバー）
   - プロバイダー: OpenAI / Claude / DeepSeek / Google / Groq
   - モデル名: 空欄でデフォルト使用

3. **検索設定**（サイドバー）
   - 最大論文数: 1-1000件
   - 開始年・終了年: 2000-2025
   - ヘッドレスモード（ブラウザ版のみ）: ⚠️ Falseを推奨

4. **研究情報入力**（メイン）
   - 研究トピック *（必須）
   - 研究課題 *（必須）
   - キーワード *（必須、1行に1つ）
   - 特定の関心領域（オプション）
   - 研究背景（オプション）

5. **実行**
   - 🚀 研究調査を開始ボタンをクリック
   - ログで進捗確認
   - 結果は「収集論文」「統合レポート」「生成ファイル」タブで閲覧

---

## 🏗️ 軽量版アーキテクチャ

### ディレクトリ構成

```
automated_research_lightweight/
├── __init__.py                      # パッケージ初期化
├── arxiv_searcher.py                # arXiv API検索エンジン
├── semantic_scholar_searcher.py     # Semantic Scholar API検索エンジン
├── ieee_searcher.py                 # IEEE Xplore軽量スクレイピング
├── hybrid_system.py                 # ハイブリッドシステム + AI自動化
└── output/                          # 出力ディレクトリ
    ├── result_YYYYMMDD_HHMMSS.json  # 検索結果JSON
    └── summary_YYYYMMDD_HHMMSS.md   # 統合レポート
```

### 主要クラス

#### 1. `ArxivSearcher`
```python
from automated_research_lightweight import ArxivSearcher

searcher = ArxivSearcher(max_results=10)
papers = await searcher.search_papers(
    query='deep learning',
    year_start=2023,
    year_end=2025,
    max_results=10
)
```

**特徴**:
- 公式arXiv API使用（認証不要）
- メモリ: 5-10MB
- CPU: <1%
- 速度: 2-5秒

#### 2. `SemanticScholarSearcher`
```python
from automated_research_lightweight import SemanticScholarSearcher

searcher = SemanticScholarSearcher()
papers = await searcher.search_papers(
    query='transformer',
    year_start=2023,
    max_results=10
)
```

**特徴**:
- 公式Semantic Scholar API使用（認証不要）
- 引用数、影響力スコア提供
- メモリ: 5-10MB
- CPU: <1%
- ⚠️ レート制限あり（100 requests/5 min）

#### 3. `IEEELightweightSearcher`
```python
from automated_research_lightweight import IEEELightweightSearcher

searcher = IEEELightweightSearcher()
papers = await searcher.search_papers(
    query='neural network',
    year_start=2022,
    year_end=2025,
    max_results=10
)
```

**特徴**:
- httpx + BeautifulSoupによるスクレイピング
- ブラウザ不使用
- メモリ: 10-20MB
- CPU: 1-2%
- 速度: 5-10秒

#### 4. `HybridResearchSystem` (AI自動化)
```python
from automated_research_lightweight import HybridResearchSystem
from automated_research.llm_provider import get_llm

llm = get_llm(provider='deepseek', temperature=0.4)
system = HybridResearchSystem(llm=llm, max_papers=10)

results = await system.run_research(
    research_topic='Large Language Models',
    research_question='LLMの最新研究動向は？',
    keywords=['LLM', 'transformer', 'GPT'],
    year_start=2023,
    year_end=2025
)
```

**AI自動化機能**:
1. **検索戦略決定**: LLMが研究内容を分析し、最適な検索エンジン割合を決定
2. **並列検索**: 3つの検索エンジンを同時実行
3. **重複除去**: タイトルベースで重複論文を除去
4. **統合レポート生成**: 収集論文をLLMが分析・要約

---

## 📈 パフォーマンス比較

| 項目 | ブラウザ自動化版 | 軽量版 | 削減率 |
|------|-----------------|--------|--------|
| **メモリ使用量** | 500-800MB | 20-30MB | **96%削減** |
| **CPU使用率** | 50-90% | 2-5% | **94%削減** |
| **起動時間** | 15-180秒 | 0.1秒 | **99%削減** |
| **安定性** | 環境依存（低） | 高 | ✅ |
| **速度** | 遅い（30-90秒/ページ） | 高速（2-10秒） | **80%削減** |

---

## 🔧 技術スタック

### 軽量版

- **httpx**: 非同期HTTPクライアント
- **BeautifulSoup4**: HTMLパーサー
- **arxiv**: arXiv公式Pythonクライアント
- **LangChain**: LLM統合フレームワーク

### ブラウザ自動化版

- **browser-use**: AI駆動ブラウザ自動化フレームワーク
- **Chromium**: フルブラウザエンジン
- **CDP (Chrome DevTools Protocol)**: ブラウザ制御プロトコル

### 共通

- **Streamlit**: Webインターフェース
- **OpenAI / Claude / DeepSeek / Google / Groq**: LLMプロバイダー
- **asyncio**: 非同期I/O

---

## 🎯 使い分けガイド

### 軽量版を使うべき場合（推奨）

✅ **以下の条件に当てはまる場合は軽量版を使用してください**:

1. リソースが限られている環境（8GB RAM未満）
2. 安定性・速度を重視
3. arXiv / Semantic Scholar で論文が見つかる分野
4. 大量の論文を一度に検索したい（100件以上）

### ブラウザ自動化版を使うべき場合

⚠️ **以下の条件に当てはまる場合のみ使用を検討**:

1. IEEE Xplore専用の検索が必須
2. 複雑な認証・ログインが必要
3. 十分なリソースがある環境（16GB+ RAM, 8+ cores）
4. 画面操作の記録が必要

---

## 📚 出力ファイル

### 軽量版

```
automated_research_lightweight/output/
├── result_20251018_143052.json      # 検索結果（JSON）
└── summary_20251018_143052.md       # 統合レポート（Markdown）
```

**result_YYYYMMDD_HHMMSS.json**:
```json
{
  "research_topic": "Large Language Models",
  "research_question": "LLMの最新研究動向は？",
  "keywords": ["LLM", "transformer", "GPT"],
  "search_strategy": {
    "arxiv_ratio": 50,
    "semantic_scholar_ratio": 30,
    "ieee_ratio": 20,
    "reasoning": "機械学習分野のため..."
  },
  "papers": [
    {
      "title": "...",
      "authors": ["..."],
      "published_date": "2024-05-15",
      "url": "...",
      "abstract": "...",
      "source": "arXiv API"
    }
  ],
  "reports": [...],
  "summary_report": "..."
}
```

### ブラウザ自動化版

```
automated_research/
├── data/
│   ├── research_info_SESSION_ID.json
│   └── search_strategy_SESSION_ID.json
└── reports/
    ├── session_SESSION_ID/
    │   ├── paper_1.md
    │   ├── paper_2.md
    │   └── ...
    └── summary_report_SESSION_ID.md
```

---

## 🐛 トラブルシューティング

### 軽量版

#### エラー: `ModuleNotFoundError: No module named 'arxiv'`

```bash
# 依存パッケージを再インストール
uv pip install arxiv beautifulsoup4
```

#### エラー: `Semantic Scholar HTTPエラー: 429`

**原因**: レート制限（100 requests/5 min）

**解決方法**:
1. 検索頻度を下げる（max_papers を減らす）
2. 数分待ってから再実行
3. Semantic Scholar割合を0%に設定（arXiv + IEEEのみ使用）

### ブラウザ自動化版

#### エラー: `TimeoutError: Browser did not start within 180 seconds`

**解決方法**:
1. ゾンビプロセスをクリーンアップ
   ```bash
   ./cleanup_browsers.sh
   ```

2. ヘッドレスモードを無効化（`headless=False`）

3. タイムアウトを延長（既に180秒に設定済み）

4. **推奨: 軽量版に切り替える**

---

## 📖 参考資料

### 分析ドキュメント

- [BROWSER_USE_PERFORMANCE_ANALYSIS.md](BROWSER_USE_PERFORMANCE_ANALYSIS.md): browser-useパフォーマンス分析
- [GOLANG_VS_PYTHON_ANALYSIS.md](GOLANG_VS_PYTHON_ANALYSIS.md): Go vs Python比較
- [ALTERNATIVE_SOLUTIONS.md](ALTERNATIVE_SOLUTIONS.md): 代替ソリューション提案

### 外部リンク

- [arXiv API Documentation](https://info.arxiv.org/help/api/index.html)
- [Semantic Scholar API Documentation](https://api.semanticscholar.org/api-docs/)
- [IEEE Xplore](https://ieeexplore.ieee.org/)
- [browser-use GitHub](https://github.com/browser-use/browser-use)

---

## 🎉 まとめ

### 軽量版の利点

✅ **96%リソース削減** (500-800MB → 20-30MB)
✅ **99%高速化** (15-180秒 → 0.1秒)
✅ **高安定性** (環境依存なし)
✅ **3つの検索エンジン統合** (arXiv + Semantic Scholar + IEEE)
✅ **AI自動化** (LLMによる検索戦略決定・統合レポート生成)

### 推奨設定

```yaml
実行モード: 軽量版（推奨）
LLMプロバイダー: DeepSeek（コスパ最高）
最大論文数: 10-50件
年範囲: 2022-2025
```

**これで、低リソース環境でも快適に研究調査が可能です！** 🚀

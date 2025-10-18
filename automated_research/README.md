# Automated Research System with PRISMA 2020 Compliance

**完全自動化されたPRISMA準拠の文献調査システム**

## 概要

このシステムは、[PRISMA 2020](https://www.prisma-statement.org/)（Preferred Reporting Items for Systematic Reviews and Meta-Analyses）ガイドラインに準拠した、完全自動化の文献調査システムです。

研究テーマを入力するだけで、以下を自動実行します：

1. **対話型ヒアリング**: 研究内容を深く理解
2. **PRISMA準拠検索戦略**: 体系的な文献検索計画を立案
3. **スクリーニング基準設定**: 包含/除外基準の自動生成
4. **自動文献検索**: IEEE Xplore等のデータベースを自動検索
5. **PRISMAフロー図生成**: 検索プロセスの可視化
6. **落合陽一式レポート生成**: 各論文の詳細分析
7. **統合レポート**: 全論文を統合した総合レビュー

## 🎯 PRISMA 2020準拠機能

### ✅ 実装済みPRISMA要素

- **体系的検索戦略**: Boolean演算子（AND/OR/NOT）を使った検索クエリ
- **複数データベース対応**: IEEE Xplore実装済み、拡張可能な設計
- **包含/除外基準**: 明示的な基準定義と自動適用
- **スクリーニング記録**: 各論文の判定と除外理由の追跡
- **PRISMAフローダイアグラム**: Mermaid形式での自動生成
- **メタデータ記録**: 検索日時、データベース名、検索結果数
- **重複除去**: タイトルベースの自動重複削除

## 実装済み機能

### ✅ ステップ1: 対話型ヒアリング
- `research_interview.py`
- LLMを使った対話形式で研究内容を深堀り
- 研究テーマ、目的、技術、問題意識を抽出

### ✅ ステップ2: PRISMA方式検索戦略
- `prisma_search_strategy.py`
- 体系的文献レビューの標準手法に基づく検索戦略
- Boolean演算子を使った複数の検索クエリ生成
- 除外キーワードでノイズ低減

### ✅ ステップ3: IEEE自動検索
- `ieee_automated_search.py`
- browser-useの既存`IEEESearchService`を活用
- 複数クエリで自動検索
- 重複除去、メタデータ収集

### ✅ ステップ4: 落合陽一式レポート生成
- `ochiai_report_generator.py`
- 各論文に対して以下を分析:
  1. どんなもの？
  2. 先行研究と比べてどこがすごいの？
  3. 技術や手法の"キモ"はどこにある？
  4. どうやって有効だと検証した？
  5. 議論はあるか？
  6. 次に読むべき論文はあるか？
  7. **自分の研究との関連**（ユーザー固有）

### ✅ ステップ5: 統合レポート生成
- `ochiai_report_generator.py`（`generate_summary_report`）
- すべての論文レポートを統合
- 研究トレンド、技術分類、重要な発見を抽出
- ユーザーの研究への具体的示唆

## 使用方法

### 基本実行

```bash
# 完全自動実行（対話モードあり）
python -m automated_research.main

# または
python automated_research/main.py
```

### オプション

```bash
# ヘッドレスモードで実行
python -m automated_research.main --headless

# 収集論文数を指定
python -m automated_research.main --max-papers 50

# 使用するLLMモデルを指定
python -m automated_research.main --model gpt-4o-mini
```

## 出力ファイル

実行すると以下のファイルが生成されます：

```
automated_research/
├── data/
│   ├── research_info_YYYYMMDD_HHMMSS.json      # 研究情報
│   ├── search_strategy_YYYYMMDD_HHMMSS.json    # 検索戦略
│   └── collected_papers_YYYYMMDD_HHMMSS.json   # 収集論文リスト
├── reports/
│   ├── session_YYYYMMDD_HHMMSS/                # 個別論文レポート
│   │   ├── 001_Paper_Title.md
│   │   ├── 002_Another_Paper.md
│   │   └── ...
│   ├── summary_report_YYYYMMDD_HHMMSS.md       # 統合レポート
│   └── papers_list_YYYYMMDD_HHMMSS.json        # 論文リスト
└── logs/
    └── (ログファイル)
```

## 個別モジュールの単独実行

各ステップを個別にテストすることも可能：

```bash
# ステップ1: ヒアリングのみ
python -m automated_research.research_interview

# ステップ2: 検索戦略生成のみ
python -m automated_research.prisma_search_strategy

# ステップ3: IEEE検索のみ
python -m automated_research.ieee_automated_search

# ステップ4: レポート生成のみ
python -m automated_research.ochiai_report_generator
```

## 必要な環境変数

`.env`ファイルに以下を設定：

```bash
# OpenAI API Key（必須）
OPENAI_API_KEY=sk-...

# オプション：他のLLMプロバイダー
# ANTHROPIC_API_KEY=...
# GOOGLE_API_KEY=...
```

## システム要件

- Python 3.11以上
- `uv`パッケージマネージャー
- 十分なディスク容量（PDF保存用）
- 安定したインターネット接続

## 技術スタック

- **browser-use**: ブラウザ自動化
- **OpenAI GPT-4**: LLMによる分析
- **IEEESearchService**: IEEE Xplore検索（既存実装）
- **Pydantic**: データバリデーション
- **asyncio**: 非同期処理

## トラブルシューティング

### IEEE Xploreにアクセスできない

- ネットワーク接続を確認
- ヘッドレスモードを解除して動作確認: `--headless`を外す

### LLMの応答が遅い

- モデルを変更: `--model gpt-4o-mini`
- タイムアウト設定を調整（コード内）

### 論文が見つからない

- 検索クエリを手動で調整
- `search_strategy.json`を編集してから再実行

## 🧪 テスト

```bash
# 全テスト実行
uv run pytest -vxs tests/ci/

# automated_research関連のテストのみ
uv run pytest -vxs tests/ci/test_prisma_search_strategy.py
uv run pytest -vxs tests/ci/test_automated_research_integration.py

# 個別コンポーネントのテスト
python automated_research/prisma_flow_diagram.py
python automated_research/screening_criteria.py
```

## 🐳 Podman/Docker実行

### ローカルでビルド

```bash
# Podmanでビルド
podman build -f Containerfile -t browser-use-research .

# Dockerでビルド
docker build -f Containerfile -t browser-use-research .
```

### docker-composeで実行

```bash
# .envファイルにAPI keyを設定
echo "OPENAI_API_KEY=sk-your-key" > .env

# 起動
podman-compose up

# または
docker-compose up
```

### Podman rootlessモードで実行

```bash
podman run -it --rm \
  --userns=keep-id \
  --security-opt label=disable \
  --shm-size=2g \
  -e OPENAI_API_KEY="sk-your-key" \
  -v ./automated_research:/app/automated_research:Z \
  -v ./papers:/app/papers:Z \
  browser-use-research --max-papers 30
```

## 📚 PRISMA 2020準拠チェックリスト

| PRISMA項目 | 実装状況 | ファイル |
|-----------|---------|---------|
| Eligibility criteria | ✅ | `screening_criteria.py` |
| Information sources | ✅ | `ieee_automated_search.py` |
| Search strategy | ✅ | `prisma_search_strategy.py` |
| Selection process | ✅ | `screening_criteria.py` |
| Data collection | ✅ | `ieee_automated_search.py` |
| Study selection flow | ✅ | `prisma_flow_diagram.py` |
| Study characteristics | ✅ | JSON出力ファイル |
| Synthesis methods | ✅ | `ochiai_report_generator.py` |

## 📖 参考文献

1. **PRISMA 2020**: Page MJ, McKenzie JE, Bossuyt PM, et al. The PRISMA 2020 statement: an updated guideline for reporting systematic reviews. BMJ 2021;372:n71. doi:10.1136/bmj.n71

2. **PRISMA公式サイト**: https://www.prisma-statement.org/

## 今後の拡張予定

### データベース対応拡張
- [ ] arXiv自動検索
- [ ] PubMed/MEDLINE対応
- [ ] Google Scholar対応
- [ ] Scopus対応
- [ ] Web of Science対応

### 機能拡張
- [ ] PDFからの直接テキスト抽出
- [ ] 引用ネットワーク分析・可視化
- [ ] 複数レビュアーによる独立スクリーニング
- [ ] リスクオブバイアス評価
- [ ] メタ分析機能
- [ ] Webダッシュボード
- [ ] スケジュール実行（cron対応）

## ライセンス

このプロジェクトは親プロジェクト（browser-use）のライセンスに従います。

## 貢献

プルリクエスト歓迎！

---

Generated with ❤️ by the browser-use community

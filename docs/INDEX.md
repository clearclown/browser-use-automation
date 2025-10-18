# Documentation Index

Browser-Use Automation with PRISMA-Compliant Research System のドキュメント一覧

---

## 📚 メインドキュメント

### 🏠 [README.md](../README.md)
プロジェクト全体の概要、システムの仕組み、セットアップ手順、使用方法

**内容**:
- **概要**: PRISMA 2020準拠の完全自動化文献調査システム
- **主な機能**:
  - PRISMA準拠研究システム（9つの自動化ステップ）
  - マルチデータベース対応（arXiv, J-STAGE, 政府文書, IEEE）
  - 複数レビュアー・リスクオブバイアス評価
- **システムの仕組み**: アーキテクチャ図・技術スタック
- **クイックスタート**: 5分で始める
- **システム要件**: Python 3.11+, uv, Chromium
- **詳細セットアップ手順**: Ubuntu/Fedora対応
- **使用方法**: PRISMA研究、コンテナ実行、個別モジュール
- **出力ファイル**: ディレクトリ構造・主要ファイルの説明
- **トラブルシューティング**: よくある問題と解決方法
- **開発者向け情報**: テスト実行、コード品質チェック、アーキテクチャ
- **テスト結果**: 64テスト100%合格の詳細

**おすすめ読者**: 初めての方、システム全体を理解したい方

---

## 🔬 PRISMA準拠研究システム

### 📖 [automated_research/README.md](../automated_research/README.md)
PRISMA 2020準拠の自動文献調査システムの詳細ドキュメント

**内容**:
- **PRISMA 2020準拠機能**: 9つの実装済みPRISMA要素
  - Eligibility criteria（スクリーニング基準）
  - Information sources（複数データベース）
  - Search strategy（検索戦略生成）
  - Risk of bias assessment（Cochrane RoB 2準拠）
  - Multiple reviewers（Cohen's kappa計算）
- **実装済み機能の詳細**: ステップ1〜7の説明
- **使用方法**: 基本実行、オプション、個別モジュール実行
- **出力ファイル**: データ・レポート・ログの構造
- **必要な環境変数**: LLM API Keys等
- **テスト**: Unit Tests (59), Integration Tests (5)
- **Podman/Docker実行**: コンテナ対応の詳細
- **PRISMA 2020準拠チェックリスト**: 実装状況一覧

**おすすめ読者**: PRISMA研究を始める方、機能詳細を知りたい方

### ⚡ [automated_research/QUICKSTART.md](../automated_research/QUICKSTART.md)
クイックスタートガイド - 最速5分で動かす

**内容**:
- **最速で動かす**: 4ステップで実行
- **実行例**: 対話的実行の実際の出力
- **ヘッドレスモード**: バックグラウンド実行
- **生成されるファイル**: データ・レポートの説明
- **統合レポートの内容**: 7つの主要セクション
- **個別論文レポートの内容**: 落合陽一式7項目
- **トラブルシューティング**: よくあるエラーと解決方法
- **よくある質問**: 実行時間、費用、日本語対応等

**おすすめ読者**: とにかく早く動かしたい方、初めての方

---

## 🔍 データベース検索

### 📖 arXiv検索 (`automated_research/arxiv_search.py`)

**特徴**:
- **XML API対応**: arXiv公式APIを使用
- **高速検索**: 非同期HTTPリクエストで並列処理
- **メタデータ完全抽出**: タイトル、著者、要約、カテゴリ、出版年、PDF URL
- **重複除去**: タイトルベースの自動重複削除
- **テスト**: 9テスト（100%合格）

### 📖 J-STAGE検索 (`automated_research/jstage_search.py`)

**特徴**:
- **日本語対応**: Hiragana, Katakana, Kanji自動検出
- **Unicode範囲検出**: 日本語論文の完全サポート
- **メタデータ抽出**: タイトル、著者、要約、DOI、URL
- **テスト**: 10テスト（100%合格）

### 📖 政府文書検索 (`automated_research/government_documents_search.py`)

**特徴**:
- **6ソース対応**: USA, Japan, UK, EU, WHO, UN
- **文書タイプ検出**: Executive Order, Regulation, Report等
- **機関情報抽出**: URLから発行機関を自動抽出
- **テスト**: 14テスト（100%合格）

### 📖 IEEE Xplore検索 (`automated_research/ieee_automated_search.py`)

**特徴**:
- **Browser-Use統合**: IEEESearchServiceを活用
- **自動論文検索**: キーワードベースの検索
- **メタデータ抽出**: タイトル、著者、DOI、URL
- **詳細**: [IEEE_SEARCH_README.md](../IEEE_SEARCH_README.md)

---

## 📊 PRISMA機能詳細

### 📖 リスクオブバイアス評価 (`automated_research/risk_of_bias.py`)

**Cochrane RoB 2準拠**:
- **5ドメイン評価**: Randomization, Deviations, Missing data, Outcome measurement, Selection reporting
- **3段階評価**: Low, Some concerns, High
- **Overall Risk計算**: 自動集計
- **テスト**: 8テスト（100%合格）

### 📖 複数レビュアー機能 (`automated_research/multiple_reviewers.py`)

**機能**:
- **独立スクリーニング**: 複数レビュアーによる独立判定
- **Cohen's kappa計算**: レビュアー間一致度の定量評価
- **コンフリクト解決**: 不一致の検出と解決
- **CSV出力**: レビュアー判定記録の保存
- **テスト**: 9テスト（100%合格）

### 📖 PRISMA検索戦略 (`automated_research/prisma_search_strategy.py`)

**機能**:
- **Boolean演算子**: AND/OR/NOT を使った体系的検索
- **主要・関連・除外キーワード**: 3種類のキーワード管理
- **複数検索クエリ生成**: 包括的な検索戦略
- **年範囲・出版物タイプ**: フィルタ設定
- **テスト**: 9テスト（100%合格）

### 📖 PRISMAフロー図 (`automated_research/prisma_flow_diagram.py`)

**機能**:
- **Mermaid形式**: GitHub/Markdown対応
- **検索プロセス可視化**: データベース別結果数
- **スクリーニング記録**: 除外理由別の件数
- **重複除去記録**: 重複削除件数の追跡

### 📖 スクリーニング基準 (`automated_research/screening_criteria.py`)

**機能**:
- **包含基準**: 論文を含める条件の定義
- **除外基準**: 論文を除外する条件の定義
- **自動適用**: 基準に基づく自動判定
- **除外理由記録**: 各論文の除外理由を追跡

---

## 🐳 コンテナ実行

### 📖 [PODMAN_SETUP.md](../PODMAN_SETUP.md)
Podman/Dockerでの実行ガイド

**内容**:
- **Podmanビルド手順**: ステップバイステップ
- **Rootlessモード実行方法**: 非root実行の詳細
- **X11転送設定**: GUIアプリケーション実行
- **SELinux対応**: `:z` フラグの使用方法
- **トラブルシューティング**: Permission denied等

**イメージサイズ**: 2.02 GB
**ビルド時間**: 約10分
**テスト**: 全テスト合格 ✅

---

## 🎬 デモ・ガイド

### 📖 [DEMO_GUIDE.md](../DEMO_GUIDE.md)
システムデモンストレーションガイド

**内容**:
- ステップバイステップのデモ手順
- 期待される出力例
- 実行例のスクリーンショット

---

## 🛠️ 開発者向けドキュメント

### 📖 [CONTRIBUTING.md](../CONTRIBUTING.md)
開発ワークフロー・TDD手順

**内容**:
- **推奨開発ワークフロー**: Push前に必ずローカルテスト
- **TDD手順**: Test-First開発（t-wada流）
- **テストコマンド一覧**: Unit, Integration, Quality Check
- **Podmanコンテナテスト**: ローカルコンテナテスト方法
- **Gitコミットメッセージ規約**: プレフィックス、例
- **よくある問題と解決方法**: GitHub Actions失敗、ruff format等
- **重要なリマインダー**: ローカルテスト必須、TDD、細かいコミット

**開発手法**: Test-Driven Development (TDD, t-wada流)

### 📖 [TEST_SUMMARY.md](../TEST_SUMMARY.md)
テスト実行結果詳細レポート

**内容**:
- **テスト実行結果**: 64/64 passed (100%)
  - Unit Tests: 59/59 passed (7.63秒)
  - Integration Tests: 5/5 passed (0.53秒)
- **GitHub Actions**: Tests & Quality = SUCCESS
- **テスト詳細**: 各テストファイルの内容
- **PRISMA 2020コンポーネント実装状況**: 完全実装
- **GitHub Actionsワークフロー**: 2つのワークフロー詳細
- **ドキュメント**: 完備
- **ローカルテスト実行方法**: test-local.sh使用方法
- **トラブルシューティング**: テスト失敗時の対処方法

### 📖 [CLAUDE.md](../CLAUDE.md)
Claude Codeでの開発ガイド（開発者向け）

**内容**:
- **High-Level Architecture**: Agent, BrowserSession, EventBus
- **Development Commands**: Setup, Testing, Quality Checks
- **Code Style**: async, tabs, modern typing
- **CDP-Use**: cdp-use使用方法
- **Keep Examples & Tests Up-To-Date**: 重要な方針
- **Strategy For Making Changes**: 変更時の戦略

### 📖 [browser_use/README.md](../browser_use/README.md)
Browser-Useライブラリの詳細ドキュメント

---

## 📊 テスト・品質保証

### 📖 テストファイル一覧

| テストファイル | テスト数 | 内容 | 結果 |
|-------------|---------|------|------|
| `test_arxiv_search.py` | 9 | arXiv API検索、XML解析、重複除去 | ✅ PASSED |
| `test_jstage_search.py` | 10 | J-STAGE検索、日本語対応、メタデータ | ✅ PASSED |
| `test_government_documents_search.py` | 14 | 6ヶ国・機関の政府文書検索 | ✅ PASSED |
| `test_risk_of_bias.py` | 8 | Cochrane RoB 2準拠評価 | ✅ PASSED |
| `test_multiple_reviewers.py` | 9 | 複数レビュアー、Cohen's kappa | ✅ PASSED |
| `test_prisma_search_strategy.py` | 9 | PRISMA検索戦略、Boolean演算 | ✅ PASSED |
| `test_full_research_workflow.py` | 5 | 完全ワークフロー結合テスト | ✅ PASSED |
| **合計** | **64** | - | **100%** |

### ローカルテスト実行

```bash
# 推奨: ローカルテストスクリプト（GitHub Actionsと同じ）
bash .github/workflows/test-local.sh

# または手動で
uv run pytest tests/ci/test_arxiv_search.py tests/ci/test_jstage_search.py tests/ci/test_government_documents_search.py tests/ci/test_risk_of_bias.py tests/ci/test_multiple_reviewers.py tests/ci/test_prisma_search_strategy.py -v

# 結合テスト
uv run pytest tests/integration/test_full_research_workflow.py -v
```

### GitHub Actions

**Workflow 1**: `automated-research-tests.yml`
- Unit Tests: 6グループ並列実行
- Integration Tests: 完全ワークフロー
- Container Tests: Podman環境検証
- Test Summary: 自動レポート生成
- **実行時間**: 約4分
- **Status**: ✅ SUCCESS

**Workflow 2**: `automated-research-quality.yml`
- Ruff Format Check
- Ruff Lint Check
- Pyright Type Check
- Security Scan (bandit)
- Documentation Check
- **実行時間**: 約30秒
- **Status**: ✅ SUCCESS

---

## 🔗 外部リソース

- **PRISMA 2020公式サイト**: https://www.prisma-statement.org/
- **Cochrane RoB 2**: https://www.riskofbias.info/welcome/rob-2-0-tool
- **Browser-Use GitHub**: https://github.com/browser-use/browser-use
- **Browser-Use Docs**: https://docs.browser-use.com
- **IEEE Xplore**: https://ieeexplore.ieee.org/
- **arXiv**: https://arxiv.org/
- **arXiv API Documentation**: https://arxiv.org/help/api/
- **J-STAGE**: https://www.jstage.jst.go.jp/
- **Cohen's kappa**: https://en.wikipedia.org/wiki/Cohen%27s_kappa

---

## 📝 ドキュメント構造

```
browser-use-automation/
├── README.md                           # ★メインREADME（ここから始める）
├── docs/
│   ├── INDEX.md                        # ★このファイル（ドキュメント一覧）
│   ├── README.md                       # docs概要
│   └── archive/
│       └── AUTOMATED_RESEARCH_SYSTEM.md  # アーカイブ
├── automated_research/
│   ├── README.md                       # PRISMA研究システム詳細
│   ├── QUICKSTART.md                   # ★クイックスタート（5分）
│   ├── arxiv_search.py                 # arXiv検索実装
│   ├── jstage_search.py                # J-STAGE検索実装
│   ├── government_documents_search.py  # 政府文書検索実装
│   ├── risk_of_bias.py                 # RoB評価実装
│   ├── multiple_reviewers.py           # 複数レビュアー実装
│   ├── prisma_search_strategy.py       # 検索戦略実装
│   ├── prisma_flow_diagram.py          # フロー図実装
│   └── screening_criteria.py           # スクリーニング基準実装
├── tests/
│   ├── ci/
│   │   ├── test_arxiv_search.py        # arXiv検索テスト（9）
│   │   ├── test_jstage_search.py       # J-STAGE検索テスト（10）
│   │   ├── test_government_documents_search.py  # 政府文書テスト（14）
│   │   ├── test_risk_of_bias.py        # RoB評価テスト（8）
│   │   ├── test_multiple_reviewers.py  # 複数レビュアーテスト（9）
│   │   └── test_prisma_search_strategy.py  # 検索戦略テスト（9）
│   └── integration/
│       └── test_full_research_workflow.py  # 結合テスト（5）
├── IEEE_SEARCH_README.md               # IEEE検索詳細
├── PODMAN_SETUP.md                     # Podmanセットアップ
├── DEMO_GUIDE.md                       # デモガイド
├── CONTRIBUTING.md                     # ★開発ワークフロー・TDD手順
├── TEST_SUMMARY.md                     # ★テスト実行結果詳細
├── CLAUDE.md                           # 開発者ガイド
├── docker/
│   └── README.md                       # Docker設定
└── browser_use/
    └── README.md                       # Browser-Useライブラリ
```

---

## 🆕 最新情報

### 2025-10-18: PRISMA 2020準拠システム実装完了 & 完全テストカバレッジ

**新機能**:
- **PRISMA 2020準拠システム**: 完全自動化の文献調査システム
  - ✅ arXiv検索: 9テスト実装・合格
  - ✅ J-STAGE検索: 10テスト実装・合格
  - ✅ 政府文書検索: 14テスト実装・合格（USA, Japan, UK, EU, WHO, UN）
  - ✅ リスクオブバイアス評価: 8テスト実装・合格（Cochrane RoB 2準拠）
  - ✅ 複数レビュアー機能: 9テスト実装・合格（Cohen's kappa計算）
  - ✅ PRISMA検索戦略: 9テスト実装・合格
  - ✅ 結合テスト: 5テスト実装・合格

- **Podman Rootless対応完了**:
  - UV_CACHE_DIR権限エラー修正
  - 全34ステップのビルド成功
  - コンテナ内で全テスト合格
  - イメージサイズ: 2.02 GB

**テスト結果**:
- **ホスト環境**: 64/64 passed (100%) ✅
- **Podman Container**: 全テスト passed ✅
- **GitHub Actions**: Tests & Quality = SUCCESS ✅
- **TDD方式**: 全機能をTest-First開発で実装

**開発手法**: Test-Driven Development (TDD, t-wada流)

---

## 💡 はじめ方（レベル別）

### 🌱 初めての方

1. **[README.md](../README.md)** を読んで全体を理解
2. **[QUICKSTART.md](../automated_research/QUICKSTART.md)** で5分で動かす
3. **統合レポート** を読んで結果を確認
4. **個別論文レポート** で気になる論文を深掘り

### 🔬 PRISMA研究を始める方

1. **[automated_research/README.md](../automated_research/README.md)** で機能詳細を確認
2. **[CONTRIBUTING.md](../CONTRIBUTING.md)** で開発ワークフロー理解
3. **ローカルテスト実行**: `bash .github/workflows/test-local.sh`
4. **PRISMA研究システム実行**: `uv run python -m automated_research.main`

### 🐳 コンテナで実行する方

1. **[PODMAN_SETUP.md](../PODMAN_SETUP.md)** でセットアップ
2. **Containerfileビルド**: `podman build -t browser-use-research -f Containerfile .`
3. **コンテナ実行**: `podman run --rm -it ...`
4. **トラブルシューティング**: Permission denied等の対処

### 👨‍💻 開発に参加する方

1. **[CLAUDE.md](../CLAUDE.md)** でアーキテクチャ理解
2. **[CONTRIBUTING.md](../CONTRIBUTING.md)** で開発ワークフロー理解
3. **[TEST_SUMMARY.md](../TEST_SUMMARY.md)** でテスト仕様確認
4. **TDD**: テストを先に書いてから実装
5. **ローカルテスト**: push前に必ず `bash .github/workflows/test-local.sh`

### 🔍 特定機能を使う方

| やりたいこと | 参照ドキュメント |
|------------|---------------|
| **arXiv検索** | `automated_research/arxiv_search.py` コード |
| **J-STAGE検索** | `automated_research/jstage_search.py` コード |
| **政府文書検索** | `automated_research/government_documents_search.py` コード |
| **リスクオブバイアス評価** | `automated_research/risk_of_bias.py` コード |
| **複数レビュアー** | `automated_research/multiple_reviewers.py` コード |
| **IEEE検索** | [IEEE_SEARCH_README.md](../IEEE_SEARCH_README.md) |

---

## 📖 ドキュメント読む順番（おすすめ）

### パターン1: とにかく動かしたい

1. **[QUICKSTART.md](../automated_research/QUICKSTART.md)** - 5分で実行
2. **統合レポート** (`automated_research/reports/summary_report_*.md`) - 結果確認
3. **[README.md](../README.md)** - 全体理解

### パターン2: じっくり理解したい

1. **[README.md](../README.md)** - 全体像把握
2. **[automated_research/README.md](../automated_research/README.md)** - 機能詳細
3. **[TEST_SUMMARY.md](../TEST_SUMMARY.md)** - テスト仕様
4. **[CONTRIBUTING.md](../CONTRIBUTING.md)** - 開発手法
5. **[CLAUDE.md](../CLAUDE.md)** - アーキテクチャ

### パターン3: 開発に参加したい

1. **[CONTRIBUTING.md](../CONTRIBUTING.md)** - 開発ワークフロー
2. **[TEST_SUMMARY.md](../TEST_SUMMARY.md)** - テスト仕様
3. **[CLAUDE.md](../CLAUDE.md)** - アーキテクチャ
4. **テストコード** (`tests/ci/test_*.py`) - テスト実装例
5. **実装コード** (`automated_research/*.py`) - 実装例

---

## ✅ Status

**Production Ready** ✅

- **Tests**: 64/64 passed (100%) ✅
- **CI/CD**: GitHub Actions SUCCESS ✅
- **Container**: Podman Rootless Ready ✅
- **Documentation**: Complete ✅
- **PRISMA 2020 Compliance**: Full ✅
- **TDD**: Complete Test Coverage ✅

---

**Last Updated**: 2025-10-18
**Version**: 1.0.0 (Production Ready)

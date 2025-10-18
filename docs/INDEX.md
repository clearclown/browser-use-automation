# Documentation Index

Browser-Use Automation with PRISMA-Compliant Research System のドキュメント一覧

---

## 📚 メインドキュメント

### 🏠 [README.md](../README.md)
プロジェクト全体の概要、セットアップ手順、基本的な使用方法

**内容**:
- PRISMA準拠研究システム概要
- IEEE Xplore統合機能
- マルチデータベース対応
- システム要件とセットアップ
- 基本的な使用方法
- トラブルシューティング

---

## 🔬 PRISMA準拠研究システム

### 📖 [automated_research/README.md](../automated_research/README.md)
PRISMA 2020準拠の自動文献調査システムの詳細ドキュメント

**内容**:
- システム概要と機能一覧
- PRISMA 2020準拠機能の詳細
- 使用方法（完全自動実行）
- 出力ファイルの説明
- 個別モジュールの使用方法
- テスト実行方法
- Podman/Docker実行

### ⚡ [automated_research/QUICKSTART.md](../automated_research/QUICKSTART.md)
クイックスタートガイド - 5分で始める

**内容**:
- 最小限のセットアップ
- 最も簡単な実行方法
- 基本的なトラブルシューティング

---

## 🔍 IEEE Xplore統合

### 📖 [IEEE_SEARCH_README.md](../IEEE_SEARCH_README.md)
IEEE Xplore論文検索・引用抽出システムの詳細ドキュメント

**内容**:
- 全コマンドラインオプション詳細
- 対話的インターフェースの完全ガイド
- 引用抽出のAPI使用方法
- PDF抽出の仕組み
- 技術詳細・アーキテクチャ

---

## 🐳 コンテナ実行

### 📖 [PODMAN_SETUP.md](../PODMAN_SETUP.md)
Podman/Dockerでの実行ガイド

**内容**:
- Podmanビルド手順
- Rootlessモード実行方法
- X11転送設定
- トラブルシューティング

### 📖 [docker/README.md](../docker/README.md)
Dockerコンテナの詳細設定

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

### 📖 [CLAUDE.md](../CLAUDE.md)
Claude Codeでの開発ガイド（開発者向け）

**内容**:
- プロジェクト構造
- コーディング規約
- テスト方針
- 重要な設計パターン

### 📖 [browser_use/README.md](../browser_use/README.md)
Browser-Useライブラリの詳細ドキュメント

---

## 📊 テスト・品質保証

### テストドキュメント

**自動テスト**:
- `tests/ci/test_arxiv_search.py` - arXiv検索テスト（9テスト）
- `tests/ci/test_jstage_search.py` - J-STAGE検索テスト（10テスト）
- `tests/ci/test_government_documents_search.py` - 政府文書検索テスト（14テスト）
- `tests/ci/test_risk_of_bias.py` - リスクオブバイアス評価テスト（8テスト）
- `tests/ci/test_multiple_reviewers.py` - 複数レビュアーテスト（9テスト）
- `tests/integration/test_full_research_workflow.py` - 結合テスト（5テスト）

**テスト実行**:
```bash
# 全テスト実行
uv run pytest -vxs tests/ci

# automated_research関連テストのみ
uv run pytest -vxs tests/ci/test_arxiv_search.py tests/ci/test_jstage_search.py tests/ci/test_government_documents_search.py tests/ci/test_risk_of_bias.py tests/ci/test_multiple_reviewers.py

# 結合テスト
uv run pytest -vxs tests/integration/test_full_research_workflow.py
```

---

## 🔗 外部リソース

- **PRISMA 2020公式サイト**: https://www.prisma-statement.org/
- **Browser-Use GitHub**: https://github.com/browser-use/browser-use
- **Browser-Use Docs**: https://docs.browser-use.com
- **IEEE Xplore**: https://ieeexplore.ieee.org/
- **arXiv**: https://arxiv.org/
- **J-STAGE**: https://www.jstage.jst.go.jp/

---

## 📝 ドキュメント構造

```
browser-use-automation/
├── README.md                           # メインREADME
├── docs/
│   ├── INDEX.md                        # このファイル
│   └── README.md                       # docs概要
├── automated_research/
│   ├── README.md                       # PRISMA研究システム詳細
│   └── QUICKSTART.md                   # クイックスタート
├── IEEE_SEARCH_README.md               # IEEE検索詳細
├── PODMAN_SETUP.md                     # Podmanセットアップ
├── DEMO_GUIDE.md                       # デモガイド
├── CLAUDE.md                           # 開発者ガイド
├── docker/
│   └── README.md                       # Docker設定
└── browser_use/
    └── README.md                       # Browser-Useライブラリ
```

---

## 🆕 最新情報

**2025-10-18**: PRISMA 2020準拠システム実装完了
- 複数データベース対応（arXiv、J-STAGE、政府文書）
- リスクオブバイアス評価
- 複数レビュアー機能
- Podman Rootless対応完了
- 73テスト実装・全合格

---

## 💡 はじめ方

1. **初めての方**: [README.md](../README.md) → [QUICKSTART.md](../automated_research/QUICKSTART.md)
2. **PRISMA研究を始める**: [automated_research/README.md](../automated_research/README.md)
3. **IEEE検索を使う**: [IEEE_SEARCH_README.md](../IEEE_SEARCH_README.md)
4. **コンテナで実行**: [PODMAN_SETUP.md](../PODMAN_SETUP.md)
5. **開発に参加**: [CLAUDE.md](../CLAUDE.md)

---

**Last Updated**: 2025-10-18

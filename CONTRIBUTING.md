# Contributing Guide

## 🚀 開発ワークフロー（推奨）

### ⚠️ 重要: Push前に必ずローカルテストを実行

GitHub Actionsでのテスト失敗を防ぐため、**必ずローカルでテストを実行してからpush**してください。

```bash
# 1. ローカルテストスクリプトを実行
bash .github/workflows/test-local.sh

# 2. 全テストが通ったらコミット
git add .
git commit -m "your message"

# 3. pushする前にもう一度確認
uv run pytest -xvs tests/ci/ -q

# 4. OK なら push
git push
```

---

## 📋 開発手順

### 1. 新機能の追加

#### ステップ1: TDD - テストを先に書く

```bash
# 新しいテストファイルを作成
touch tests/ci/test_new_feature.py

# テストを書く（まだ実装はない）
# テストは失敗するはず
uv run pytest -xvs tests/ci/test_new_feature.py
```

#### ステップ2: 実装

```bash
# 機能を実装
touch automated_research/new_feature.py

# テストが通るまで実装
uv run pytest -xvs tests/ci/test_new_feature.py
```

#### ステップ3: ローカルテスト

```bash
# 全テストを実行
bash .github/workflows/test-local.sh

# または個別に
uv run ruff format automated_research/
uv run ruff check automated_research/ --fix
uv run pytest -xvs tests/ci/
```

#### ステップ4: コミット

```bash
git add tests/ci/test_new_feature.py automated_research/new_feature.py
git commit -m "feat: 新機能追加

- テスト: test_new_feature.py
- 実装: new_feature.py
- X個のテスト追加

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

#### ステップ5: Push前の最終確認

```bash
# もう一度テスト
uv run pytest -xvs tests/ci/test_new_feature.py

# OK なら push
git push
```

---

## 🧪 テストコマンド一覧

### 全テスト実行

```bash
# 推奨: ローカルテストスクリプト（GitHub Actionsと同じ）
bash .github/workflows/test-local.sh

# または手動で
uv run pytest -xvs tests/ci/
uv run pytest -xvs tests/integration/
```

### 個別テスト実行

```bash
# arXiv検索
uv run pytest -xvs tests/ci/test_arxiv_search.py

# J-STAGE検索
uv run pytest -xvs tests/ci/test_jstage_search.py

# 政府文書検索
uv run pytest -xvs tests/ci/test_government_documents_search.py

# リスクオブバイアス
uv run pytest -xvs tests/ci/test_risk_of_bias.py

# 複数レビュアー
uv run pytest -xvs tests/ci/test_multiple_reviewers.py

# PRISMA検索戦略
uv run pytest -xvs tests/ci/test_prisma_search_strategy.py

# 結合テスト
uv run pytest -xvs tests/integration/test_full_research_workflow.py
```

### コード品質チェック

```bash
# フォーマットチェック
uv run ruff format automated_research/ --check

# フォーマット実行
uv run ruff format automated_research/

# Lintチェック
uv run ruff check automated_research/

# Lint修正
uv run ruff check automated_research/ --fix

# 型チェック
uv run pyright automated_research/
```

---

## 🐳 Podmanコンテナテスト

### ローカルでコンテナテスト

```bash
# 1. ビルド
podman build -t browser-use-research:test -f Containerfile .

# 2. テスト実行
podman run --rm \
  --entrypoint bash \
  -e UV_CACHE_DIR=/tmp/uv-cache \
  browser-use-research:test \
  -c "mkdir -p /tmp/uv-cache && uv run pytest -xvs tests/ci/test_arxiv_search.py --tb=short"

# 3. 結合テスト
podman run --rm \
  --entrypoint bash \
  -e UV_CACHE_DIR=/tmp/uv-cache \
  browser-use-research:test \
  -c "mkdir -p /tmp/uv-cache && uv run pytest -xvs tests/integration/test_full_research_workflow.py --tb=short"
```

---

## 🔄 Git コミットメッセージ規約

### プレフィックス

- `feat:` - 新機能追加
- `fix:` - バグ修正
- `docs:` - ドキュメント更新
- `test:` - テスト追加・修正
- `refactor:` - リファクタリング
- `style:` - コードスタイル修正（フォーマット等）
- `chore:` - ビルド・設定変更

### 例

```
feat: arXiv検索機能追加

- ArXivSearcherクラス実装
- XML APIパース機能
- 9個のテスト追加

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

---

## ⚠️ よくある問題と解決方法

### 問題1: GitHub Actionsでテスト失敗

**原因**: ローカルでテストせずにpushした

**解決方法**:
```bash
# 1. ローカルでテストを実行
bash .github/workflows/test-local.sh

# 2. エラーを修正

# 3. 再度テスト

# 4. 修正をコミット・push
git add .
git commit -m "fix: テスト修正"
git push
```

### 問題2: ruff formatエラー

**原因**: コードがフォーマットされていない

**解決方法**:
```bash
# フォーマット実行
uv run ruff format automated_research/

# コミット
git add automated_research/
git commit -m "style: ruff format適用"
```

### 問題3: テストファイルがgitに追加されていない

**原因**: `git add` 忘れ

**解決方法**:
```bash
# 未追跡ファイルを確認
git status

# テストファイルを追加
git add tests/ci/test_*.py tests/integration/test_*.py

# コミット
git commit -m "test: テストファイル追加"
```

### 問題4: Podmanコンテナで権限エラー

**原因**: UV_CACHE_DIRの権限問題

**解決方法**:
```bash
# UV_CACHE_DIRを/tmp/に設定
podman run --rm \
  -e UV_CACHE_DIR=/tmp/uv-cache \
  ...
```

---

## 📚 参考リンク

- **PRISMA 2020**: https://www.prisma-statement.org/
- **TDD (t-wada流)**: テストを先に書いてから実装
- **Ruff**: https://docs.astral.sh/ruff/
- **Pytest**: https://docs.pytest.org/

---

## 🎯 重要なリマインダー

1. ✅ **必ずローカルでテストしてからpush**
2. ✅ **TDD: テストを先に書く**
3. ✅ **細かい粒度でコミット**
4. ✅ **コミットメッセージは明確に**
5. ✅ **ruff formatを実行**

---

**Last Updated**: 2025-10-18

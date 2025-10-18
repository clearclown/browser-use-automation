#!/bin/bash
# ローカルでGitHub Actionsのテストを実行するスクリプト

set -e

echo "🧪 ローカルテスト開始"
echo ""

echo "1️⃣ Ruff Format Check"
uv run ruff format automated_research/ --check
echo "✅ Format check passed"
echo ""

echo "2️⃣ Ruff Lint Check"
uv run ruff check automated_research/
echo "✅ Lint check passed"
echo ""

echo "3️⃣ Unit Tests"
echo "  - arXiv Search"
uv run pytest -xvs tests/ci/test_arxiv_search.py --tb=short -q
echo "  - J-STAGE Search"
uv run pytest -xvs tests/ci/test_jstage_search.py --tb=short -q
echo "  - Government Documents"
uv run pytest -xvs tests/ci/test_government_documents_search.py --tb=short -q
echo "  - Risk of Bias"
uv run pytest -xvs tests/ci/test_risk_of_bias.py --tb=short -q
echo "  - Multiple Reviewers"
uv run pytest -xvs tests/ci/test_multiple_reviewers.py --tb=short -q
echo "  - PRISMA Search"
uv run pytest -xvs tests/ci/test_prisma_search_strategy.py --tb=short -q
echo "✅ Unit tests passed"
echo ""

echo "4️⃣ Integration Tests"
uv run pytest -xvs tests/integration/test_full_research_workflow.py --tb=short -q
echo "✅ Integration tests passed"
echo ""

echo "🎉 全テスト成功！pushしても大丈夫です"

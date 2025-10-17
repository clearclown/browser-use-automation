#!/bin/bash
# Setup git branches for each research theme

set -e

# Define themes
THEMES=(
	"machine_learning"
	"cybersecurity"
	"blockchain"
	"iot"
	"quantum_computing"
)

# Get current branch
CURRENT_BRANCH=$(git branch --show-current)
echo "📍 Current branch: $CURRENT_BRANCH"

# Create branches for each theme
for THEME in "${THEMES[@]}"; do
	BRANCH_NAME="research/${THEME}"

	if git show-ref --verify --quiet "refs/heads/${BRANCH_NAME}"; then
		echo "✅ Branch already exists: $BRANCH_NAME"
	else
		echo "🌿 Creating branch: $BRANCH_NAME"
		git branch "$BRANCH_NAME"
		echo "✅ Created: $BRANCH_NAME"
	fi
done

echo ""
echo "📊 Available research branches:"
git branch | grep "research/" || echo "  (none found)"

echo ""
echo "💡 To switch to a theme branch:"
echo "   git checkout research/machine_learning"
echo ""
echo "💡 To view all branches:"
echo "   git branch -a"

#!/bin/bash

# Simple GitHub Push with Personal Access Token
# Usage: bash PUSH_WITH_TOKEN.sh

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║         GitHub Push with Personal Access Token                ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Check if in git repo
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "❌ ERROR: Not in a git repository!"
    exit 1
fi

echo "📋 Current Status:"
echo "  Repository: $(git rev-parse --show-toplevel | xargs basename)"
echo "  Branch: $(git rev-parse --abbrev-ref HEAD)"
echo "  Remote: $(git remote get-url github 2>/dev/null || echo 'github')"
echo ""

# Show commits to push
echo "📤 Commits ready to push:"
git log --oneline origin/master..HEAD 2>/dev/null | head -5 || git log --oneline -5
echo ""

# Get token
echo "🔐 AUTHENTICATION SETUP:"
echo ""
echo "You need a GitHub Personal Access Token:"
echo ""
echo "📍 To get your token:"
echo "   1. Go to: https://github.com/settings/tokens"
echo "   2. Click 'Generate new token (classic)'"
echo "   3. Give it a name: 'RSS Curation Deploy'"
echo "   4. Select scopes:"
echo "      ✓ repo (full control of private repositories)"
echo "      ✓ workflow"
echo "   5. Click 'Generate token'"
echo "   6. COPY the token (you won't see it again!)"
echo ""
echo "Token format: ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
echo ""

read -sp "Paste your GitHub Personal Access Token here: " TOKEN
echo ""

if [ -z "$TOKEN" ]; then
    echo "❌ No token provided. Push cancelled."
    exit 1
fi

echo ""
echo "⏳ Pushing to GitHub..."
echo ""

# Push with token
PUSH_URL="https://branislav1989:${TOKEN}@github.com/branislav1989/ipfs-kubo-private-public-ipfs-cluster.git"
git push "$PUSH_URL" master

# Check result
if [ $? -eq 0 ]; then
    echo ""
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║                   ✅ PUSH SUCCESSFUL! ✅                       ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
    echo ""
    echo "📊 Your files are now on GitHub!"
    echo ""
    echo "✅ Visit: https://github.com/branislav1989/ipfs-kubo-private-public-ipfs-cluster"
    echo "✅ Check: rss_curation/ folder"
    echo "✅ Check: .github/workflows/daily-link-curation.yml"
    echo ""
    echo "🤖 GitHub Actions will now run daily at 2 AM UTC!"
    echo ""
else
    echo ""
    echo "❌ Push failed. Possible reasons:"
    echo "  • Token is invalid or expired"
    echo "  • Token doesn't have 'repo' scope"
    echo "  • Network connection issue"
    echo ""
    echo "Try again:"
    echo "  bash PUSH_WITH_TOKEN.sh"
    exit 1
fi

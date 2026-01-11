#!/bin/bash
################################################################################
# Push github_deployment folder to existing GitHub repository
# Repository: https://github.com/branislav1989/ipfs-kubo-private-public-ipfs-cluster
################################################################################

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║   Push to GitHub: ipfs-kubo-private-public-ipfs-cluster      ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

REPO_URL="https://github.com/branislav1989/ipfs-kubo-private-public-ipfs-cluster.git"

# Check if we're in the right directory
if [ ! -f "README.md" ] || [ ! -f "docker-compose.yml" ]; then
    echo "❌ Error: Must run this script from github_deployment folder"
    echo ""
    echo "Please run:"
    echo "  cd github_deployment"
    echo "  ./PUSH_TO_GITHUB.sh"
    exit 1
fi

echo "📋 Step 1: Initialize Git Repository"
echo "─────────────────────────────────────────────────────────────────"
if [ ! -d ".git" ]; then
    git init
    echo "✅ Git initialized"
else
    echo "✅ Git repository already exists"
fi
echo ""

echo "📋 Step 2: Configure Git Remote"
echo "─────────────────────────────────────────────────────────────────"
if git remote get-url origin 2>/dev/null; then
    echo "Remote already configured:"
    git remote get-url origin
else
    git remote add origin "$REPO_URL"
    echo "✅ Remote added: $REPO_URL"
fi
echo ""

echo "📋 Step 3: Check Files to Commit"
echo "─────────────────────────────────────────────────────────────────"
echo "Files in this folder:"
find . -type f ! -path "./.git/*" ! -name "PUSH_TO_GITHUB.sh" | head -30
echo ""

read -p "These files look correct? (y/N): " CONFIRM
if [ "$CONFIRM" != "y" ]; then
    echo "❌ Aborted"
    exit 1
fi

echo ""
echo "📋 Step 4: Add Files to Git"
echo "─────────────────────────────────────────────────────────────────"
git add .
echo "✅ All files staged"
echo ""

echo "📋 Step 5: Review Staged Files"
echo "─────────────────────────────────────────────────────────────────"
git status
echo ""

read -p "Proceed with commit? (y/N): " PROCEED
if [ "$PROCEED" != "y" ]; then
    echo "❌ Aborted"
    exit 1
fi

echo ""
echo "📋 Step 6: Create Commit"
echo "─────────────────────────────────────────────────────────────────"
read -p "Enter commit message (or press Enter for default): " COMMIT_MSG

if [ -z "$COMMIT_MSG" ]; then
    COMMIT_MSG="Complete IPFS hosting platform with Docker deployment

Features:
- IPFS Kubo pinning (prepaid retention: 1, 2, 6, 12 months)
- IPFS Cluster (monthly subscription with 1-3 replicas)
- Bitcoin payment integration (SatSale)
- Automated billing system with grace periods
- 5GB free bandwidth per account
- Public and private IPFS networks
- Docker Compose for easy deployment
- PostgreSQL database
- Nginx reverse proxy

Pricing:
- IPFS Kubo: €0.05-€0.10/GB/month (discounts for longer retention)
- IPFS Cluster: €0.0156/GB/month per replica
- Bandwidth: 5GB free, then €0.02-€0.10/GB

Live demo: https://datahosting.company"
fi

git commit -m "$COMMIT_MSG"
echo "✅ Commit created"
echo ""

echo "📋 Step 7: Push to GitHub"
echo "─────────────────────────────────────────────────────────────────"
echo "Repository: $REPO_URL"
echo ""
echo "⚠️  You will need GitHub credentials:"
echo "   Username: branislav1989"
echo "   Password: Use Personal Access Token (not your GitHub password)"
echo ""
echo "To create a token:"
echo "   1. Go to: https://github.com/settings/tokens"
echo "   2. Click 'Generate new token (classic)'"
echo "   3. Select 'repo' scope"
echo "   4. Copy the token and use it as password"
echo ""

read -p "Ready to push? (y/N): " READY
if [ "$READY" != "y" ]; then
    echo "❌ Aborted"
    echo ""
    echo "When ready, run:"
    echo "  git push -u origin main"
    exit 1
fi

git branch -M main
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║                  ✅ SUCCESS!                                   ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
    echo ""
    echo "🌐 Your repository is live at:"
    echo "   https://github.com/branislav1989/ipfs-kubo-private-public-ipfs-cluster"
    echo ""
    echo "📦 Users can now deploy with:"
    echo "   git clone $REPO_URL"
    echo "   cd ipfs-kubo-private-public-ipfs-cluster"
    echo "   cp flask-app/.env.example flask-app/.env"
    echo "   docker-compose up -d"
    echo ""
    echo "🎉 Next Steps:"
    echo "   1. Visit your GitHub repository"
    echo "   2. Check README.md is displaying correctly"
    echo "   3. Test deployment instructions"
    echo "   4. Share your repository!"
    echo ""
else
    echo ""
    echo "❌ Push failed!"
    echo ""
    echo "Common issues:"
    echo "  1. Wrong credentials - Use Personal Access Token"
    echo "  2. Repository doesn't exist"
    echo "  3. No push permissions"
    echo ""
    echo "To retry:"
    echo "  git push -u origin main"
    echo ""
fi

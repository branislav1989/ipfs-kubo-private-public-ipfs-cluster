#!/bin/bash

# ============================================================================
# SAFE DEPLOYMENT SCRIPT FOR RSS CURATION
# Pushes Link Curator to existing GitHub repo with daily automation
# ============================================================================

echo "======================================================================"
echo "🚀 RSS CURATION - SAFE DEPLOYMENT TO GITHUB"
echo "======================================================================"
echo ""
echo "Repository: ipfs-kubo-private-public-ipfs-cluster"
echo ""

# Check if repo directory exists
if [ ! -d ".git" ]; then
    echo "❌ ERROR: Not in a git repository!"
    echo "Please cd into your repo directory and run this script again"
    exit 1
fi

# Verify we're in the right repo
REPO_NAME=$(git rev-parse --show-toplevel | xargs basename)
echo "📁 Current Repository: $REPO_NAME"
echo ""

# Check current branch
BRANCH=$(git rev-parse --abbrev-ref HEAD)
echo "📍 Current Branch: $BRANCH"
echo ""

# List what we're about to add
echo "📋 FILES TO BE ADDED:"
echo "  ✓ rss_curation/curated_links.json"
echo "  ✓ rss_curation/curated_links.md"
echo "  ✓ rss_curation/curated_links.html"
echo "  ✓ rss_curation/daily_update.sh"
echo "  ✓ rss_curation/setup_cron.sh"
echo "  ✓ rss_curation/README.md"
echo "  ✓ .github/workflows/daily-link-curation.yml"
echo ""

# Show what won't be touched
echo "🛡️  FILES THAT WON'T BE MODIFIED:"
echo "  ✓ All your existing repository files"
echo "  ✓ All other commits and history"
echo "  ✓ All configurations outside RSS curation"
echo ""

# Show automation details
echo "⚙️  DAILY AUTOMATION SETUP:"
echo "  ✓ GitHub Actions runs daily at 2:00 AM UTC"
echo "  ✓ Auto-generates curated_links (JSON, MD, HTML)"
echo "  ✓ Auto-commits and pushes daily changes"
echo "  ✓ Manual trigger available via GitHub Actions UI"
echo ""

# Check what's staged
STAGED_COUNT=$(git diff --cached --name-only | wc -l)
if [ $STAGED_COUNT -gt 0 ]; then
    echo "✅ Already staged files:"
    git diff --cached --name-only | sed 's/^/  ✓ /'
    echo ""
else
    echo "⚠️  No files staged yet"
    echo ""
fi

# Confirm before proceeding
read -p "Continue with deployment? (yes/no): " CONFIRM
if [ "$CONFIRM" != "yes" ]; then
    echo "❌ Deployment cancelled"
    exit 1
fi

echo ""
echo "======================================================================"
echo "📤 DEPLOYING..."
echo "======================================================================"
echo ""

# Check for authentication
echo "🔐 Checking GitHub authentication..."
if ! git push --dry-run github $BRANCH > /dev/null 2>&1 && ! git push --dry-run origin $BRANCH > /dev/null 2>&1; then
    echo ""
    echo "⚠️  AUTHENTICATION REQUIRED"
    echo ""
    echo "You need to authenticate with GitHub first."
    echo ""
    echo "Option 1: SSH Setup (Recommended)"
    echo "  ssh-keygen -t ed25519 -C \"your-email@gmail.com\""
    echo "  # Add key to https://github.com/settings/keys"
    echo ""
    echo "Option 2: GitHub Personal Access Token"
    echo "  git config --global credential.helper store"
    echo "  # Then run this script again and enter token when prompted"
    echo ""
    exit 1
fi

echo "✅ Authentication OK"
echo ""

# Show what will be committed
echo "✅ Stage 1: Checking changes"
echo ""
git diff --cached --stat
echo ""

# Get commit message
echo "📝 Commit Message:"
read -p "Enter message (default: '🔄 Add RSS curation with daily GitHub Actions automation'): " COMMIT_MSG
if [ -z "$COMMIT_MSG" ]; then
    COMMIT_MSG="🔄 Add RSS curation with daily GitHub Actions automation"
fi

# Commit
echo ""
echo "✅ Stage 2: Creating commit..."
git commit -m "$COMMIT_MSG" || exit 1

# Ask about push
echo ""
echo "======================================================================"
echo "✅ COMMIT CREATED SUCCESSFULLY"
echo "======================================================================"
echo ""
echo "Commit message: $COMMIT_MSG"
echo ""
echo "Next step: Push to GitHub"
read -p "Push to $BRANCH now? (yes/no): " PUSH_CONFIRM

if [ "$PUSH_CONFIRM" != "yes" ]; then
    echo "ℹ️  You can push manually later:"
    echo "   git push origin $BRANCH"
    exit 0
fi

echo ""
echo "📤 Pushing to GitHub..."
git push origin $BRANCH || git push github $BRANCH

if [ $? -eq 0 ]; then
    echo ""
    echo "======================================================================"
    echo "✅ DEPLOYMENT SUCCESSFUL!"
    echo "======================================================================"
    echo ""
    echo "🎉 Your RSS Curation is now deployed!"
    echo ""
    echo "📊 What happens next:"
    echo "  1. GitHub Actions workflow is now active"
    echo "  2. Daily automation starts at 2 AM UTC"
    echo "  3. Files auto-generated: curated_links.md, .json, .html"
    echo "  4. Changes auto-committed and pushed daily"
    echo ""
    echo "📌 Next steps:"
    echo "  1. Visit: https://github.com/branislav1989/ipfs-kubo-private-public-ipfs-cluster"
    echo "  2. Verify files in rss_curation/ folder"
    echo "  3. Check .github/workflows/daily-link-curation.yml"
    echo "  4. Go to GitHub Actions to monitor runs"
    echo ""
    echo "📂 Repository structure:"
    echo "  • rss_curation/curated_links.md - Markdown index"
    echo "  • rss_curation/curated_links.json - JSON data"
    echo "  • rss_curation/curated_links.html - HTML sitemap"
    echo "  • .github/workflows/daily-link-curation.yml - Automation"
    echo ""
    echo "🔍 To manually trigger update:"
    echo "  1. Go to GitHub Actions"
    echo "  2. Select 'Daily Link Curation Update'"
    echo "  3. Click 'Run workflow'"
    echo ""
else
    echo "❌ Push failed"
    echo "Check your git configuration and try again"
    exit 1
fi

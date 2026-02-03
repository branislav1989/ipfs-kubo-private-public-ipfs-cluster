#!/bin/bash

# Rclone Plan Upgrade Command
# Allows customers to upgrade their Rclone hosting plan interactively

set -e

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║          🚀 Rclone Hosting - Plan Upgrade Tool 🚀             ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Check if API credentials are provided
if [ -z "$API_KEY" ] || [ -z "$API_SECRET" ]; then
    echo "❌ Error: API credentials not found!"
    echo ""
    echo "Set your credentials:"
    echo "  export API_KEY='your_api_key'"
    echo "  export API_SECRET='your_api_secret'"
    echo ""
    echo "Get credentials at: https://datahosting.company/dashboard"
    exit 1
fi

# API Base URL
API_URL="https://api.datahosting.company/api"

# Step 1: Show current plan
echo "📊 Fetching your current plan..."
echo ""

CURRENT=$(curl -s "$API_URL/rclone/status" \
  -H "X-API-KEY: $API_KEY" \
  -H "X-API-SECRET: $API_SECRET")

CURRENT_PLAN=$(echo $CURRENT | jq -r '.package // "unknown"' 2>/dev/null || echo "unknown")
CURRENT_STORAGE=$(echo $CURRENT | jq -r '.storage // "N/A"' 2>/dev/null || echo "N/A")
CURRENT_REMOTES=$(echo $CURRENT | jq -r '.remotes // "N/A"' 2>/dev/null || echo "N/A")
BALANCE=$(echo $CURRENT | jq -r '.balance // "0"' 2>/dev/null || echo "0")

echo "Current Plan: $CURRENT_PLAN"
echo "Storage: $CURRENT_STORAGE"
echo "Cloud Remotes: $CURRENT_REMOTES"
echo "Balance: €$BALANCE"
echo ""

# Step 2: Show available plans
echo "📋 Available Plans:"
echo ""
echo "1️⃣  STARTER      - €8/month"
echo "    • 10GB storage"
echo "    • 5 cloud remotes"
echo "    • Email support"
echo ""
echo "2️⃣  PROFESSIONAL - €20/month"
echo "    • 50GB storage"
echo "    • 20 cloud remotes"
echo "    • Priority support"
echo ""
echo "3️⃣  ENTERPRISE   - €60/month"
echo "    • 200GB storage"
echo "    • Unlimited remotes"
echo "    • 24/7 dedicated support"
echo ""

# Step 3: Get user choice
read -p "Select new plan (1-3) or 'q' to quit: " CHOICE

case $CHOICE in
  1)
    NEW_PLAN="starter"
    NEW_COST="8.00"
    ;;
  2)
    NEW_PLAN="professional"
    NEW_COST="20.00"
    ;;
  3)
    NEW_PLAN="enterprise"
    NEW_COST="60.00"
    ;;
  q|Q)
    echo "Cancelled."
    exit 0
    ;;
  *)
    echo "❌ Invalid selection!"
    exit 1
    ;;
esac

# Step 4: Confirm upgrade
echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "📝 Upgrade Summary:"
echo "═══════════════════════════════════════════════════════════════"
echo "Current Plan: $CURRENT_PLAN → New Plan: $NEW_PLAN"
echo "Monthly Cost: €$NEW_COST"
echo ""

if [ "$CURRENT_PLAN" = "$NEW_PLAN" ]; then
    echo "⚠️  You are already on the $NEW_PLAN plan!"
    exit 0
fi

read -p "Confirm upgrade? (yes/no): " CONFIRM

if [ "$CONFIRM" != "yes" ]; then
    echo "Cancelled."
    exit 0
fi

# Step 5: Process upgrade
echo ""
echo "⏳ Processing upgrade..."

UPGRADE_RESPONSE=$(curl -s -X POST "$API_URL/rclone/upgrade-plan" \
  -H "X-API-KEY: $API_KEY" \
  -H "X-API-SECRET: $API_SECRET" \
  -H "Content-Type: application/json" \
  -d "{\"package\": \"$NEW_PLAN\"}")

STATUS=$(echo $UPGRADE_RESPONSE | jq -r '.status // "error"' 2>/dev/null)
MESSAGE=$(echo $UPGRADE_RESPONSE | jq -r '.message // "Unknown error"' 2>/dev/null)

if [ "$STATUS" = "success" ]; then
    echo ""
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║                  ✅ UPGRADE SUCCESSFUL! ✅                     ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
    echo ""
    echo "✓ Plan: $CURRENT_PLAN → $NEW_PLAN"
    echo "✓ Monthly Cost: €$NEW_COST"
    echo "✓ Effective: Immediately"
    echo ""
    echo "📊 New Details:"
    echo $UPGRADE_RESPONSE | jq '.details // empty' 2>/dev/null || echo "Plan updated"
    echo ""
    echo "💳 Note: Monthly billing will be adjusted on your next cycle"
    echo "📧 Confirmation email sent to: $(jq -r '.email // "your registered email"' <<< "$UPGRADE_RESPONSE")"
    echo ""
else
    echo ""
    echo "❌ Upgrade failed!"
    echo "Reason: $MESSAGE"
    exit 1
fi

#!/bin/bash
# Subscribe to Gitea package

read -p "API Key: " API_KEY
read -p "API Secret: " API_SECRET

echo ""
echo "Available packages:"
echo "  1. Micro (€5/month - 5GB, 10 repos)"
echo "  2. Pro (€15/month - 25GB, 50 repos)"
echo "  3. Enterprise (€50/month - 100GB, unlimited)"
echo ""
read -p "Select package (1-3): " CHOICE

case $CHOICE in
  1) PACKAGE="micro" ;;
  2) PACKAGE="pro" ;;
  3) PACKAGE="enterprise" ;;
  *) echo "Invalid choice"; exit 1 ;;
esac

echo "Subscribing to $PACKAGE..."
RESPONSE=$(curl -s -X POST https://api.datahosting.company/api/gitea/subscribe \
  -H "X-API-KEY: $API_KEY" \
  -H "X-API-SECRET: $API_SECRET" \
  -H "Content-Type: application/json" \
  -d "{\"package\": \"$PACKAGE\"}")

echo "$RESPONSE" | jq .

BITCOIN_ADDRESS=$(echo $RESPONSE | jq -r '.bitcoin_address')
GITEA_USERNAME=$(echo $RESPONSE | jq -r '.gitea_username')

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "PAYMENT INSTRUCTIONS:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Send Bitcoin to: $BITCOIN_ADDRESS"
echo ""
echo "Your Gitea credentials:"
echo "  Username: $GITEA_USERNAME"
echo "  Password: $API_SECRET"
echo "  URL: https://git.datahosting.company"
echo ""
echo "After payment (1-2 min), use ./check-status.sh"

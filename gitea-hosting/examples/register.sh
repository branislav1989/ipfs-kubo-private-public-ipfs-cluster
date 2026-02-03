#!/bin/bash
# Register for DataHosting Gitea account

echo "DataHosting Gitea - Registration"
echo ""
read -p "Enter your email: " EMAIL

echo "Registering..."
RESPONSE=$(curl -s -X POST https://api.datahosting.company/api/register \
  -H "Content-Type: application/json" \
  -d "{\"email\": \"$EMAIL\"}")

echo "$RESPONSE" | jq .

# Save credentials
API_KEY=$(echo $RESPONSE | jq -r '.api_key')
API_SECRET=$(echo $RESPONSE | jq -r '.api_secret')

echo ""
echo "SAVE THESE CREDENTIALS:"
echo "API Key: $API_KEY"
echo "API Secret: $API_SECRET"
echo ""
echo "Next: Run ./subscribe.sh to subscribe to Gitea"

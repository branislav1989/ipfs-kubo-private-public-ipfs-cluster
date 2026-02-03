#!/bin/bash
# Check Gitea account status

read -p "API Key: " API_KEY
read -p "API Secret: " API_SECRET

curl -s https://api.datahosting.company/api/gitea/status \
  -H "X-API-KEY: $API_KEY" \
  -H "X-API-SECRET: $API_SECRET" | jq .

# 🚀 Gitea Hosting - Quick Start Guide

Get your Git hosting running in **5 minutes**!

---

## Step 1: Register Account

```bash
curl -X POST https://api.datahosting.company/api/register \
  -H "Content-Type: application/json" \
  -d '{"email": "your@email.com"}'
```

**Response:**
```json
{
  "api_key": "abc123def456",
  "api_secret": "secret789xyz",
  "dashboard_url": "https://datahosting.company/dashboard/abc123def456"
}
```

**Save these!** You'll need them for everything.

---

## Step 2: View Available Packages

```bash
curl https://api.datahosting.company/api/gitea/packages
```

**Shows:**
- Micro: €5/month (5GB, 10 repos)
- Pro: €15/month (25GB, 50 repos)
- Enterprise: €50/month (100GB, unlimited)

---

## Step 3: Subscribe to Gitea

```bash
curl -X POST https://api.datahosting.company/api/gitea/subscribe \
  -H "X-API-KEY: abc123def456" \
  -H "X-API-SECRET: secret789xyz" \
  -H "Content-Type: application/json" \
  -d '{"package": "micro"}'
```

**Response:**
```json
{
  "status": "success",
  "package": "micro",
  "monthly_cost": 5.00,
  "gitea_username": "user_abc123",
  "gitea_password": "secret789xyz",
  "gitea_url": "https://git.datahosting.company",
  "bitcoin_address": "bc1q...",
  "message": "Add credits to activate your account"
}
```

---

## Step 4: Add Credits (Bitcoin)

Send Bitcoin to the address provided in Step 3.

**Payment automatically detected within 1-2 minutes!**

Check balance:
```bash
curl https://api.datahosting.company/api/gitea/status \
  -H "X-API-KEY: abc123def456" \
  -H "X-API-SECRET: secret789xyz"
```

---

## Step 5: Start Using Git!

### Option A: Web Interface

1. Go to: https://git.datahosting.company
2. Login with:
   - Username: `user_abc123` (from Step 3)
   - Password: `secret789xyz` (your API secret)

### Option B: Git Command Line

```bash
# Clone a repository
git clone https://user_abc123:secret789xyz@git.datahosting.company/user_abc123/my-repo.git

# Or configure Git to remember credentials
git config --global credential.helper store

# Then just use normal Git commands
cd my-project
git init
git add .
git commit -m "Initial commit"
git remote add origin https://git.datahosting.company/user_abc123/my-project.git
git push -u origin master
```

---

## Complete Example Script

```bash
#!/bin/bash

# 1. Register
RESPONSE=$(curl -s -X POST https://api.datahosting.company/api/register \
  -H "Content-Type: application/json" \
  -d '{"email": "john@example.com"}')

API_KEY=$(echo $RESPONSE | jq -r '.api_key')
API_SECRET=$(echo $RESPONSE | jq -r '.api_secret')

echo "API Key: $API_KEY"
echo "API Secret: $API_SECRET"

# 2. Subscribe to Gitea
GITEA_RESPONSE=$(curl -s -X POST https://api.datahosting.company/api/gitea/subscribe \
  -H "X-API-KEY: $API_KEY" \
  -H "X-API-SECRET: $API_SECRET" \
  -H "Content-Type: application/json" \
  -d '{"package": "micro"}')

GITEA_USERNAME=$(echo $GITEA_RESPONSE | jq -r '.gitea_username')
BITCOIN_ADDRESS=$(echo $GITEA_RESPONSE | jq -r '.bitcoin_address')

echo "Gitea Username: $GITEA_USERNAME"
echo "Bitcoin Address: $BITCOIN_ADDRESS"
echo "Send Bitcoin to: $BITCOIN_ADDRESS"

# 3. Wait for payment
echo "Waiting for payment..."
sleep 120

# 4. Check status
curl -s https://api.datahosting.company/api/gitea/status \
  -H "X-API-KEY: $API_KEY" \
  -H "X-API-SECRET: $API_SECRET" | jq

# 5. Clone/create first repo
cd ~/projects/my-project
git init
git add .
git commit -m "Initial commit"
git remote add origin https://$GITEA_USERNAME:$API_SECRET@git.datahosting.company/$GITEA_USERNAME/my-project.git
git push -u origin master

echo "Done! Your repo is live at:"
echo "https://git.datahosting.company/$GITEA_USERNAME/my-project"
```

---

## Next Steps

- **[API Reference](./API.md)** - Complete API docs
- **[Examples](./examples/)** - More example scripts
- **[Security](./SECURITY.md)** - Abuse prevention
- **[Support](mailto:branislavusjak1989@gmail.com)** - Get help

---

## Troubleshooting

### "Access denied" when pushing
- Check your balance: Account may be suspended
- Verify credentials: Username = API key, Password = API secret

### "Repository not found"
- Create repo via web interface first
- Check repo name spelling

### Payment not detected
- Wait 2-3 minutes (Bitcoin confirmation time)
- Check Bitcoin address is correct
- Contact support if still not credited

---

**Need help?** Email: branislavusjak1989@gmail.com


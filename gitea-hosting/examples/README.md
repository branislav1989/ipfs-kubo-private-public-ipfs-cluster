# Example Scripts

Copy-paste ready bash scripts for common operations.

## Available Scripts

### 1. register.sh
Register for a new account.
```bash
./register.sh
```

### 2. subscribe.sh
Subscribe to a Gitea package.
```bash
./subscribe.sh
```

### 3. check-status.sh
Check your account status and balance.
```bash
./check-status.sh
```

### 4. git-usage.sh
Get Git command examples for your account.
```bash
./git-usage.sh
```

## Quick One-Liner

```bash
# Register + Subscribe + Check Status
curl -X POST https://api.datahosting.company/api/register -d '{"email":"me@test.com"}' | \
  tee /tmp/reg.json && \
  curl -X POST https://api.datahosting.company/api/gitea/subscribe \
    -H "X-API-KEY: $(jq -r .api_key /tmp/reg.json)" \
    -H "X-API-SECRET: $(jq -r .api_secret /tmp/reg.json)" \
    -d '{"package":"micro"}'
```

## Requirements

- `curl` - HTTP client
- `jq` - JSON processor (optional, for prettier output)

Install jq:
```bash
sudo apt-get install jq  # Debian/Ubuntu
brew install jq          # macOS
```

# 🔧 Gitea Hosting - Self-Hosted Git Repository Management

**Privacy-focused Git hosting with Bitcoin payments. No credit cards, no tracking, no hassle.**

🌐 **Website:** [datahosting.company](https://datahosting.company)  
🔐 **Gitea Instance:** [git.datahosting.company](https://git.datahosting.company)  
📧 **Support:** branislavusjak1989@gmail.com

---

## 🚀 Quick Start

```bash
# 1. Register account
curl -X POST https://api.datahosting.company/api/register \
  -H "Content-Type: application/json" \
  -d '{"email": "you@example.com"}'

# 2. Subscribe to Gitea package
curl -X POST https://api.datahosting.company/api/gitea/subscribe \
  -H "X-API-KEY: your_api_key" \
  -H "X-API-SECRET: your_api_secret" \
  -d '{"package": "micro"}'

# 3. Pay with Bitcoin (address provided in response)
# 4. Start using Git!
git clone https://username:password@git.datahosting.company/repo.git
```

📖 **[Full Quick Start Guide](./QUICK_START.md)**

---

## 💰 Pricing

### Account Packages

| Package | Monthly | Storage | Repos | Developers | Retention |
|---------|---------|---------|-------|------------|-----------|
| **Micro** | €5 | 5 GB | 10 | 1 | 7 days |
| **Pro** | €15 | 25 GB | 50 | 10 | 30 days |
| **Enterprise** | €50 | 100 GB | Unlimited | Unlimited | 90 days |

### Developer Access (Collaborators)

| Tier | Monthly | Access To |
|------|---------|-----------|
| Micro Dev | €2 | Micro accounts |
| Pro Dev | €3 | Pro accounts |
| Enterprise Dev | €5 | Enterprise accounts |

### Storage Overages

- Micro: €0.10/GB/month
- Pro: €0.08/GB/month
- Enterprise: €0.05/GB/month

---

## ✨ Features

### ✅ What's Included

- **Private & Public Repositories** - Unlimited within storage limits
- **Issue Tracking** - Built-in bug tracking and project management
- **Wiki Documentation** - Markdown-based documentation for each repo
- **Webhooks** - Integrate with CI/CD and notification services
- **GitHub Mirroring** - Automatic backup from GitHub repositories
- **Web-Based Interface** - Browse code, manage repos via web UI
- **SSH & HTTPS Access** - Full Git protocol support
- **LFS Support** (Pro/Enterprise) - Large File Storage for binary files
- **Custom Domains** (Pro/Enterprise) - Use your own domain
- **SSO/LDAP** (Enterprise) - Enterprise authentication

### ❌ What's NOT Included

- **CI/CD Runners** - To prevent server resource abuse
- **Automated Builds** - Use external CI/CD services if needed
- **Container Registry** - Not available
- **Package Registry** - Not available

---

## 🔒 Security & Privacy

- **Bitcoin Payments Only** - No credit cards, no personal info required
- **Europe-Based** - GDPR compliant, data stays in Europe
- **Self-Hosted** - Your code, your control
- **No Tracking** - We don't track or analyze your code
- **Zero Balance Protection** - 15-day grace period before deletion

---

## 🆚 Why Choose Us Over GitHub/GitLab?

| Feature | DataHosting Gitea | GitHub | GitLab |
|---------|-------------------|--------|--------|
| **Payment** | Bitcoin only | Credit card | Credit card |
| **Privacy** | High (EU, no tracking) | Low (US, analytics) | Medium |
| **Price** | €5-50/month | $4-21/user | $29-99/user |
| **Per-User Cost** | Flat rate | Per user | Per user |
| **Self-Hosted** | Yes | No | Self-host available |
| **CI/CD** | No (lightweight) | Yes | Yes |

**Best for:**
- 💰 Small budgets (cheaper than GitHub/GitLab)
- 🔐 Privacy-conscious developers
- ₿ Bitcoin holders
- 🚫 Users who want NO credit cards
- 🌍 European customers (GDPR)

---

## 📚 Documentation

- **[Quick Start Guide](./QUICK_START.md)** - Get started in 5 minutes
- **[API Reference](./API.md)** - Complete API documentation
- **[Security Configuration](./SECURITY.md)** - Abuse prevention details
- **[Example Scripts](./examples/)** - Copy-paste bash examples

---

## 🛠️ How It Works

### 1. **Same Account for Everything**
One account works for both IPFS and Gitea services. Use the same API key/secret.

### 2. **Prepaid Credits System**
- Buy Bitcoin → Send to your unique address
- Credits automatically added
- Daily automatic deductions (charged at 3 AM UTC)

### 3. **Git Authentication**
- **Web:** Username = `user_xxx`, Password = API secret
- **Git CLI:** Username = API key, Password = API secret

### 4. **Zero Balance = Suspended**
- Git operations blocked when balance reaches €0
- Dashboard remains accessible (read-only)
- 15-day grace period to add credits
- After 15 days: Repos permanently deleted

---

## 🧪 Example Usage

### Register & Subscribe
```bash
# Register
curl -X POST https://api.datahosting.company/api/register \
  -d '{"email": "dev@example.com"}'

# Subscribe to Pro package
curl -X POST https://api.datahosting.company/api/gitea/subscribe \
  -H "X-API-KEY: abc123" \
  -H "X-API-SECRET: secret789" \
  -d '{"package": "pro"}'
```

### Use Git
```bash
# Clone repository
git clone https://user_abc123:secret789@git.datahosting.company/username/repo.git

# Or configure credentials
git config --global credential.helper store
git clone https://git.datahosting.company/username/repo.git
```

### Check Status
```bash
curl https://api.datahosting.company/api/gitea/status \
  -H "X-API-KEY: abc123" \
  -H "X-API-SECRET: secret789"
```

---

## 🌟 Comparison to Competitors

### vs GitHub
- ✅ **Cheaper:** €5-50/account vs $4-21/user
- ✅ **Bitcoin payments**
- ✅ **Better privacy**
- ❌ No CI/CD (use external)
- ❌ Smaller community

### vs GitLab
- ✅ **Much cheaper:** €5-50 vs $29-99/user
- ✅ **Simpler billing**
- ✅ **Bitcoin payments**
- ❌ No CI/CD
- ❌ Fewer features

### vs Self-Hosting Gitea
- ✅ **Managed service** (we handle updates, backups, security)
- ✅ **Automatic billing**
- ✅ **Built-in GitHub mirroring**
- ❌ More expensive than pure self-hosting

---

## 📞 Support

- **Email:** branislavusjak1989@gmail.com
- **Website:** https://datahosting.company
- **Terms:** https://datahosting.company/terms

---

## 📜 License & Terms

- **Terms of Service:** [datahosting.company/terms](https://datahosting.company/terms)
- **No CI/CD to prevent abuse**
- **15-day grace period for zero balance**
- **All prices in EUR**

---

## 🏷️ Keywords

`gitea` `self-hosted` `git-hosting` `bitcoin` `privacy` `github-alternative` `gitlab-alternative` `decentralized` `cryptocurrency` `europe` `gdpr` `no-credit-card`


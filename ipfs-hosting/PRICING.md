# 💰 IPFS Hosting - Pricing & Plan Upgrades

## Plan Comparison

| Feature | Basic | Professional | Enterprise |
|---------|-------|--------------|------------|
| **Monthly Cost** | €10 | €25 | €75 |
| **Storage** | 50GB | 100GB | 500GB |
| **Bandwidth** | 500GB/mo | 2TB/mo | Unlimited |
| **Pinning Replicas** | 1 | 3 | 5+ |
| **API Rate Limit** | 100 req/sec | 1000 req/sec | Unlimited |
| **Custom Domains** | 1 | 5 | Unlimited |
| **Support** | Email | Priority | 24/7 Dedicated |
| **SLA** | - | 99% | 99.9% |

---

## How to Upgrade Your Plan

### Option 1: Using CLI Command (Fastest)

```bash
export API_KEY="your_api_key"
export API_SECRET="your_api_secret"

bash ipfs-upgrade-plan.sh
```

### Option 2: Using API

```bash
curl -X POST https://api.datahosting.company/api/ipfs/upgrade-plan \
  -H "X-API-KEY: your_api_key" \
  -H "X-API-SECRET: your_api_secret" \
  -H "Content-Type: application/json" \
  -d '{"package": "professional"}'
```

### Option 3: Web Dashboard

1. Visit: https://datahosting.company/dashboard
2. Click "Upgrade Plan"
3. Select new plan
4. Confirm

---

## Payment Methods

- **Bitcoin:** Instant activation (Recommended)
- **Bank Transfer:** Direct EUR payment
- **Credit Card:** Coming soon

---

## Billing & Support

- Plans upgrade immediately
- Prorated billing for mid-cycle upgrades
- Annual plans: 20% discount
- Bulk discounts available (5+ accounts)

---

## Need Help?

📧 Email: branislavusjak1989@gmail.com
📚 Docs: https://datahosting.company/docs
💬 Support: https://datahosting.company/support


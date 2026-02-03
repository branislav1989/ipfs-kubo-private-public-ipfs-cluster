# 💰 Gitea Hosting - Pricing & Plan Upgrades

## Plan Comparison

| Feature | Micro | Pro | Enterprise |
|---------|-------|-----|------------|
| **Monthly Cost** | €5 | €15 | €50 |
| **Storage** | 5GB | 25GB | 100GB |
| **Repositories** | 10 | 50 | Unlimited |
| **Team Members** | 1 | 5 | Unlimited |
| **CI/CD Pipelines** | Limited | Full | Full |
| **SSL/TLS** | ✅ | ✅ | ✅ |
| **Daily Backups** | ✅ | ✅ | ✅ |
| **API Access** | ✅ | ✅ | ✅ |
| **Support** | Email | Priority | 24/7 Dedicated |
| **SLA** | - | 99% | 99.9% |

---

## Payment Methods

### Bitcoin (Recommended)
- Send Bitcoin to provided address
- Instant activation within 1-2 minutes
- Most privacy-friendly option
- No transaction fees

### Card (Coming Soon)
- Credit/Debit card support
- Automatic monthly billing
- Invoice generation
- Early 2024

### Bank Transfer
- EUR bank transfer
- Direct payment to account
- Best for enterprise customers
- Contact: branislavusjak1989@gmail.com

---

## How to Upgrade Your Plan

### Option 1: Using CLI Command (Fastest)

```bash
export API_KEY="your_api_key"
export API_SECRET="your_api_secret"

bash gitea-upgrade-plan.sh
```

The command will:
1. Show your current plan
2. Display available plans
3. Ask for confirmation
4. Process upgrade immediately
5. Show new plan details

### Option 2: Using API

```bash
curl -X POST https://api.datahosting.company/api/gitea/upgrade-plan \
  -H "X-API-KEY: your_api_key" \
  -H "X-API-SECRET: your_api_secret" \
  -H "Content-Type: application/json" \
  -d '{"package": "pro"}'
```

**Response:**
```json
{
  "status": "success",
  "old_plan": "micro",
  "new_plan": "pro",
  "monthly_cost": 15.00,
  "effective_date": "2024-02-03",
  "message": "Plan upgraded successfully"
}
```

### Option 3: Web Dashboard

1. Visit: https://datahosting.company/dashboard
2. Login with your API credentials
3. Click "Upgrade Plan"
4. Select new plan
5. Confirm

---

## Billing Details

### How Billing Works

- **Monthly Billing Cycle**: 30 days
- **First Month**: Prorated based on signup date
- **Renewals**: Automatic on day 30
- **Upgrades**: Prorated upgrade cost + remainder of month
- **Downgrades**: Refund on next cycle

### Example: Upgrading Mid-Month

**Scenario:**
- Current Plan: Micro (€5/month)
- Day: 15th of month
- Upgrade to: Pro (€15/month)

**Calculation:**
- Days remaining: 15 days
- Pro daily rate: €15/30 = €0.50/day
- Micro daily rate: €5/30 = €0.167/day
- Additional charge: (€0.50 - €0.167) × 15 = €5.00

**Your Account:**
- Immediate charge: €5.00
- New billing cycle: €15/month starting day 30

### Prepaid Credits

Instead of monthly billing, you can add prepaid credits:

```bash
# Add €100 in credits
curl -X POST https://api.datahosting.company/api/credits/add \
  -H "X-API-KEY: your_api_key" \
  -H "X-API-SECRET: your_api_secret" \
  -H "Content-Type: application/json" \
  -d '{"amount": "100", "currency": "EUR"}'
```

**Bitcoin Address Provided:**
```
bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh
```

**How Credits Work:**
- €1 credit = 1 month of Micro plan
- €3 credit = 1 month of Pro plan
- €10 credit = 1 month of Enterprise
- Proration applies to partial months
- Unused credits never expire

---

## Downgrading Plans

### Downgrade Considerations

- Effective on next billing cycle
- Data will be limited to new plan's storage
- Cannot exceed repository limits
- Support level will be reduced

### How to Downgrade

```bash
export API_KEY="your_api_key"
export API_SECRET="your_api_secret"

bash gitea-upgrade-plan.sh
```

Select lower tier plan. You'll see:
- Current usage vs. new limits
- Warning if data exceeds limits
- Effective downgrade date

---

## Cost Savings

### Annual Commitment Discount

Save 20% with annual plans:

| Plan | Monthly | Annual | Savings |
|------|---------|--------|---------|
| Micro | €5/mo | €48/yr | €12/yr |
| Pro | €15/mo | €144/yr | €36/yr |
| Enterprise | €50/mo | €480/yr | €120/yr |

**Request annual plan:**
```bash
curl -X POST https://api.datahosting.company/api/gitea/set-billing-cycle \
  -H "X-API-KEY: your_api_key" \
  -H "X-API-SECRET: your_api_secret" \
  -H "Content-Type: application/json" \
  -d '{"billing_cycle": "annual"}'
```

### Family/Bulk Discount

- 2+ accounts: 10% discount each
- 5+ accounts: 20% discount each
- 10+ accounts: 30% discount + dedicated support

Contact: branislavusjak1989@gmail.com

---

## Free Tier

### Developer Tier (Limited)

- **Cost**: €0
- **Storage**: 1GB
- **Repositories**: 3
- **Duration**: Unlimited
- **Support**: Community only

**Upgrade anytime** to paid plan for more resources.

---

## FAQ

### Q: Can I change plans anytime?
**A:** Yes! Use the CLI command or API anytime. Changes take effect immediately.

### Q: Do you offer refunds?
**A:** Unused portion of prepaid credits are refunded within 30 days of cancellation.

### Q: What happens to my data if I downgrade?
**A:** Your data remains. If you exceed new limits, you can't add more until you upgrade.

### Q: Can I switch to annual billing?
**A:** Yes! Contact support or use the API. Annual plans include 20% discount.

### Q: Is there a free trial?
**A:** Developer tier is free. Upgrade to paid plan anytime.

### Q: Do you accept corporate accounts?
**A:** Yes! Enterprise plan includes dedicated support. Email: branislavusjak1989@gmail.com

---

## Need Help?

📧 **Email:** branislavusjak1989@gmail.com
💬 **Support:** https://datahosting.company/support
📚 **Docs:** https://datahosting.company/docs
🐛 **Issues:** https://github.com/branislav1989/datahosting-company/issues


# 💰 Rclone Hosting - Pricing & Plan Upgrades

## Plan Comparison

| Feature | Starter | Professional | Enterprise |
|---------|---------|--------------|------------|
| **Monthly Cost** | €8 | €20 | €60 |
| **Storage** | 10GB | 50GB | 200GB |
| **Cloud Remotes** | 5 | 20 | Unlimited |
| **Concurrent Transfers** | 2 | 5 | Unlimited |
| **Bandwidth** | 100GB/mo | 500GB/mo | Unlimited |
| **API Access** | ✅ | ✅ | ✅ |
| **Scheduled Syncs** | Basic | Advanced | Full |
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

bash rclone-upgrade-plan.sh
```

The command will:
1. Show your current plan
2. Display available plans
3. Ask for confirmation
4. Process upgrade immediately
5. Show new plan details

### Option 2: Using API

```bash
curl -X POST https://api.datahosting.company/api/rclone/upgrade-plan \
  -H "X-API-KEY: your_api_key" \
  -H "X-API-SECRET: your_api_secret" \
  -H "Content-Type: application/json" \
  -d '{"package": "professional"}'
```

**Response:**
```json
{
  "status": "success",
  "old_plan": "starter",
  "new_plan": "professional",
  "monthly_cost": 20.00,
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
- Current Plan: Starter (€8/month)
- Day: 15th of month
- Upgrade to: Professional (€20/month)

**Calculation:**
- Days remaining: 15 days
- Professional daily rate: €20/30 = €0.67/day
- Starter daily rate: €8/30 = €0.27/day
- Additional charge: (€0.67 - €0.27) × 15 = €6.00

**Your Account:**
- Immediate charge: €6.00
- New billing cycle: €20/month starting day 30

### Prepaid Credits

Instead of monthly billing, you can add prepaid credits:

```bash
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
- €1 credit = 1 month of Starter plan
- €2.50 credit = 1 month of Professional
- €7.50 credit = 1 month of Enterprise
- Proration applies to partial months
- Unused credits never expire

---

## Downgrading Plans

### Downgrade Considerations

- Effective on next billing cycle
- Data will be limited to new plan's storage
- Cannot exceed remote limits
- Support level will be reduced

### How to Downgrade

```bash
export API_KEY="your_api_key"
export API_SECRET="your_api_secret"

bash rclone-upgrade-plan.sh
```

Select lower tier plan. You'll see:
- Current usage vs. new limits
- Warning if data exceeds limits
- Effective downgrade date

---

## Cost Savings

### Annual Commitment Discount

Save 25% with annual plans:

| Plan | Monthly | Annual | Savings |
|------|---------|--------|---------|
| Starter | €8/mo | €72/yr | €24/yr |
| Professional | €20/mo | €180/yr | €60/yr |
| Enterprise | €60/mo | €540/yr | €180/yr |

**Request annual plan:**
```bash
curl -X POST https://api.datahosting.company/api/rclone/set-billing-cycle \
  -H "X-API-KEY: your_api_key" \
  -H "X-API-SECRET: your_api_secret" \
  -H "Content-Type: application/json" \
  -d '{"billing_cycle": "annual"}'
```

### Family/Bulk Discount

- 2+ accounts: 15% discount each
- 5+ accounts: 25% discount each
- 10+ accounts: 35% discount + dedicated support

Contact: branislavusjak1989@gmail.com

---

## Free Tier

### Starter Trial (Limited)

- **Cost**: €0
- **Storage**: 2GB
- **Cloud Remotes**: 2
- **Duration**: 14 days
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
**A:** Yes! Contact support or use the API. Annual plans include 25% discount.

### Q: Is there a free trial?
**A:** Starter trial is free for 14 days. Upgrade to paid plan anytime.

### Q: Do you accept corporate accounts?
**A:** Yes! Enterprise plan includes dedicated support. Email: branislavusjak1989@gmail.com

### Q: What are cloud remotes?
**A:** Cloud remotes are connections to cloud storage services (Google Drive, AWS S3, Dropbox, etc.)

### Q: Can I use Rclone with any cloud provider?
**A:** Yes! Rclone supports 40+ cloud storage providers.

### Q: Is there bandwidth throttling?
**A:** No! We don't throttle bandwidth. Limits shown are soft limits based on fair usage.

---

## Need Help?

📧 **Email:** branislavusjak1989@gmail.com
💬 **Support:** https://datahosting.company/support
📚 **Docs:** https://datahosting.company/docs
🐛 **Issues:** https://github.com/branislav1989/datahosting-company/issues


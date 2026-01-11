# 🌐 IPFS Hosting Platform - Docker Deployment

**Open-source IPFS hosting platform with Bitcoin payments, dual-network support (public/private), and automated billing.**

🌍 **Live Demo:** https://datahosting.company  
📖 **GitHub:** https://github.com/branislav1989/ipfs-kubo-private-public-ipfs-cluster

---

## 🚀 Quick Start (Docker)

Deploy the entire platform in 3 commands:

```bash
# 1. Clone repository
git clone https://github.com/branislav1989/ipfs-kubo-private-public-ipfs-cluster.git
cd ipfs-kubo-private-public-ipfs-cluster

# 2. Configure environment
cp flask-app/.env.example flask-app/.env
nano flask-app/.env  # Edit with your settings

# 3. Start all services
docker-compose up -d
```

**Access:** http://localhost (or your server IP)

---

## ✨ Features

### 📦 IPFS Kubo Pinning (Prepaid Retention)
- **1 Month:** €0.10/GB
- **2 Months:** €0.09/GB (10% OFF)
- **6 Months:** €0.07/GB (30% OFF) ⭐
- **12 Months:** €0.05/GB (50% OFF) 🎉 BEST VALUE!
- Files automatically unpinned after retention expires
- Public and private IPFS networks supported

### 🌐 IPFS Cluster (Monthly Subscription)
- **1 Replica:** €0.0156/GB/month [€0.00052/GB/day]
- **2 Replicas:** €0.0312/GB/month [€0.00104/GB/day] ⭐ RECOMMENDED
- **3 Replicas:** €0.0468/GB/month [€0.00156/GB/day]
- Prepaid balance with automatic monthly deductions
- 7-day grace period if balance insufficient
- High availability with distributed redundancy

### 📊 Bandwidth
- **5 GB FREE** per account per month
- **Public Gateway:** €0.10/GB (after free allowance)
- **Private Gateway:** €0.02/GB (after free allowance)
- Resets monthly

### 💰 Bitcoin Payments
- Integrated SatSale payment processor
- Lightning Network support
- Automatic payment verification
- Real-time balance updates

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────┐
│           Nginx (Reverse Proxy)                 │
│         Port 80/443 - SSL/TLS Ready             │
└─────────────────┬───────────────────────────────┘
                  │
        ┌─────────┴─────────┐
        │                   │
┌───────▼────────┐  ┌──────▼──────────┐
│  Flask App     │  │   SatSale       │
│  Port 5003     │  │   Port 8000     │
│  (API/WebUI)   │  │   (Payments)    │
└───────┬────────┘  └─────────────────┘
        │
        ├───────────┬────────────┬─────────────┐
        │           │            │             │
┌───────▼─────┐ ┌──▼──────┐ ┌──▼──────┐ ┌────▼─────┐
│ PostgreSQL  │ │  IPFS   │ │  IPFS   │ │  IPFS    │
│   Database  │ │ Public  │ │ Private │ │ Cluster  │
│ Port 5432   │ │Port 5001│ │Port 5002│ │Port 9094 │
└─────────────┘ └─────────┘ └─────────┘ └──────────┘
```

---

## 📋 Prerequisites

- **Docker** 20.10+ and **Docker Compose** 2.0+
- **4GB+ RAM** (8GB recommended for production)
- **50GB+ storage** (SSD recommended)
- **Linux server** (Ubuntu 20.04+, Debian 11+, or similar)

---

## 🔧 Installation Steps

### 1. Install Docker (if not already installed)

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo apt install docker-compose-plugin

# Add user to docker group (logout/login after this)
sudo usermod -aG docker $USER
```

### 2. Clone Repository

```bash
git clone https://github.com/branislav1989/ipfs-kubo-private-public-ipfs-cluster.git
cd ipfs-kubo-private-public-ipfs-cluster
```

### 3. Configure Environment

```bash
# Copy example environment file
cp flask-app/.env.example flask-app/.env

# Edit configuration
nano flask-app/.env
```

**Important settings to change:**
- `DB_PASS` - Set a strong database password
- `FLASK_SECRET_KEY` - Generate random key: `openssl rand -hex 32`
- `ADMIN_USERNAME` and `ADMIN_PASSWORD` - Set admin credentials
- `SATSALE_API_URL` - Configure if using Bitcoin payments

### 4. Start Services

```bash
# Start all services in background
docker-compose up -d

# Check logs
docker-compose logs -f

# Check service status
docker-compose ps
```

### 5. Initialize Database

```bash
# Database is automatically initialized on first start
# Check database logs
docker-compose logs postgres
```

### 6. Access Platform

- **Website:** http://your-server-ip
- **Admin Dashboard:** http://your-server-ip/dashboard
- **IPFS Public Gateway:** http://your-server-ip:8080
- **IPFS Private Gateway:** http://your-server-ip:8081

---

## 🔐 Security Setup (Production)

### 1. SSL/TLS Certificate (Let's Encrypt)

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d yourdomain.com

# Auto-renewal (already configured)
sudo certbot renew --dry-run
```

### 2. Firewall Configuration

```bash
# Enable UFW
sudo ufw enable

# Allow SSH
sudo ufw allow 22/tcp

# Allow HTTP/HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Check status
sudo ufw status
```

### 3. Change Default Passwords

Edit `flask-app/.env`:
- Change `ADMIN_PASSWORD`
- Change `DB_PASS`
- Regenerate `FLASK_SECRET_KEY`

Then restart:
```bash
docker-compose restart
```

---

## 📊 Management Commands

### Start/Stop Services

```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# Restart specific service
docker-compose restart flask-app

# View logs
docker-compose logs -f flask-app
```

### Database Backup

```bash
# Backup database
docker-compose exec postgres pg_dump -U billing_user ipfs_billing > backup.sql

# Restore database
docker-compose exec -T postgres psql -U billing_user ipfs_billing < backup.sql
```

### Update Platform

```bash
# Pull latest changes
git pull origin main

# Rebuild and restart
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

---

## 💡 Customization

### Modify Pricing

Edit `flask-app/.env`:
```env
KUBO_PRICE_1_MONTH=0.10
KUBO_PRICE_12_MONTHS=0.05
CLUSTER_PRICE_PER_GB_MONTH=0.0156
BANDWIDTH_FREE_GB=5
```

### Modify Website Content

- **Homepage:** Edit `index.html`
- **Terms of Service:** Edit `flask-app/src/templates/terms_of_service.html`
- **Styling:** Edit `styles.css`

After changes:
```bash
docker-compose restart nginx flask-app
```

---

## 📚 Documentation

- **API Documentation:** See `docs/API.md`
- **Billing System:** See `docs/BILLING.md`
- **IPFS Configuration:** See `docs/IPFS.md`

---

## 🐛 Troubleshooting

### Services Won't Start

```bash
# Check logs
docker-compose logs

# Check disk space
df -h

# Check memory
free -h

# Restart everything
docker-compose down
docker-compose up -d
```

### Database Connection Issues

```bash
# Check postgres is running
docker-compose ps postgres

# Check logs
docker-compose logs postgres

# Verify credentials in .env match init-db.sql
```

### IPFS Not Working

```bash
# Check IPFS services
docker-compose ps ipfs-public ipfs-private

# Check IPFS logs
docker-compose logs ipfs-public

# Verify API endpoints
curl http://localhost:5001/api/v0/version
```

---

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit Pull Request

---

## 📄 License

MIT License - See [LICENSE](LICENSE) file

---

## 🔗 Links

- **Website:** https://datahosting.company
- **GitHub:** https://github.com/branislav1989/ipfs-kubo-private-public-ipfs-cluster
- **Support:** Open an issue on GitHub
- **LinkedIn:** https://www.linkedin.com/company/branislavusjak/

---

## ⭐ Star This Repository

If you find this project useful, please give it a star! ⭐

---

**Built with ❤️ for the decentralized web**

# 🌐 IPFS Kubo & Cluster — Deployment Guide + Live Hosting Service

[![Website](https://img.shields.io/badge/🌐_Live_Service-datahosting.company-blue?style=for-the-badge)](https://datahosting.company)
[![Register](https://img.shields.io/badge/Register-Free_Account-success?style=for-the-badge)](https://datahosting.company/register)
[![Pricing](https://img.shields.io/badge/Pricing-€0.05%2FGB%2Fmonth-orange?style=for-the-badge)](https://datahosting.company)

> **🚀 Live IPFS Hosting:** [https://datahosting.company](https://datahosting.company)  
> **💰 Starting at:** €0.05/GB/month (50% OFF annual plans)  
> **💳 Payment:** Bitcoin - No KYC Required  
> **📞 Support:** [branislavusjka1989@gmail.com](mailto:branislavusjka1989@gmail.com)  
> **💼 LinkedIn:** [linkedin.com/company/branislavusjak](https://www.linkedin.com/company/branislavusjak/)

---

## 📚 What's in This Repository?

This repository contains:
1. **📖 Technical Documentation** - Manual/systemd deployment guides for IPFS Kubo & Cluster
2. **🛠️ Deployment Scripts** - Systemd unit files and helper scripts
3. **📝 Articles & Tutorials** - Learn IPFS from basics to advanced
4. **🎥 Videos & Resources** - Visual guides and podcasts

**Plus:** All this powers our live hosting service at [datahosting.company](https://datahosting.company)!

---

## 🚀 Quick Start: Use Our Live Service (No Setup Required!)

**Want IPFS storage without the setup hassle?**

### Option A: Use Our Managed Service ⭐ Easiest!

1. **Register:** [datahosting.company/register](https://datahosting.company/register) (free, instant)
2. **Upload files via API** or dashboard
3. **Pay with Bitcoin** - No credit card, no KYC

**Pricing:**
| Retention | Price/GB/month | Discount | Best For |
|-----------|----------------|----------|----------|
| 1 Month   | €0.10 | - | Testing |
| 6 Months  | €0.07 | 30% OFF | Medium projects ⭐ |
| 12 Months | €0.05 | **50% OFF** | Large projects ⭐ |

**Plus:** 5 GB free bandwidth per month!

[**Start Using IPFS Now →**](https://datahosting.company/register)

---

### Option B: Self-Host (Technical Users)

Follow the deployment guide below to run your own IPFS nodes.

---

## 🛠️ Self-Hosted Deployment Guide

This repository is intentionally *not* a Docker-based deployment — the examples assume installing the binaries on the host and running nodes as systemd services.

### What You'll Deploy:
- ✅ **Public IPFS (Kubo) node** - Open to public IPFS network
- ✅ **Private IPFS (Kubo) node** - Private swarm using a `swarm.key`
- ✅ **IPFS Cluster service** - Manage pinning across multiple nodes

**IMPORTANT:** Do NOT commit real secrets (swarm keys, cluster secrets). Keep them out of source control and store them securely.

---

## 📋 Prerequisites

- Linux server(s) with systemd (Ubuntu, Debian, CentOS, etc.)
- `ipfs` (go-ipfs / Kubo) binary installed and available in PATH  
  Download: [github.com/ipfs/go-ipfs](https://github.com/ipfs/go-ipfs)
- `ipfs-cluster-service` binary  
  Download: [github.com/ipfs/ipfs-cluster](https://github.com/ipfs/ipfs-cluster)
- Basic familiarity with systemd and file system permissions

---

## 📦 What's Included

- **README.md** - This file
- **systemd/** - Example systemd unit files for public/private Kubo and IPFS Cluster
- **scripts/** - Helper scripts to initialize nodes and set up swarm keys
- **.gitignore** - Avoids committing data and secrets
- **LICENSE** - Apache-2.0 (permissive license to encourage adoption)

---

## 🚀 Quickstart (Single Host Example)

### Step 1: Install Binaries

Install go-ipfs (Kubo) and place `ipfs` in `/usr/local/bin` or similar:
```bash
# Download and install IPFS Kubo
wget https://dist.ipfs.tech/kubo/latest/kubo_linux-amd64.tar.gz
tar -xvzf kubo_linux-amd64.tar.gz
cd kubo
sudo bash install.sh
```

Install ipfs-cluster-service and ipfs-cluster-ctl:
```bash
# Download and install IPFS Cluster
wget https://dist.ipfs.tech/ipfs-cluster-service/latest/ipfs-cluster-service_linux-amd64.tar.gz
tar -xvzf ipfs-cluster-service_linux-amd64.tar.gz
cd ipfs-cluster-service
sudo cp ipfs-cluster-service /usr/local/bin/
sudo cp ipfs-cluster-ctl /usr/local/bin/
```

### Step 2: Create Data Directories

```bash
sudo mkdir -p /var/lib/ipfs/public
sudo mkdir -p /var/lib/ipfs/private
sudo mkdir -p /var/lib/ipfs-cluster
sudo mkdir -p /etc/ipfs
sudo mkdir -p /etc/ipfs-cluster
```

### Step 3: Initialize Public Node

```bash
# Initialize public IPFS node
sudo IPFS_PATH=/var/lib/ipfs/public ipfs init

# Apply server profile for production
sudo IPFS_PATH=/var/lib/ipfs/public ipfs config profile apply server
```

### Step 4: Initialize Private Node

```bash
# Initialize private IPFS node
sudo IPFS_PATH=/var/lib/ipfs/private ipfs init

# Generate swarm key for private network
echo -e "/key/swarm/psk/1.0.0/\n/base16/\n$(tr -dc 'a-f0-9' < /dev/urandom | head -c64)" | sudo tee /etc/ipfs/swarm.key

# Set secure permissions
sudo chmod 400 /etc/ipfs/swarm.key
sudo chown root:root /etc/ipfs/swarm.key

# Copy swarm key to private node
sudo cp /etc/ipfs/swarm.key /var/lib/ipfs/private/swarm.key
```

**Note:** A private swarm will only accept peers with the same `swarm.key`.

### Step 5: Initialize IPFS Cluster

```bash
# Initialize cluster with Raft consensus
sudo ipfs-cluster-service init --consensus raft --config /var/lib/ipfs-cluster

# Generate cluster secret
echo $(openssl rand -hex 32) | sudo tee /etc/ipfs-cluster/service.secret
sudo chmod 400 /etc/ipfs-cluster/service.secret
```

### Step 6: Install Systemd Units

Copy the systemd unit files from the `systemd/` folder to `/etc/systemd/system/`:

```bash
sudo cp systemd/ipfs-kubo-public.service /etc/systemd/system/
sudo cp systemd/ipfs-kubo-private.service /etc/systemd/system/
sudo cp systemd/ipfs-cluster.service /etc/systemd/system/

# Reload systemd
sudo systemctl daemon-reload

# Enable and start services
sudo systemctl enable --now ipfs-kubo-public.service
sudo systemctl enable --now ipfs-kubo-private.service
sudo systemctl enable --now ipfs-cluster.service
```

---

## ✅ Verifying Your Setup

Check that services are running:

```bash
# Check status
sudo systemctl status ipfs-kubo-public
sudo systemctl status ipfs-kubo-private
sudo systemctl status ipfs-cluster

# Check logs
sudo journalctl -u ipfs-kubo-public -f
sudo journalctl -u ipfs-kubo-private -f
sudo journalctl -u ipfs-cluster -f
```

Test API endpoints:

- **Public Kubo API:** http://127.0.0.1:5001 (or as configured)
- **Private Kubo API:** http://127.0.0.1:5002 (or as configured)
- **IPFS Cluster API:** http://127.0.0.1:9094 (or as configured)

---

## 🔒 Security & Production Notes

### Critical Security Steps:

1. **Protect Secrets:**
   - Keep `swarm.key` and cluster secrets out of git
   - Restrict file permissions to `0400` (read-only for owner)
   - Store secrets in `/etc/` directories with root ownership

2. **Network Security:**
   - Consider TLS for cluster HTTP endpoints
   - Secure the cluster RPC ports with firewall rules
   - Use VPN or private networks for cluster communication

3. **Data Protection:**
   - Use persistent, backed-up volumes for IPFS repo paths
   - Implement regular backup strategies
   - Monitor disk usage and set quotas

4. **Multi-Host Production:**
   - Run one Kubo node per host (avoid multiple daemons on same machine)
   - Bootstrap cluster peers properly
   - Use load balancers for gateway traffic
   - Implement health checks and monitoring

---

## 💡 Self-Host vs. Managed Service

### Self-Host (This Guide):
✅ Full control over infrastructure  
✅ No monthly costs (just server costs)  
✅ Learn IPFS deeply  
❌ Requires technical expertise  
❌ You manage updates, security, backups  
❌ Time-consuming setup  

### Managed Service ([DataHosting.Company](https://datahosting.company)):
✅ No setup required  
✅ Automatic updates and maintenance  
✅ Professional support  
✅ Bitcoin payments (anonymous)  
✅ 5 GB free bandwidth/month  
❌ Monthly costs (but 50% OFF with annual plans)  

**Choose based on your needs!**

---

## 🎓 Learn More About IPFS

### What is IPFS?

**IPFS (InterPlanetary File System)** is a peer-to-peer hypermedia protocol designed to make the web faster, safer, and more open.

**Key Features:**
- 🌍 **Decentralized** - Content distributed across multiple nodes
- 🔒 **Content-Addressed** - Files identified by cryptographic hashes (CIDs)
- 🚀 **Faster** - Retrieve from nearest peer, not a single server
- 💪 **Resilient** - No single point of failure
- 🔐 **Verifiable** - Content integrity guaranteed by CID

### IPFS Kubo vs IPFS Cluster

| Feature | IPFS Kubo (Single Node) | IPFS Cluster (Multi-Node) |
|---------|------------------------|---------------------------|
| **Storage** | Single server | Distributed across nodes |
| **Redundancy** | No built-in replication | Multiple replicas (1-3+) |
| **Availability** | Depends on one node | High availability |
| **Use Case** | Testing, personal files | Production, critical data |
| **Complexity** | Simple setup | Advanced configuration |

---

## 📞 Get Help & Support

### For Self-Hosting Issues:
- 📖 **Open an Issue** on this GitHub repository
- 💬 **IPFS Forums:** [discuss.ipfs.tech](https://discuss.ipfs.tech)
- 📚 **Official Docs:** [docs.ipfs.tech](https://docs.ipfs.tech)

### For Managed Service Support:
- 📧 **Email:** [branislavusjka1989@gmail.com](mailto:branislavusjka1989@gmail.com)
- 💼 **LinkedIn:** [linkedin.com/company/branislavusjak](https://www.linkedin.com/company/branislavusjak/)
- 📱 **Phone/WhatsApp/Viber:** [+421 951 044 387](tel:+421951044387)
- ⏰ **Hours:** Monday-Friday, 9:00-17:00 CET

---

## 🔧 Customization & Multi-Host Setup

If you need help:
- Customizing the systemd units
- Automating multi-host bootstrapping
- Setting up load balancers
- Implementing monitoring and alerts
- Configuring backups

**Contact us** via the homepage or LinkedIn listed above, or open an issue in this repository.

---

## 🌟 Why We Built DataHosting.Company

After deploying IPFS infrastructure for ourselves, we realized:
1. **IPFS setup is complex** - Not everyone has time to learn systemd, swarm keys, cluster configuration
2. **Maintenance is ongoing** - Updates, security patches, monitoring
3. **Costs add up** - Server costs, bandwidth, time investment

So we built [DataHosting.Company](https://datahosting.company) to offer:
- ✅ **Instant IPFS storage** - No setup, just upload
- ✅ **Affordable pricing** - 29-64% cheaper than competitors
- ✅ **Bitcoin payments** - Anonymous, no KYC
- ✅ **Professional support** - We manage everything

**Try it:** [datahosting.company/register](https://datahosting.company/register)

---

## 📊 Pricing Comparison

### Self-Host Costs (Monthly):
- Server (2 vCPU, 4GB RAM, 100GB): ~€10-20
- Bandwidth (100GB): ~€5-10
- Your time (setup + maintenance): Priceless
- **Total:** €15-30/month + significant time investment

### DataHosting.Company (Managed):
- 100GB storage (12 months): €60 upfront = **€5/month**
- Bandwidth: 5 GB free/month (€0.08/GB overage)
- Your time: 0 hours (we handle everything)
- **Total:** €5/month + no maintenance time

**For small to medium projects, managed service is cheaper and faster!**

---

## 🎯 Use Cases

### Perfect for This Guide (Self-Host):
- 🎓 Learning IPFS technology
- 🏢 Enterprise with dedicated DevOps team
- 🔬 Research projects requiring full control
- 🛠️ Custom IPFS implementations

### Perfect for Managed Service:
- 📄 Document storage and sharing
- 🌐 Static website hosting
- 🗄️ Backup and archival storage
- 📊 Data sets and CSV files
- 💼 Small business file hosting

---

## 📜 License

**Apache-2.0** - Permissive license to encourage adoption and modification.

See [LICENSE](LICENSE) file for details.

---

## ⭐ Show Your Support

If you find this repository helpful:
- ⭐ **Star this repository**
- 🔗 **Share with your network**
- 🐦 **Tweet about us**
- 💬 **Contribute** improvements or documentation

---

## 🔗 Quick Links

| Resource | Link |
|----------|------|
| **Live Service** | [datahosting.company](https://datahosting.company) |
| **Register** | [Register Free Account](https://datahosting.company/register) |
| **Pricing** | [View Pricing](https://datahosting.company/pricing) |
| **Dashboard** | [Manage Files](https://datahosting.company/dashboard) |
| **API Docs** | [API Reference](https://datahosting.company/api/pricing) |
| **IPFS Official** | [ipfs.tech](https://ipfs.tech) |
| **Support Email** | [branislavusjka1989@gmail.com](mailto:branislavusjka1989@gmail.com) |

---

<div align="center">

**Made with ❤️ for the decentralized web**

[![Website](https://img.shields.io/badge/Visit-datahosting.company-blue?style=for-the-badge)](https://datahosting.company)
[![GitHub Stars](https://img.shields.io/github/stars/branislav1989/ipfs-kubo-private-public-ipfs-cluster?style=social)](https://github.com/branislav1989/ipfs-kubo-private-public-ipfs-cluster)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Company-0A66C2?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/company/branislavusjak/)

**© 2024-2025 DataHosting.Company - Decentralized IPFS Storage**

*Self-host with this guide, or use our managed service at [datahosting.company](https://datahosting.company)*

</div>

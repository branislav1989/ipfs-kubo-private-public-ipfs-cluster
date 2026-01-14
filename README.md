# DataHosting IPFS Python SDK

Official Python SDK for [DataHosting.company](https://datahosting.company)

## Installation

```bash
pip install git+https://github.com/branislav1989/ipfs-kubo-private-public-ipfs-cluster.git#subdirectory=datahosting-sdk
```

## Get API Credentials

1. Visit [datahosting.company/register](https://datahosting.company/register)
2. Complete registration
3. Copy your **API Key** and **API Secret**

## Quick Start

```python
from datahosting import DataHostingClient

# Initialize with your credentials
client = DataHostingClient(
    api_key="your_api_key_here",
    api_secret="your_api_secret_here"
)

# Upload to IPFS Kubo (retention-based)
result = client.upload_kubo(
    file_path="document.pdf",
    is_private=False,
    retention_months=6
)
print(f"CID: {result['cid']}, Cost: €{result['cost']}")

# Upload to IPFS Cluster (monthly subscription)
result = client.upload_cluster(
    file_path="backup.zip",
    replica_count=2
)
print(f"CID: {result['cid']}")

# Check balance
balance = client.get_balance()
print(f"Kubo: €{balance['kubo_balance']}, Cluster: €{balance['cluster_balance']}")

# List your files
pins = client.list_pins()
backups = client.list_cluster_backups()
```

## Features

- IPFS Kubo pinning (1, 2, 6, 12 month retention)
- IPFS Cluster with replicas (1-3)
- Balance management
- File listing

## Pricing

- Kubo: €0.05-€0.10/GB/month
- Cluster: €0.0156/GB/month per replica
- 5GB free bandwidth/month

## Support

Email: branislavusjak1989@gmail.com
Website: https://datahosting.company

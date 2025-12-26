---
title: "IPFS Kubo (go-ipfs): Setup, configuration and best practices"
date: "2025-12-26"
summary: "Practical guide to installing Kubo (go-ipfs), configuring it for private/public networks, and operational tips."
---

Installing Kubo
- Linux (example):
  curl -O https://dist.ipfs.io/go-ipfs/v0.20.0/go-ipfs_v0.20.0_linux-amd64.tar.gz
  tar -xzf go-ipfs_*.tar.gz && cd go-ipfs && sudo bash install.sh
- Verify: ipfs --version

Initialize and run
- ipfs init
- ipfs config Addresses.API "/ip4/127.0.0.1/tcp/5001"
- ipfs daemon

Private network configuration
- Generate a swarm key for private networks using "p2p-swarm-key-gen" or provided tools.
- Place the swarm key in ~/.ipfs/swarm.key on each node.
- Restrict bootstrap peers to internal nodes and remove public bootstrappers.

Performance and maintenance
- Garbage collection: ipfs repo gc (run on schedules, careful with pinned content)
- Repo size: monitor ipfs repo stat and plan disk usage.
- Pinning strategies: combine local pinning, cluster pinning, or third-party pinning services.

Security
- Use firewalls and security groups to restrict the API and gateway ports.
- Gateways: run a reverse proxy, enable CORS carefully, and limit public write endpoints.

Observability
- Enable metrics (Prometheus) from Kubo and collect cluster metrics.
- Log retention and rotation — Kubo can run under systemd with journald or file logs.

Backup and recovery
- Periodically export pinned CIDs list with "ipfs pin ls --type=recursive" and store externally.
- Snapshot cluster state and keep offsite copies of important blocks.

Closing
These three posts form a practical starting point for both newcomers and operators. I can add images, diagrams, or split these into shorter posts and schedule a series with social-post-ready summaries. Tell me how you want them organized (folder structure, front matter format, or publishing target) and I will update the repository accordingly.
---

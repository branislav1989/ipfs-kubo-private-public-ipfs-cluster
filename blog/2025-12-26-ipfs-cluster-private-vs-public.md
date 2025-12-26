---
title: "IPFS Cluster: Private vs Public Hosting — choose the right model"
date: "2025-12-26"
summary: "How IPFS Cluster helps coordinate pinning across multiple nodes and how to run it privately or publicly."
---

IPFS Cluster is an orchestration tool that coordinates pinning across a group of IPFS nodes. It provides consensus-based replication, making it easy to ensure selected content remains available across a fleet of nodes.

Key concepts
- Pinning: instructing a node to retain a block permanently.
- Cluster peers: the set of nodes participating in replication.
- Consensus: Cluster uses Raft or CRDT-based algorithms (depending on implementation/version) to agree on the pinset.

Public cluster
- Anyone on the network can fetch and contribute content, but the cluster's replication is still controlled by cluster peers.
- Useful for shared public datasets, community caches, or distributed CDN-like setups.
- Lower management overhead for discovery but careful about content policies.

Private cluster
- Cluster communication is restricted (firewalls, private networks, or using private libp2p keys).
- Used for enterprise hosting, private archives, or regulated data.
- Ensures control over who can pin and access the cluster's internal state.

Deployment patterns
- On-premises: VMs or bare metal inside a private network with a private libp2p swarm key.
- Cloud VPC: nodes in the same VPC/subnet with strict security groups.
- Hybrid: public gateways for read-only access, cluster nodes kept private for pinning.

Quick example commands (Kubo + Cluster)
- Install and init Kubo: ipfs init && ipfs daemon
- Install cluster service (example using ipfs-cluster-service and ipfs-cluster-ctl)
- Add and pin a file from the cluster controller: ipfs-cluster-ctl add <file-or-cid>

Best practices
- Use a private swarm key for private clusters to prevent unwanted nodes.
- Monitor replication state and pin health regularly.
- Use backups/export of the cluster state for disaster recovery.

Further reading
- https://cluster.ipfs.io/
- IPFS Cluster docs and admin guides

---

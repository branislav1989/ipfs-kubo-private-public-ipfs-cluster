# IPFS Kubo (public & private) + IPFS Cluster — Manual / systemd deployment

This repository contains example instructions, systemd unit files and helper scripts to run:
- a public IPFS (Kubo) node
- a private IPFS (Kubo) node (private swarm using a `swarm.key`)
- an IPFS Cluster service to manage pinning across nodes

This repository is intentionally *not* a Docker-based deployment — the examples assume installing the binaries on the host and running nodes as systemd services.

Homepage: https://datahosting.company
Contact / LinkedIn: https://www.linkedin.com/company/branislavusjak/

IMPORTANT: Do NOT commit real secrets (swarm keys, cluster secrets). Keep them out of source control and store them securely.

Prerequisites
- Linux server(s) with systemd (Ubuntu, Debian, CentOS, etc.)
- ipfs (go-ipfs / Kubo) binary installed and available in PATH (https://github.com/ipfs/go-ipfs)
- ipfs-cluster service binary (https://github.com/ipfs/ipfs-cluster)
- Basic familiarity with systemd and file system permissions

What is included
- README.md (this file)
- systemd/ — example systemd unit files for public/private Kubo and IPFS Cluster
- scripts/ — helper scripts to initialize nodes and set up swarm keys
- .gitignore — avoids committing data and secrets
- LICENSE (Apache-2.0) — permissive license to encourage adoption

Quickstart (single host example)
1. Install binaries:
   - Install go-ipfs (Kubo) and place `ipfs` in `/usr/local/bin` or similar.
   - Install ipfs-cluster-service and ipfs-cluster-ctl and place them in `/usr/local/bin`.

2. Create data directories (example paths used below):
   - /var/lib/ipfs/public
   - /var/lib/ipfs/private
   - /var/lib/ipfs-cluster

3. Initialize the public node:
   - IPFS_PATH=/var/lib/ipfs/public ipfs init
   - (Optional) apply a server profile: IPFS_PATH=/var/lib/ipfs/public ipfs config profile apply server

4. Initialize the private node and add the swarm.key:
   - IPFS_PATH=/var/lib/ipfs/private ipfs init
   - Put your swarm.key at /etc/ipfs/swarm.key (or another secure location) and ensure permission is root:root 0400
   - Copy or symlink it to /var/lib/ipfs/private/swarm.key

   Note: a private swarm will only accept peers with the same swarm.key.

5. Initialize IPFS Cluster:
   - ipfs-cluster-service init --consensus raft --config /var/lib/ipfs-cluster
   - Put cluster secret at /etc/ipfs-cluster/service.secret (protected permissions)
   - Configure the cluster to talk to the IPFS HTTP APIs of your nodes (examples in systemd unit files)

6. Install systemd units (examples in the `systemd/` folder), then:
   - sudo systemctl daemon-reload
   - sudo systemctl enable --now ipfs-kubo-public.service
   - sudo systemctl enable --now ipfs-kubo-private.service
   - sudo systemctl enable --now ipfs-cluster.service

Verifying
- Public Kubo API: http://127.0.0.1:5001 (or as configured)
- Private Kubo API: http://127.0.0.1:5002 (or as configured)
- IPFS Cluster API: http://127.0.0.1:9094 (or as configured)
- Check logs: sudo journalctl -u ipfs-kubo-public -f

Security & production notes
- Keep `swarm.key` and cluster secrets out of git and restrict file permissions (0400).
- Consider TLS for cluster HTTP endpoints and secure the cluster RPC ports.
- Use persistent, backed-up volumes for IPFS repo paths.
- For multi-host production, run one Kubo node per host and bootstrap cluster peers rather than running multiple daemons on the same machine.

If you need help customizing the systemd units or automating multi-host bootstrapping, open an issue or contact us via the homepage or LinkedIn listed above.

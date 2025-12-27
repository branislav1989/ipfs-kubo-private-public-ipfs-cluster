# Managed IPFS Clusters for Teams — Private + Public Setup, Security, and Free Local Demo

Meta description: Practical, hands‑on guide to running private and public IPFS (Kubo) clusters for teams — includes architecture, step‑by‑step configs, security checklist, monitoring advice, cost/size guidance, and a runnable GitHub demo (no signup).

TL;DR
- Want to try IPFS clusters without signing up for any cloud service? This guide shows how teams can run private and public IPFS (Kubo) clusters, the tradeoffs, and best practices to operate them in production.
- Follow the Quick Demo section to spin up a two‑node local Kubo demo in ~10 minutes (no signup): https://github.com/<your-username>/ipfs-examples
- If you want help running this for your team, email contact@datahosting.company.

Why teams consider private + public IPFS clusters
- Data locality & compliance: Keep sensitive data on private clusters while using public gateways for distributed assets.
- Reduced vendor lock‑in: IPFS decouples content addressing from a single provider.
- Performance & caching: Use public gateways and private pinning strategies to serve frequently accessed content quickly.
- Hybrid patterns: Private clusters for internal apps; public gateways for content distribution and sharing.

Who this guide is for
- DevOps and platform engineers evaluating decentralized storage.
- Developers who need a reproducible demo to test IPFS workflows.
- Architects designing hybrid storage solutions: internal + public content distribution.

Table of contents
1. Architecture & components
2. Quick demo (run locally — no signup)
3. Step‑by‑step: Deploy a simple Kubo cluster
4. Security checklist — production considerations
5. Monitoring & maintenance
6. Cost & sizing guidelines
7. Migration & operational playbook
8. Sample (illustrative) case study
9. FAQ
10. Appendix: full docker‑compose and useful commands

1 — Architecture & components (high level)
- Kubo/go‑ipfs nodes: the IPFS daemon that stores and serves content.
- IPFS Cluster (optional): an orchestration layer to coordinate pinning across nodes.
- Bootstrap / bootstrap peers: nodes used for peer discovery in a cluster.
- Gateways: HTTP endpoints that expose /ipfs/* for retrieval (can be public or internal).
- Private swarm keys: ensure nodes join a private network (swarm key).
- Pinning & replication: decide how many replicas and which nodes hold which content.
- Access controls: API auth, gateway TLS, network policies.

Common deployment patterns
- Fully private cluster: Nodes only on private network, private swarm key, internal gateway.
- Fully public cluster: Nodes accessible via public gateways; useful for content distribution.
- Hybrid: Private cluster for sensitive data; a separate public gateway or cluster for public assets. Use a controlled replication policy to pin selected content publicly.

2 — Quick demo (run locally — no signup)
This repo is the demo: https://github.com/<your-username>/ipfs-examples

Why this is useful
- Acts as a hands‑on “try before you deploy” demo for engineers and decision makers.
- No cloud account or signup required — runs locally with Docker.
- The repo contains docker‑compose to run two go‑ipfs nodes, commands to add/pin/retrieve, and short scripts you can copy into CI or a proof‑of‑concept.

Quickstart (summary)
1. Clone the demo repo:
   git clone https://github.com/<your-username>/ipfs-examples
   cd ipfs-examples

2. Start the nodes:
   docker-compose up -d

3. Add a file to Node A and fetch from Node B's gateway. See full commands in the Appendix.

Tip: record the terminal using asciinema (asciinema.org) for a quick demo GIF you can embed into docs or videos.

3 — Step‑by‑step: Deploy a simple Kubo cluster (local → production path)
This section shows a reproducible path: local demo → small self‑hosted cluster → hardened production.

Prereqs (local test)
- Docker & docker‑compose (or Podman)
- curl and jq for API calls
- Basic network port availability

3.1 Local demo (docker‑compose)
- Use the demo repo (Appendix includes docker‑compose.yml). The compose file runs two go‑ipfs nodes with APIs exposed on different host ports and gateways on 8080/8081 for quick testing.

3.2 From local to VMs / cloud instances
- Provision 3+ VMs across availability zones (for resilience).
- Install Docker or use native binary installs for performance.
- Use a private swarm key for internal nodes to prevent accidental connections to mainnet nodes.
- Configure a load balanced public gateway (optional) behind TLS for external access.

3.3 Optional: IPFS Cluster for coordinated pinning
- IPFS Cluster (https://cluster.ipfs.io) can be used to manage replication and pinset consistency across nodes.
- Run a Cluster service with a coordination backend (e.g., RAFT) and configure each Kubo node to talk to Cluster for pin actions.

3.4 Example workflow (production)
- Developer pushes hashed content → content CID stored in DB.
- Pin workflow: trigger pin via Cluster API to the private cluster (replication = 3).
- For public assets, add pin to public gateway cluster or push to a public CDN synced with gateway output.
- Monitor replication and health via metrics.

4 — Security checklist (production)
Security is critical for teams. At minimum, implement the following:

Network & access
- Private swarm keys: use generate-swarm-key tooling; never commit keys to repos.
- VPC / firewall rules: restrict API ports (5001) to trusted hosts / management network.
- Gateway TLS: terminate TLS on the gateway; force HTTPS for external access.
- API authentication: use a reverse proxy (nginx, traefik) with basic auth or JWT for the Kubo API; don't expose the API publicly.

Data integrity & backups
- Periodic snapshot and backup of pinned content (store snapshots of metadata + replication sets).
- Offsite backups for repo metadata and any associated DBs.

Operational security
- Rotate keys/credentials periodically.
- Use least privilege for automation tokens.
- Audit logs: capture IPFS API calls (who pinned, when).

Privacy & compliance
- Evaluate content addressability vs. right to be forgotten — plan retention & removal workflows.
- For regulated data, keep sensitive content on isolated private clusters and control gateway exposure.

5 — Monitoring & maintenance
Essential signals to monitor
- Node health: daemon uptime, peer counts
- Storage usage: available disk, total pinned size
- Bandwidth: incoming/outgoing throughput
- Pin queue & success rate (if using IPFS Cluster)
- Gateway latency & error rates

Recommended tools & integrations
- Prometheus + Grafana: exporters exist for go‑ipfs (or monitor via node metrics endpoints).
- Log aggregation: centralize logs (ELK/EFK/Datadog).
- Alerting: set alerts for low disk, high pin failures, or unusual peer churn.

Maintenance tasks (weekly/monthly)
- Check pin health and replication.
- Vacuum unused or stale content (where policy allows).
- Update go‑ipfs/Kubo to latest stable releases, test in staging first.

6 — Cost & sizing guidelines
Bandwidth & storage are the key drivers:
- Storage: estimate pinned data footprint + overhead for replication factor.
- Bandwidth: consider egress-heavy workloads (static content distribution); public gateways can generate high egress costs.
- Example: 1 TB of pinned data replicated 3x = 3 TB total storage across nodes + replication overhead for garbage collection.

Sizing rules of thumb
- Start with 3 nodes for resiliency (replication=2 or 3).
- Use SSDs for nodes with high churn or large datasets.
- Scale gateways horizontally behind load balancers; keep nodes focused on pinning and storage.

7 — Migration & operational playbook
Migrating from object store to IPFS cluster (high level)
- Map content identifiers: convert existing object keys to content-addressed files (store mapping in DB).
- Batch add content to a staging cluster and verify retrieval times.
- Pin content incrementally and monitor hit rates; do not attempt a full migration in one large job unless tested.

Operational playbook (incident response)
- Pin failure: check IPFS Cluster status, retry pin, check disk space.
- Node unreachable: failover to other replicas; rehydrate replicas from other nodes or backups.
- Data corruption: verify content retrieval across multiple nodes using CID checks.

8 — Sample illustrative case study (hypothetical)
Problem: Team needed an internal file store for documents with selective public distribution for assets. They wanted reduced vendor lock‑in and compliance controls.

Solution:
- Deployed a 3‑node private IPFS cluster with a separate public gateway cluster for assets meant to be publicly accessible.
- Used IPFS Cluster to coordinate pinning and set replication=3 for critical data.
- Result: Faster internal retrieval for cached assets, better auditability, and simpler content distribution for public assets. (Illustrative metrics: internal retrieval latency down 30% for cached assets.)

9 — FAQ
Q: Does content disappear if no one pins it?
A: Yes. IPFS is content‑addressed; if no node pins an object, it can be garbage collected. Use pinning and replication to keep content available.

Q: Can I run IPFS in Kubernetes?
A: Yes — you can run go‑ipfs and IPFS Cluster in Kubernetes. Use PVCs for storage and ensure proper network config for swarm ports.

Q: Is IPFS secure by default?
A: IPFS offers building blocks. For production, you must configure private swarm keys, TLS, API access controls, and network policies.

10 — Appendix: demo README excerpt and docker‑compose (copy/paste)
Quick demo: clone the repo and run locally — no signup required.

Minimal docker‑compose (two nodes, example)
```yaml
version: "3.7"
services:
  ipfs1:
    image: ipfs/go-ipfs:latest
    container_name: ipfs1
    restart: unless-stopped
    ports:
      - "5001:5001"   # API
      - "8080:8080"   # Gateway
    volumes:
      - ./data/ipfs1:/data/ipfs

  ipfs2:
    image: ipfs/go-ipfs:latest
    container_name: ipfs2
    restart: unless-stopped
    ports:
      - "5002:5001"   # API for node2 mapped to host 5002
      - "8081:8080"   # Gateway for node2 mapped to host 8081
    volumes:
      - ./data/ipfs2:/data/ipfs
```

Useful commands (example)
- Start:
  docker-compose up -d

- Get peer ID (Node A):
  curl -s "http://localhost:5001/api/v0/id" | jq -r '.ID'

- Add a file:
  echo "Hello from datahosting.company demo" > hello.txt
  CID=$(curl -s -X POST "http://localhost:5001/api/v0/add" -F file=@hello.txt | jq -r '.Hash')
  echo "Added CID: $CID"

- Retrieve via Node B gateway:
  curl "http://localhost:8081/ipfs/${CID}"

- Stop:
  docker-compose down

Embed a terminal demo
- Record the short terminal demo with asciinema and embed the player on your blog to increase conversion. Example: asciinema.org → record → embed code snippet.

Call to action — try it now (no signup)
- Run the demo now: https://github.com/<your-username>/ipfs-examples
- Read the full downloadable configs & appendix (this page).
- Want help running this for your team? Email contact@datahosting.company for a free 30‑minute POC consultation.

Final notes & next steps
- Publish this guide as a pillar page on your site (slug: /ipfs-private-public-clusters) and put the demo repo link above the fold with a “Try demo — no signup” CTA.
- Create a short YouTube demo (6–8 min) showing the docker‑compose flow; put the repo link in the description.
- Post condensed tutorial to Dev.to and a short “run IPFS locally in 10 minutes” post to Reddit/r/ipfs. Link traffic directly to the GitHub demo for instant hands‑on experience — no signup required.

If you want, I can:
- Convert this guide into a ready‑to‑publish Markdown file tailored to your site’s template (I can insert your GitHub repo URL and any company phrasing you prefer).
- Create the full GitHub README + docker‑compose files ready to push.

Tell me if you want me to:
A) Insert your GitHub repo URL (what is your GitHub username or desired repo owner?), or
B) Generate the README and files for the demo repo ready to copy into GitHub.
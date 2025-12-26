---
title: "Introduction to IPFS: Decentralized Web and Content Addressing"
date: "2025-12-26"
summary: "A practical introduction to IPFS, how content addressing works, and why it matters for the decentralized web."
---

IPFS (InterPlanetary File System) is a peer-to-peer distributed file system that seeks to connect all computing devices with the same system of files. Instead of locating files by where they are (a server URL) IPFS locates files by what they are — a content identifier (CID).

How IPFS works (high level)
- Content addressing: files are chunked, hashed, and addressed by CID.
- Merkle DAG: content is organized into a Merkle Directed Acyclic Graph ensuring integrity and de-duplication.
- Peer-to-peer network: nodes exchange blocks using libp2p and DHT for discovery.

Benefits
- Immutable addressing: the CID always refers to the same content version.
- Deduplication: identical blocks stored once regardless of filename or path.
- Offline resilience: content can be fetched from any peer that has it.
- Enables distributed apps and content delivery without centralized servers.

When to use IPFS
- Publishing immutable artifacts (releases, datasets, academic papers).
- Distributing large static assets to many users.
- Building censorship-resistant or resilient applications.

Common mistakes and gotchas
- CIDs are immutable: if you update a file you get a new CID (use IPNS or DNSLink for stable names).
- Content availability: content is available only while some node(s) pin it or cache it — use pinning services or clusters.
- Not a drop-in CDN replacement for dynamic content.

Next steps
- Try the quick start: install Kubo (go-ipfs), add a file, and cat it by CID.
- Learn about IPNS, DNSLink and pinning services.

References
- https://ipfs.tech/
- https://docs.ipfs.io/

---

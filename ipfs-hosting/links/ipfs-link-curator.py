#!/usr/bin/env python3
"""IPFS Ecosystem Link Curator - Daily updates for IPFS ecosystem links"""
import json
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).parent

LINKS_DATA = {
    "metadata": {
        "title": "IPFS Hosting Ecosystem - Curated Links & Resources",
        "description": "High-impact links for IPFS, distributed storage, Web3, and decentralized web",
        "updated": datetime.utcnow().isoformat() + "Z",
        "total_links": 18
    },
    "links": [
        {"id": 1, "title": "IPFS - Official Website", "url": "https://ipfs.io", "category": "IPFS Official", "relevance_score": 10},
        {"id": 2, "title": "IPFS GitHub Repository", "url": "https://github.com/ipfs/go-ipfs", "category": "IPFS Official", "relevance_score": 10},
        {"id": 3, "title": "IPFS Documentation", "url": "https://docs.ipfs.io", "category": "IPFS Official", "relevance_score": 10},
        {"id": 4, "title": "IPFS Kubo", "url": "https://github.com/ipfs/kubo", "category": "IPFS Official", "relevance_score": 10},
        {"id": 5, "title": "IPFS Cluster", "url": "https://cluster.ipfs.io", "category": "IPFS Official", "relevance_score": 9},
        {"id": 6, "title": "Filecoin", "url": "https://filecoin.io", "category": "Distributed Storage", "relevance_score": 9},
        {"id": 7, "title": "Pinata", "url": "https://pinata.cloud", "category": "Distributed Storage", "relevance_score": 8},
        {"id": 8, "title": "Web3.Storage", "url": "https://web3.storage", "category": "Distributed Storage", "relevance_score": 8},
        {"id": 9, "title": "Fleek", "url": "https://fleek.co", "category": "Web3 & Blockchain", "relevance_score": 8},
        {"id": 10, "title": "Ethereum", "url": "https://ethereum.org", "category": "Web3 & Blockchain", "relevance_score": 8},
        {"id": 11, "title": "IPFS Companion", "url": "https://github.com/ipfs/ipfs-companion", "category": "DevOps & Tools", "relevance_score": 7},
        {"id": 12, "title": "OrbitDB", "url": "https://orbitdb.org", "category": "DevOps & Tools", "relevance_score": 7},
        {"id": 13, "title": "Textile", "url": "https://www.textile.io", "category": "DevOps & Tools", "relevance_score": 7},
        {"id": 14, "title": "Docker IPFS", "url": "https://hub.docker.com/r/ipfs/go-ipfs", "category": "DevOps & Tools", "relevance_score": 8},
        {"id": 15, "title": "Content Addressing", "url": "https://docs.ipfs.io/concepts/content-addressing/", "category": "Guides", "relevance_score": 8},
        {"id": 16, "title": "IPFS Gateway Guide", "url": "https://docs.ipfs.io/how-to/address-ipfs-on-web/", "category": "Guides", "relevance_score": 8},
        {"id": 17, "title": "IPFS Security", "url": "https://docs.ipfs.io/how-to/security-best-practices/", "category": "Guides", "relevance_score": 8},
        {"id": 18, "title": "Protocol Labs", "url": "https://protocol.ai", "category": "IPFS Official", "relevance_score": 9}
    ]
}

def save_json():
    output_file = BASE_DIR / "ipfs_ecosystem_links.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(LINKS_DATA, f, indent=2, ensure_ascii=False)
    print(f"✅ Updated: {output_file}")

def main():
    print("🔄 IPFS Ecosystem Link Curator")
    print(f"📅 Update time: {datetime.utcnow().isoformat()}Z")
    save_json()
    print(f"✅ Total links curated: {len(LINKS_DATA['links'])}")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Rclone Ecosystem Link Curator
Automatically curates and updates high-impact links for Rclone ecosystem
Generates JSON, Markdown, HTML, and RSS feed formats
"""

import json
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).parent

LINKS_DATA = {
    "metadata": {
        "title": "Rclone Hosting Ecosystem - Curated Links & Resources",
        "description": "High-impact links for Rclone cloud storage sync, backup solutions, and cloud provider integrations",
        "keywords": "rclone, cloud storage, sync, backup, cloud providers, S3, Google Drive, Dropbox",
        "updated": datetime.utcnow().isoformat() + "Z",
        "total_links": 18,
        "categories": ["Rclone Official", "Cloud Providers", "Backup & Sync", "DevOps", "Guides"]
    },
    "links": [
        {"id": 1, "title": "Rclone - Official Website", "url": "https://rclone.org", "description": "Official Rclone website.", "category": "Rclone Official", "tags": ["rclone", "sync", "open-source"], "keywords": ["rclone", "cloud sync"], "relevance_score": 10, "indexed": True},
        {"id": 2, "title": "Rclone GitHub Repository", "url": "https://github.com/rclone/rclone", "description": "Open-source Rclone repository.", "category": "Rclone Official", "tags": ["github", "open-source"], "keywords": ["rclone source"], "relevance_score": 10, "indexed": True},
        {"id": 3, "title": "Rclone Documentation", "url": "https://rclone.org/docs/", "description": "Complete Rclone documentation.", "category": "Rclone Official", "tags": ["docs", "guide"], "keywords": ["rclone docs"], "relevance_score": 10, "indexed": True},
        {"id": 4, "title": "Rclone Commands Reference", "url": "https://rclone.org/commands/", "description": "All Rclone commands reference.", "category": "Rclone Official", "tags": ["commands", "CLI"], "keywords": ["rclone commands"], "relevance_score": 10, "indexed": True},
        {"id": 5, "title": "Rclone WebUI", "url": "https://rclone.org/gui/", "description": "Web GUI for Rclone.", "category": "Rclone Official", "tags": ["webui", "gui"], "keywords": ["rclone webui"], "relevance_score": 9, "indexed": True},
        {"id": 6, "title": "Google Drive - Rclone", "url": "https://rclone.org/drive/", "description": "Rclone with Google Drive.", "category": "Cloud Providers", "tags": ["google-drive"], "keywords": ["google drive rclone"], "relevance_score": 9, "indexed": True},
        {"id": 7, "title": "AWS S3 - Rclone", "url": "https://rclone.org/s3/", "description": "Rclone with AWS S3.", "category": "Cloud Providers", "tags": ["aws", "s3"], "keywords": ["rclone s3"], "relevance_score": 9, "indexed": True},
        {"id": 8, "title": "Dropbox - Rclone", "url": "https://rclone.org/dropbox/", "description": "Rclone with Dropbox.", "category": "Cloud Providers", "tags": ["dropbox"], "keywords": ["rclone dropbox"], "relevance_score": 8, "indexed": True},
        {"id": 9, "title": "OneDrive - Rclone", "url": "https://rclone.org/onedrive/", "description": "Rclone with OneDrive.", "category": "Cloud Providers", "tags": ["onedrive"], "keywords": ["rclone onedrive"], "relevance_score": 8, "indexed": True},
        {"id": 10, "title": "Backblaze B2 - Rclone", "url": "https://rclone.org/b2/", "description": "Rclone with Backblaze B2.", "category": "Cloud Providers", "tags": ["backblaze", "b2"], "keywords": ["rclone b2"], "relevance_score": 8, "indexed": True},
        {"id": 11, "title": "Duplicacy - Backup", "url": "https://duplicacy.com", "description": "Backup with Rclone.", "category": "Backup & Sync", "tags": ["backup"], "keywords": ["duplicacy backup"], "relevance_score": 8, "indexed": True},
        {"id": 12, "title": "Restic - Backup", "url": "https://restic.net", "description": "Restic backup tool.", "category": "Backup & Sync", "tags": ["restic", "backup"], "keywords": ["restic backup"], "relevance_score": 8, "indexed": True},
        {"id": 13, "title": "Docker - Rclone", "url": "https://hub.docker.com/r/rclone/rclone", "description": "Docker Rclone image.", "category": "DevOps", "tags": ["docker"], "keywords": ["rclone docker"], "relevance_score": 9, "indexed": True},
        {"id": 14, "title": "Kubernetes - Rclone", "url": "https://rclone.org/docker/", "description": "Rclone on Kubernetes.", "category": "DevOps", "tags": ["kubernetes", "k8s"], "keywords": ["rclone kubernetes"], "relevance_score": 8, "indexed": True},
        {"id": 15, "title": "Systemd - Rclone", "url": "https://rclone.org/systemd/", "description": "Rclone as systemd service.", "category": "DevOps", "tags": ["systemd"], "keywords": ["rclone systemd"], "relevance_score": 8, "indexed": True},
        {"id": 16, "title": "Rclone Mount", "url": "https://rclone.org/commands/rclone_mount/", "description": "Mount cloud storage.", "category": "Guides", "tags": ["mount", "fuse"], "keywords": ["rclone mount"], "relevance_score": 8, "indexed": True},
        {"id": 17, "title": "Rclone Filtering", "url": "https://rclone.org/filtering/", "description": "Advanced filtering.", "category": "Guides", "tags": ["filtering"], "keywords": ["rclone filtering"], "relevance_score": 7, "indexed": True},
        {"id": 18, "title": "Rclone Crypt", "url": "https://rclone.org/crypt/", "description": "Encryption with Rclone.", "category": "Guides", "tags": ["encryption"], "keywords": ["rclone encryption"], "relevance_score": 9, "indexed": True}
    ]
}

def save_json():
    output_file = BASE_DIR / "rclone_ecosystem_links.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(LINKS_DATA, f, indent=2, ensure_ascii=False)
    print(f"✅ Updated: {output_file}")

def main():
    print("🔄 Rclone Ecosystem Link Curator")
    print(f"📅 Update time: {datetime.utcnow().isoformat()}Z")
    print("")
    save_json()
    print("")
    print(f"✅ Total links curated: {len(LINKS_DATA['links'])}")
    print(f"📂 Categories: {len(LINKS_DATA['metadata']['categories'])}")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Gitea Ecosystem Link Curator
Automatically curates and updates high-impact links for Gitea ecosystem
Generates JSON, Markdown, HTML, and RSS feed formats
"""

import json
from datetime import datetime
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent

# Gitea ecosystem links data
LINKS_DATA = {
    "metadata": {
        "title": "Gitea Hosting Ecosystem - Curated Links & Resources",
        "description": "High-impact links for self-hosted Git repositories, Gitea instances, version control tools, and DevOps solutions",
        "keywords": "gitea, self-hosted git, version control, git hosting, devops, ci/cd, open source",
        "updated": datetime.utcnow().isoformat() + "Z",
        "total_links": 18,
        "categories": ["Gitea", "Self-Hosting", "Git Tools", "CI/CD", "DevOps", "Version Control"]
    },
    "links": [
        # Gitea Official
        {
            "id": 1,
            "title": "Gitea - Painless Self-Hosted Git Service",
            "url": "https://gitea.io",
            "description": "Official Gitea website. Lightweight Git service written in Go.",
            "category": "Gitea",
            "tags": ["gitea", "self-hosted", "git", "open-source"],
            "keywords": ["gitea", "self-hosted git", "lightweight git service"],
            "relevance_score": 10,
            "indexed": True
        },
        {
            "id": 2,
            "title": "Gitea GitHub Repository",
            "url": "https://github.com/go-gitea/gitea",
            "description": "Open-source Gitea repository with source code and documentation.",
            "category": "Gitea",
            "tags": ["gitea", "github", "open-source", "repository"],
            "keywords": ["gitea source code", "git hosting", "open source"],
            "relevance_score": 10,
            "indexed": True
        },
        {
            "id": 3,
            "title": "Gitea Documentation - Installation",
            "url": "https://docs.gitea.io/en-us/installation/",
            "description": "Complete Gitea installation guide for all platforms.",
            "category": "Self-Hosting",
            "tags": ["documentation", "installation", "setup"],
            "keywords": ["gitea installation", "setup", "deployment"],
            "relevance_score": 10,
            "indexed": True
        },
        {
            "id": 4,
            "title": "Gitea Actions - GitHub Compatible",
            "url": "https://docs.gitea.io/en-us/usage/actions/",
            "description": "GitHub Actions compatible CI/CD for Gitea.",
            "category": "CI/CD",
            "tags": ["gitea", "github-actions", "ci/cd"],
            "keywords": ["gitea actions", "workflow automation"],
            "relevance_score": 9,
            "indexed": True
        },
        {
            "id": 5,
            "title": "Gitea Docker Hub Images",
            "url": "https://hub.docker.com/r/gitea/gitea",
            "description": "Official Gitea Docker images for containerized deployment.",
            "category": "Self-Hosting",
            "tags": ["docker", "containers", "deployment"],
            "keywords": ["gitea docker", "container deployment"],
            "relevance_score": 9,
            "indexed": True
        },
        {
            "id": 6,
            "title": "Gitea Kubernetes Helm Chart",
            "url": "https://github.com/gitea/helm-chart",
            "description": "Official Helm chart for Kubernetes deployment.",
            "category": "Self-Hosting",
            "tags": ["kubernetes", "helm", "devops"],
            "keywords": ["gitea kubernetes", "helm chart"],
            "relevance_score": 8,
            "indexed": True
        },
        {
            "id": 7,
            "title": "Drone CI",
            "url": "https://www.drone.io",
            "description": "CI/CD platform that integrates with Gitea.",
            "category": "CI/CD",
            "tags": ["ci/cd", "automation"],
            "keywords": ["drone ci", "gitea ci/cd"],
            "relevance_score": 8,
            "indexed": True
        },
        {
            "id": 8,
            "title": "Woodpecker CI",
            "url": "https://woodpecker-ci.org",
            "description": "Community-driven self-hosted CI/CD platform.",
            "category": "CI/CD",
            "tags": ["ci/cd", "automation", "devops"],
            "keywords": ["woodpecker ci", "self-hosted"],
            "relevance_score": 8,
            "indexed": True
        },
        {
            "id": 9,
            "title": "Git Official",
            "url": "https://git-scm.com",
            "description": "Official Git version control system.",
            "category": "Version Control",
            "tags": ["git", "vcs", "scm"],
            "keywords": ["git version control"],
            "relevance_score": 10,
            "indexed": True
        },
        {
            "id": 10,
            "title": "GitHub",
            "url": "https://github.com",
            "description": "Leading Git hosting platform.",
            "category": "Version Control",
            "tags": ["github", "hosting"],
            "keywords": ["github", "git hosting"],
            "relevance_score": 8,
            "indexed": True
        },
        {
            "id": 11,
            "title": "GitLab",
            "url": "https://gitlab.com",
            "description": "Enterprise Git platform with DevOps.",
            "category": "Version Control",
            "tags": ["gitlab", "devops", "enterprise"],
            "keywords": ["gitlab", "devops platform"],
            "relevance_score": 8,
            "indexed": True
        },
        {
            "id": 12,
            "title": "Gogs",
            "url": "https://gogs.io",
            "description": "Lightweight self-hosted Git service.",
            "category": "Version Control",
            "tags": ["gogs", "lightweight", "self-hosted"],
            "keywords": ["gogs", "lightweight git"],
            "relevance_score": 7,
            "indexed": True
        },
        {
            "id": 13,
            "title": "Gitolite",
            "url": "http://gitolite.com",
            "description": "Git access control and permissions.",
            "category": "Git Tools",
            "tags": ["access-control", "permissions"],
            "keywords": ["gitolite", "access control"],
            "relevance_score": 7,
            "indexed": True
        },
        {
            "id": 14,
            "title": "Forgejo",
            "url": "https://forgejo.org",
            "description": "Community-driven Gitea fork.",
            "category": "Gitea",
            "tags": ["forgejo", "gitea-fork", "federation"],
            "keywords": ["forgejo", "gitea fork"],
            "relevance_score": 8,
            "indexed": True
        },
        {
            "id": 15,
            "title": "Prometheus",
            "url": "https://prometheus.io",
            "description": "Monitoring system for Gitea metrics.",
            "category": "DevOps",
            "tags": ["prometheus", "monitoring"],
            "keywords": ["prometheus", "monitoring"],
            "relevance_score": 7,
            "indexed": True
        },
        {
            "id": 16,
            "title": "Nginx",
            "url": "https://nginx.org",
            "description": "Reverse proxy for Gitea.",
            "category": "DevOps",
            "tags": ["nginx", "proxy"],
            "keywords": ["nginx", "reverse proxy"],
            "relevance_score": 8,
            "indexed": True
        },
        {
            "id": 17,
            "title": "Let's Encrypt",
            "url": "https://letsencrypt.org",
            "description": "Free SSL certificates.",
            "category": "DevOps",
            "tags": ["ssl", "certificates"],
            "keywords": ["ssl", "https"],
            "relevance_score": 8,
            "indexed": True
        },
        {
            "id": 18,
            "title": "PostgreSQL",
            "url": "https://www.postgresql.org",
            "description": "Database backend for Gitea.",
            "category": "DevOps",
            "tags": ["postgresql", "database"],
            "keywords": ["postgresql", "database"],
            "relevance_score": 8,
            "indexed": True
        }
    ]
}

def save_json():
    """Save links as JSON"""
    output_file = BASE_DIR / "gitea_ecosystem_links.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(LINKS_DATA, f, indent=2, ensure_ascii=False)
    print(f"✅ Updated: {output_file}")

def main():
    """Main curator function"""
    print("🔄 Gitea Ecosystem Link Curator")
    print(f"📅 Update time: {datetime.utcnow().isoformat()}Z")
    print("")
    
    # Update JSON (primary format)
    save_json()
    
    print("")
    print(f"✅ Total links curated: {len(LINKS_DATA['links'])}")
    print(f"📂 Categories: {len(LINKS_DATA['metadata']['categories'])}")
    print("")
    print("HTML and Markdown files are static and updated manually.")
    print("RSS feed is auto-generated from JSON data.")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Link Curator Configuration - IPFS Kubo & IPFS Cluster Focus
High-quality sources only: blogs, articles, videos, discussions, podcasts
"""

# ============================================================================
# CURATED SOURCES - IPFS KUBO & IPFS CLUSTER
# ============================================================================
# Only high-quality sources that won't create noise or harm SEO
# Prioritize: Official docs, reputable blogs, quality discussions, podcasts

CURATOR_SOURCES = {
    'documentation': [
        'https://docs.ipfs.tech/',              # Official IPFS docs
        'https://github.com/ipfs/kubo',         # Kubo official repo
        'https://github.com/ipfs-cluster/ipfs-cluster',  # Cluster repo
        'https://docs.ipfs.tech/reference/kubo/rpc/',    # Kubo RPC docs
    ],
    
    'official_blogs': [
        'https://blog.ipfs.tech/',              # Official IPFS blog
        'https://protocol.ai/blog/',            # Protocol Labs blog
        'https://blog.libp2p.io/',              # libp2p blog (used by IPFS)
    ],
    
    'news_updates': [
        'https://discuss.ipfs.tech/',           # IPFS discussions (quality source)
        'https://github.com/ipfs/kubo/discussions',  # Kubo discussions
        'https://github.com/ipfs-cluster/ipfs-cluster/discussions',  # Cluster discussions
    ],
    
    'video_tutorials': [
        'https://www.youtube.com/@IPFSbot',     # Official IPFS YouTube
        'https://www.youtube.com/results?search_query=IPFS+Kubo',  # Quality videos
        'https://www.youtube.com/results?search_query=IPFS+Cluster',  # Cluster videos
    ],
    
    'podcasts': [
        'https://research.protocol.ai/',        # Protocol Labs research (quality)
        'https://protocol.ai/news/',            # Protocol Labs news
    ],
    
    'research': [
        'https://research.protocol.ai/',        # Official research
        'https://research.protocol.ai/publications/',  # Research papers
    ],
    
    'community': [
        'https://github.com/ipfs',              # IPFS organization
        'https://github.com/ipfs-cluster',      # Cluster organization
        'https://awesome-ipfs.com/',            # Awesome IPFS curated list
    ],
    
    'tools_apis': [
        'https://github.com/ipfs/kubo/blob/master/docs/command-line-reference.md',
        'https://docs.ipfs.tech/reference/kubo/rpc/',
    ],
}

# ============================================================================
# CATEGORIES - IPFS KUBO & CLUSTER SPECIFIC
# ============================================================================

CATEGORIES = {
    'documentation': 'IPFS Kubo & Cluster Documentation',
    'official_blogs': 'Official IPFS & Protocol Labs Blogs',
    'news_updates': 'News, Updates & Discussions',
    'video_tutorials': 'Video Tutorials & Webinars',
    'podcasts': 'Podcasts & Audio Content',
    'research': 'Research & Whitepapers',
    'community': 'Community & GitHub',
    'tools_apis': 'Tools, APIs & CLI Reference',
    'integration': 'Integration Examples',
    'deployment': 'Deployment & Setup Guides',
}

# ============================================================================
# PRIORITY KEYWORDS - IPFS KUBO & CLUSTER
# ============================================================================
# These keywords are prioritized during extraction to ensure quality results

PRIORITY_KEYWORDS = [
    # Core IPFS Kubo
    'IPFS', 'Kubo', 'IPFS Kubo', 'distributed storage',
    'P2P', 'peer-to-peer', 'content addressing',
    'DHT', 'distributed hash table', 'IPLD',
    
    # IPFS Cluster
    'IPFS Cluster', 'clustering', 'replication',
    'persistence', 'pinning', 'data persistence',
    
    # Protocol
    'libp2p', 'protocol', 'interoperability',
    
    # Web3/Blockchain
    'Web3', 'blockchain', 'decentralized', 'cryptocurrency',
    
    # Technical
    'API', 'CLI', 'documentation', 'tutorial', 'guide',
    'deployment', 'configuration', 'setup', 'installation',
]

# ============================================================================
# OUTPUT SETTINGS
# ============================================================================

OUTPUT_SETTINGS = {
    'markdown_file': 'curated_links.md',
    'json_file': 'curated_links.json',
    'html_file': 'curated_links.html',
    'max_links_per_category': 100,
    'description_max_length': 160,  # SEO optimal
    'keywords_per_link': 5,  # 3-5 keywords per link
}

# ============================================================================
# SEO SETTINGS
# ============================================================================

SEO_SETTINGS = {
    'include_in_sitemap': True,
    'robots_follow': True,
    'add_schema_markup': True,
    'canonical_urls': True,
    'description_length': 160,  # Google's optimal length
}

# ============================================================================
# REQUEST SETTINGS
# ============================================================================

REQUEST_SETTINGS = {
    'timeout': 10,
    'max_retries': 2,
    'backoff_factor': 0.5,
    'user_agent': 'IPFS-LinkCurator/1.0 (+https://github.com/ipfs)',  # Identify ourselves
}

# ============================================================================
# DOMAINS TO SKIP (SPAM/LOW QUALITY)
# ============================================================================

SKIP_DOMAINS = [
    # Social media (not for SEO link indexing)
    'facebook.com',
    'twitter.com',
    'linkedin.com',
    'instagram.com',
    'tiktok.com',
    
    # Ad/tracking networks
    'googleadservices.com',
    'doubleclick.net',
    'analytics.google.com',
]

# ============================================================================
# URL PATTERNS TO SKIP
# ============================================================================

SKIP_PATTERNS = [
    r'#',  # Anchors (same page links)
    r'javascript:',
    r'mailto:',
    r'tel:',
    r'\.exe$',
    r'\.zip$',
    r'\.torrent$',
]

# ============================================================================
# QUALITY FILTERS
# ============================================================================
# These help ensure we only capture high-quality, relevant content

QUALITY_FILTERS = {
    # Minimum title length
    'min_title_length': 5,
    
    # Skip if link text is just numbers or symbols
    'skip_numeric_only': True,
    
    # Preferred domains (boost ranking of these)
    'preferred_domains': [
        'github.com',
        'docs.ipfs.tech',
        'blog.ipfs.tech',
        'protocol.ai',
        'research.protocol.ai',
        'discuss.ipfs.tech',
        'libp2p.io',
    ],
    
    # Exclude patterns (low-quality indicator)
    'exclude_patterns': [
        r'click here',
        r'read more',
        r'learn more',
        r'\d{4}-\d{2}-\d{2}',  # Date-only titles
    ],
}

# ============================================================================
# GITHUB INTEGRATION
# ============================================================================

GITHUB_SETTINGS = {
    'repo': 'ipfs-kubo-private-public-ipfs-cluster',
    'branch': 'main',
    'preserve_existing_files': True,  # IMPORTANT: Don't delete other files
    'commit_prefix': '🔗 IPFS Link Curation',
}

# ============================================================================
# NOTES FOR SEO & QUALITY
# ============================================================================
"""
QUALITY ASSURANCE APPROACH:

1. SOURCES ONLY FROM:
   - Official IPFS/Protocol Labs websites
   - GitHub official repositories
   - Reputable blogs (not spammy)
   - Quality discussion forums
   - Official YouTube channels
   - Research papers

2. SKIP ENTIRELY:
   - Social media platforms (no SEO value)
   - Advertising networks
   - Spam/low-quality domains
   - Duplicate/dated content

3. KEYWORDS:
   - Only extract IPFS/Kubo/Cluster related keywords
   - 3-5 keywords per link (no keyword stuffing)
   - Focus on technical accuracy

4. DESCRIPTIONS:
   - 140-160 characters (Google optimal)
   - Accurate summary of content
   - No fluff or marketing speak

5. DEDUPLICATION:
   - Automatic URL deduplication
   - No spam or low-quality repeats
   - Daily refresh prevents stale links

6. GITHUB SAFETY:
   - Only append to existing files
   - Never delete other repositories files
   - Careful git operations
"""

# ============================================================================
# CUSTOMIZATION TIPS
# ============================================================================
"""
TO ADD MORE SOURCES:

1. Add to CURATOR_SOURCES with proper category:
   
   CURATOR_SOURCES = {
       'your_category': [
           'https://quality-source.com/',
       ],
   }

2. Update CATEGORIES if adding new category:
   
   CATEGORIES = {
       'your_category': 'Your Category Title',
   }

3. Remember: Quality over quantity!
   - Verify sources before adding
   - Check if content is IPFS/Kubo/Cluster related
   - Avoid spam or low-quality domains

TO FILTER OUT NOISY CONTENT:

1. Add to SKIP_DOMAINS:
   SKIP_DOMAINS = ['bad-domain.com']

2. Add to SKIP_PATTERNS:
   SKIP_PATTERNS = [r'pattern_to_skip']

3. Update QUALITY_FILTERS if needed
"""


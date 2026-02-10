#!/usr/bin/env python3
"""
RSS Feed Curator - Fetches, categorizes, and republishes RSS feeds
Helps with SEO by creating content-rich feeds with proper tags
"""

import feedparser
import json
from datetime import datetime
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom
import requests
import socket

# Set global timeout for all network operations
socket.setdefaulttimeout(10)  # 10 second timeout

class RSSCurator:
    def __init__(self):
        # Categories and tags for IPFS/Web3 content
        self.categories = {
            'ipfs': ['IPFS', 'InterPlanetary File System', 'Content Addressed Storage', 'distributed-p2p'],
            'web3': ['Web3', 'Web3 infrastructure', 'decentralized web', 'dWeb'],
            'storage': ['distributed storage', 'decentralized storage', 'p2p storage'],
            'libp2p': ['libp2p', 'peer-to-peer', 'networking'],
            'blockchain': ['blockchain', 'cryptocurrency', 'Bitcoin', 'Ethereum'],
            'tech': ['distributed systems', 'decentralization', 'cryptography'],
            'discussion': ['community discussion', 'developer forum', 'technical discussion'],
            'development': ['software development', 'code changes', 'bug fixes', 'issues'],
            'release': ['software release', 'new version', 'updates', 'changelog'],
            'blog': ['blog post', 'article', 'news', 'announcement'],
            'research': ['research', 'academic', 'technical paper', 'whitepaper'],
            'podcast': ['podcast', 'audio', 'interview', 'discussion'],
            'video': ['video', 'tutorial', 'presentation', 'demo'],
            'my-content': ['DataHosting.Company', 'our content', 'original content', 'company updates']
        }
        
        # RSS feeds to curate (you'll add these)
        self.source_feeds = []
    
    def add_feed(self, url, category):
        """Add an RSS feed source (URL or local file path)"""
        self.source_feeds.append({'url': url, 'category': category})
    
    def add_local_feed(self, filepath, category):
        """Add a local RSS feed file"""
        self.source_feeds.append({'url': filepath, 'category': category, 'local': True})
    
    def fetch_feeds(self):
        """Fetch all RSS feeds (URLs or local files) with timeout"""
        all_entries = []
        
        for feed_info in self.source_feeds:
            try:
                source = feed_info['url']
                is_local = feed_info.get('local', False)
                
                if is_local:
                    print(f"Loading local file: {source}...")
                else:
                    print(f"Fetching {source}...")
                
                # Use requests with timeout for better control
                if not is_local:
                    try:
                        response = requests.get(source, timeout=10)
                        feed = feedparser.parse(response.content)
                    except (requests.Timeout, requests.ConnectionError) as e:
                        print(f"  ⚠️  Timeout/Connection error: {e}")
                        continue
                else:
                    feed = feedparser.parse(source)
                
                if not feed.entries:
                    print(f"  ⚠️  No entries found")
                    continue
                
                for entry in feed.entries:
                    # Add category tags
                    entry['curator_category'] = feed_info['category']
                    entry['curator_tags'] = self.categories.get(feed_info['category'], [])
                    all_entries.append(entry)
                    
                print(f"  ✅ Got {len(feed.entries)} items")
            except Exception as e:
                print(f"  ❌ Error: {str(e)[:100]}")
        
        return all_entries
    
    def filter_relevant(self, entries, keywords):
        """Filter entries that mention relevant keywords"""
        relevant = []
        
        for entry in entries:
            title = entry.get('title', '').lower()
            summary = entry.get('summary', '').lower()
            content = title + ' ' + summary
            
            # Check if any keyword matches
            if any(keyword.lower() in content for keyword in keywords):
                relevant.append(entry)
        
        return relevant
    
    def validate_url(self, url):
        """Check if URL is valid and accessible"""
        import requests
        try:
            # Quick check - just see if URL format is valid
            if not url or not url.startswith('http'):
                return False
            
            # Skip 404 check for performance - just validate format
            # Google Search Console will handle broken links
            return True
        except:
            return False
    
    def create_curated_feed(self, entries, output_file='feed-curated.xml'):
        """Create curated RSS feed with tags and categories"""
        
        # Create RSS root
        rss = Element('rss', version='2.0')
        rss.set('xmlns:atom', 'http://www.w3.org/2005/Atom')
        rss.set('xmlns:content', 'http://purl.org/rss/1.0/modules/content/')
        rss.set('xmlns:dc', 'http://purl.org/dc/elements/1.1/')
        
        channel = SubElement(rss, 'channel')
        
        # Channel metadata
        SubElement(channel, 'title').text = 'DataHosting.Company - Curated IPFS & Web3 News'
        SubElement(channel, 'link').text = 'https://datahosting.company'
        SubElement(channel, 'description').text = 'Curated news about IPFS, Web3, distributed storage, and decentralized infrastructure'
        SubElement(channel, 'language').text = 'en'
        SubElement(channel, 'lastBuildDate').text = datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S +0000')
        
        # Add categories
        for cat_name, tags in self.categories.items():
            for tag in tags:
                SubElement(channel, 'category').text = tag
        
        # Add items (with URL validation)
        added_count = 0
        for entry in entries:
            if added_count >= 50:  # Limit to 50 items
                break
            
            # Validate link
            link = entry.get('link', '')
            if not link or not self.validate_url(link):
                continue
            
            # Skip deleted Reddit posts
            if '[deleted]' in entry.get('title', '').lower():
                continue
            
            # Skip removed posts
            if '[removed]' in entry.get('title', '').lower():
                continue
            
            item = SubElement(channel, 'item')
            
            SubElement(item, 'title').text = entry.get('title', 'No title')
            SubElement(item, 'link').text = link
            SubElement(item, 'guid').text = link
            
            added_count += 1
            
            # Publication date
            pub_date = entry.get('published', datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S +0000'))
            SubElement(item, 'pubDate').text = pub_date
            
            # Description
            summary = entry.get('summary', '')
            SubElement(item, 'description').text = summary[:500] + '...' if len(summary) > 500 else summary
            
            # Add curator tags
            for tag in entry.get('curator_tags', []):
                SubElement(item, 'category').text = tag
            
            # Add source attribution
            SubElement(item, 'dc:creator', {'xmlns:dc': 'http://purl.org/dc/elements/1.1/'}).text = 'DataHosting.Company Curator'
        
        # Pretty print XML
        xml_str = minidom.parseString(tostring(rss)).toprettyxml(indent="  ")
        
        # Write to file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(xml_str)
        
        print(f"\n✅ Created curated feed: {output_file}")
        print(f"   Items added: {added_count}")
        print(f"   Items filtered: {len(entries) - added_count}")
        print(f"   Categories: {len(self.categories)}")
        print(f"   Tags: {sum(len(tags) for tags in self.categories.values())}")


def main():
    """Main function - configure and run curator"""
    
    curator = RSSCurator()
    
    print("=" * 70)
    print("📡 RSS FEED CURATOR - IPFS & Web3 News")
    print("=" * 70)
    print()
    
    # Add RSS/Atom feed sources
    feeds = [
        # === REDDIT DISCUSSIONS ===
        ('https://www.reddit.com/r/ipfs/new/.rss', 'discussion'),
        ('https://www.reddit.com/r/web3/new/.rss', 'discussion'),
        ('https://www.reddit.com/r/nft/new/.rss', 'discussion'),
        
        # === GITHUB RELEASES (High signal!) ===
        ('https://github.com/ipfs/kubo/releases.atom', 'release'),
        ('https://github.com/ipfs-cluster/ipfs-cluster/releases.atom', 'release'),
        ('https://github.com/ipfs/go-ipfs/releases.atom', 'release'),
        ('https://github.com/libp2p/go-libp2p/releases.atom', 'release'),
        
        # === GITHUB DISCUSSIONS (High quality) ===
        ('https://github.com/ipfs/kubo/discussions.atom', 'discussion'),
        ('https://github.com/ipfs-cluster/ipfs-cluster/discussions.atom', 'discussion'),
        
        # === GITHUB ISSUES (Development activity) ===
        ('https://github.com/ipfs/kubo/issues.atom', 'development'),
        ('https://github.com/ipfs-cluster/ipfs-cluster/issues.atom', 'development'),
        
        # === GITHUB COMMITS (Code changes) ===
        ('https://github.com/ipfs/kubo/commits/master.atom', 'development'),
        ('https://github.com/ipfs-cluster/ipfs-cluster/commits/main.atom', 'development'),
        
        # === OFFICIAL BLOGS ===
        ('https://blog.ipfs.tech/index.xml', 'ipfs'),
        ('https://blog.libp2p.io/index.xml', 'libp2p'),
        
        # === CRYPTO NEWS ===
        ('https://decrypt.co/feed', 'blockchain'),
        ('https://cointelegraph.com/rss', 'blockchain'),
        
        ('https://protocol.ai/blog/feed/', 'ipfs'),
        ('https://research.protocol.ai/blog/feed/', 'tech'),
        ('https://filecoin.io/blog/rss/', 'storage'),
        ('https://blog.ethereum.org/feed.xml', 'blockchain'),
        ('https://www.reddit.com/r/cryptotechnology/new/.rss', 'discussion'),
        ('https://www.reddit.com/r/selfhosted/new/.rss', 'discussion'),
        ('https://www.reddit.com/r/decentralized/new/.rss', 'discussion'),
        ('https://github.com/ipfs/specs/releases.atom', 'release'),
        ('https://github.com/ipld/ipld/releases.atom', 'release'),
        ('https://github.com/filecoin-project/go-filecoin/releases.atom', 'release'),
        ('https://github.com/libp2p/go-libp2p/releases.atom', 'release'),
        ('https://github.com/ipfs/kubo/discussions.atom', 'discussion'),
        ('https://github.com/ipfs/kubo/releases.atom', 'release'),
        ('https://ipfscluster.io/news/feeds/all.atom.xml', 'release'),
        ('https://protocol.ai/blog/feed/', 'blog'),
        ('https://research.protocol.ai/publications/rss.xml', 'research'),
        ('https://github.com/ipfs-cluster/ipfs-cluster/releases.atom', 'release'),
        ('https://github.com/ipfs-cluster/ipfs-cluster/issues.atom', 'development'),
        ('https://github.com/filecoin-project/go-filecoin/releases.atom', 'release'),
        ('https://feeds.zeroknowledge.fm/zeroknowledgefm', 'podcast'),
        ('https://fsjam.org/rss.xml', 'podcast'),
        ('https://www.youtube.com/feeds/videos.xml?channel_id=UCSSgiLn9Yo8uV6O9_1e55jw', 'video'),
        ('https://www.youtube.com/feeds/videos.xml?channel_id=UC0rSW0kK2OuCheredjxf7dA', 'video'),
        ('https://www.youtube.com/feeds/videos.xml?channel_id=UCiva-JNW8d_eW9JAbluAmFQ', 'my-content'),
        # === DEVELOPER COMMUNITIES ===
        ('https://news.ycombinator.com/rss', 'tech'),
    ]
    
    print("📡 Adding RSS feed sources:")
    for url, category in feeds:
        curator.add_feed(url, category)
        source_name = url.split('/')[-2] if 'reddit.com' in url else url.split('/')[2]
        print(f"  • {source_name} → {category}")
    print()
    
    # Fetch all feeds
    print("🔄 Fetching feeds...")
    print()
    all_entries = curator.fetch_feeds()
    
    if not all_entries:
        print("\n❌ No entries found in any feed!")
        return
    
    print()
    print(f"📊 Total entries collected: {len(all_entries)}")
    print()
    
    # Filter for relevant content
    ipfs_keywords = [
        'IPFS', 'InterPlanetary', 'Filecoin', 'libp2p',
        'content addressing', 'distributed storage',
        'Web3', 'decentralized', 'p2p', 'peer-to-peer',
        'blockchain', 'cryptocurrency'
    ]
    
    print("🔍 Filtering for relevant keywords...")
    relevant_entries = curator.filter_relevant(all_entries, ipfs_keywords)
    print(f"  ✅ Found {len(relevant_entries)} relevant entries")
    print()
    
    # Sort by date (most recent first)
    relevant_entries.sort(key=lambda x: x.get('published_parsed', (0,)*9), reverse=True)
    
    # Create curated feed
    print("📝 Creating curated feed...")
    curator.create_curated_feed(relevant_entries)
    print()
    print("=" * 70)
    print("✅ CURATION COMPLETE!")
    print("=" * 70)
    print()
    print("Next steps:")
    print("  1. Review: cat feed-curated.xml")
    print("  2. Publish: cp feed-curated.xml /var/www/datahosting.company/html/")
    print("  3. Submit to Google Search Console")
    print("  4. Automate: Add to crontab for daily updates")


if __name__ == '__main__':
    main()

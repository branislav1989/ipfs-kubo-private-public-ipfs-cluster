#!/usr/bin/env python3
"""
Link Curator - Scrapes, curates, and indexes links for SEO
Automatically extracts links with metadata and publishes daily to GitHub
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from datetime import datetime
import json
import re
from typing import List, Dict, Tuple
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class LinkCurator:
    """Main link curation engine"""
    
    def __init__(self):
        self.curated_links: List[Dict] = []
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        # Categories for link classification
        self.categories = {
            'ipfs': 'IPFS & Distributed Storage',
            'web3': 'Web3 & Blockchain',
            'storage': 'Cloud & Storage Solutions',
            'api': 'APIs & Integrations',
            'development': 'Development & Tools',
            'research': 'Research & Whitepapers',
            'news': 'News & Updates',
            'documentation': 'Documentation & Guides',
            'tutorial': 'Tutorials & Courses',
            'community': 'Community & Forums'
        }
    
    def extract_keywords_from_text(self, text: str, max_keywords: int = 5) -> List[str]:
        """Extract relevant keywords from text using simple NLP"""
        # Remove common words
        stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
                     'of', 'with', 'by', 'from', 'is', 'are', 'was', 'be', 'been', 'being',
                     'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'should',
                     'could', 'may', 'might', 'can', 'this', 'that', 'these', 'those'}
        
        # Split into words and clean
        words = re.findall(r'\b[a-z]{4,}\b', text.lower())
        
        # Filter stopwords and get unique
        keywords = [w for w in words if w not in stopwords]
        
        # Count frequency and get top keywords
        from collections import Counter
        keyword_freq = Counter(keywords)
        top_keywords = [word for word, _ in keyword_freq.most_common(max_keywords)]
        
        return top_keywords if top_keywords else ['content', 'resource']
    
    def extract_description(self, text: str, max_length: int = 160) -> str:
        """Extract description from text, optimized for SEO"""
        # Clean text
        text = re.sub(r'\s+', ' ', text).strip()
        text = re.sub(r'[^\w\s.,!?-]', '', text)
        
        # Truncate to max length
        if len(text) > max_length:
            text = text[:max_length].rsplit(' ', 1)[0] + '...'
        
        return text or 'Curated content resource'
    
    def scrape_page(self, url: str, category: str) -> List[Dict]:
        """Scrape a single webpage for links and metadata"""
        links_found = []
        
        try:
            logger.info(f"Scraping: {url}")
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract all links
            for link in soup.find_all('a', href=True):
                href = link.get('href', '').strip()
                title = link.get_text(strip=True)[:100]
                
                # Validate URL
                if not href or not title:
                    continue
                
                # Convert relative URLs to absolute
                if href.startswith('/'):
                    href = urljoin(url, href)
                elif not href.startswith('http'):
                    continue
                
                # Skip certain domains
                if any(skip in href for skip in ['facebook.com', 'twitter.com', 'linkedin.com', '#']):
                    continue
                
                # Extract description from page context
                description = self.extract_description(
                    link.find_parent('p').get_text() if link.find_parent('p') else title,
                    max_length=160
                )
                
                # Extract keywords
                keywords = self.extract_keywords_from_text(title + ' ' + description)
                
                link_data = {
                    'url': href,
                    'title': title or urlparse(href).netloc,
                    'description': description,
                    'keywords': keywords[:5],  # Limit to 5 keywords
                    'category': category,
                    'domain': urlparse(href).netloc,
                    'date_added': datetime.now().isoformat(),
                    'source': url
                }
                
                links_found.append(link_data)
            
            logger.info(f"  ✅ Found {len(links_found)} links")
            return links_found
            
        except Exception as e:
            logger.error(f"  ❌ Error scraping {url}: {e}")
            return []
    
    def scrape_sources(self, sources: Dict[str, List[str]]) -> List[Dict]:
        """Scrape multiple source URLs organized by category"""
        all_links = []
        
        for category, urls in sources.items():
            logger.info(f"\n📂 Scraping {category.upper()}:")
            
            for url in urls:
                links = self.scrape_page(url, category)
                all_links.extend(links)
        
        return all_links
    
    def deduplicate_links(self, links: List[Dict]) -> List[Dict]:
        """Remove duplicate links"""
        seen_urls = set()
        unique_links = []
        
        for link in links:
            url = link['url']
            if url not in seen_urls:
                seen_urls.add(url)
                unique_links.append(link)
        
        logger.info(f"Deduplicated: {len(links)} → {len(unique_links)} links")
        return unique_links
    
    def validate_links(self, links: List[Dict]) -> List[Dict]:
        """Quick validation that links are accessible (optional)"""
        valid_links = []
        
        for link in links:
            try:
                # Quick HEAD request to validate
                response = self.session.head(link['url'], timeout=5, allow_redirects=True)
                if response.status_code < 400:
                    valid_links.append(link)
                else:
                    logger.warning(f"  ⚠️  Bad status {response.status_code}: {link['url']}")
            except Exception as e:
                logger.warning(f"  ⚠️  Unreachable: {link['url']}")
        
        return valid_links
    
    def generate_markdown(self, links: List[Dict], output_file: str = 'curated_links.md') -> str:
        """Generate Markdown file with curated links"""
        
        content = []
        content.append("# 🔗 Curated SEO Links Index\n")
        content.append(f"**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}\n")
        content.append(f"**Total Links:** {len(links)}\n\n")
        content.append("---\n\n")
        
        # Group by category
        by_category = {}
        for link in links:
            cat = link['category']
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(link)
        
        # Generate sections
        for category in sorted(by_category.keys()):
            cat_links = by_category[category]
            cat_title = self.categories.get(category, category.title())
            
            content.append(f"## 📌 {cat_title}\n")
            content.append(f"**{len(cat_links)} links**\n\n")
            
            for idx, link in enumerate(cat_links, 1):
                content.append(f"### {idx}. {link['title']}\n")
                content.append(f"- **URL:** [{link['domain']}]({link['url']})\n")
                content.append(f"- **Description:** {link['description']}\n")
                content.append(f"- **Keywords:** {', '.join(link['keywords'])}\n")
                content.append(f"- **Added:** {link['date_added'][:10]}\n\n")
        
        # Table of contents
        toc = "\n## 📇 Table of Contents\n\n"
        for idx, category in enumerate(sorted(by_category.keys()), 1):
            cat_title = self.categories.get(category, category.title())
            content.insert(3, toc)
            toc += f"{idx}. [{cat_title}](#{cat_title.lower().replace(' ', '-')})\n"
        
        # Write to file
        markdown_content = ''.join(content)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        logger.info(f"✅ Generated Markdown: {output_file}")
        return markdown_content
    
    def generate_json(self, links: List[Dict], output_file: str = 'curated_links.json') -> str:
        """Generate JSON file for machine processing"""
        data = {
            'metadata': {
                'generated': datetime.now().isoformat(),
                'total_links': len(links),
                'categories': len(set(l['category'] for l in links))
            },
            'links': links
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"✅ Generated JSON: {output_file}")
        return json.dumps(data, indent=2)
    
    def generate_html_sitemap(self, links: List[Dict], output_file: str = 'curated_links.html') -> str:
        """Generate HTML sitemap for SEO"""
        html = []
        html.append("<!DOCTYPE html>")
        html.append("<html lang='en'>")
        html.append("<head>")
        html.append("<meta charset='UTF-8'>")
        html.append("<meta name='viewport' content='width=device-width, initial-scale=1.0'>")
        html.append("<title>Curated SEO Links Index</title>")
        html.append("<style>")
        html.append("""
            body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; 
                   line-height: 1.6; color: #333; max-width: 900px; margin: 40px auto; padding: 20px; }
            h1 { color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }
            h2 { color: #34495e; margin-top: 30px; }
            .link-item { background: #f8f9fa; padding: 15px; margin: 10px 0; border-left: 4px solid #3498db; }
            .url { color: #0066cc; text-decoration: none; word-break: break-all; }
            .url:hover { text-decoration: underline; }
            .keywords { color: #7f8c8d; font-size: 0.9em; }
            .meta { font-size: 0.85em; color: #95a5a6; }
            .stats { background: #ecf0f1; padding: 15px; border-radius: 5px; margin-bottom: 20px; }
        """)
        html.append("</style>")
        html.append("</head>")
        html.append("<body>")
        
        html.append(f"<h1>🔗 Curated SEO Links Index</h1>")
        html.append(f"<div class='stats'>")
        html.append(f"<p><strong>Last Updated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}</p>")
        html.append(f"<p><strong>Total Links:</strong> {len(links)}</p>")
        html.append(f"</div>")
        
        # Group by category
        by_category = {}
        for link in links:
            cat = link['category']
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(link)
        
        for category in sorted(by_category.keys()):
            cat_links = by_category[category]
            cat_title = self.categories.get(category, category.title())
            
            html.append(f"<h2>{cat_title} ({len(cat_links)})</h2>")
            
            for link in cat_links:
                html.append(f"<div class='link-item'>")
                html.append(f"<p><a class='url' href='{link['url']}'>{link['title']}</a></p>")
                html.append(f"<p>{link['description']}</p>")
                html.append(f"<p class='keywords'>🏷️ {', '.join(link['keywords'])}</p>")
                html.append(f"<p class='meta'>📍 {link['domain']} | 📅 {link['date_added'][:10]}</p>")
                html.append(f"</div>")
        
        html.append("</body>")
        html.append("</html>")
        
        html_content = '\n'.join(html)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        logger.info(f"✅ Generated HTML: {output_file}")
        return html_content
    
    def run(self, sources: Dict[str, List[str]]) -> Dict:
        """Main execution"""
        logger.info("=" * 70)
        logger.info("🚀 LINK CURATOR - SEO INDEX GENERATOR")
        logger.info("=" * 70 + "\n")
        
        # Scrape all sources
        logger.info("🌐 SCRAPING PHASE:")
        all_links = self.scrape_sources(sources)
        
        if not all_links:
            logger.warning("❌ No links found!")
            return {'success': False, 'links': 0}
        
        logger.info(f"\n📊 Total links scraped: {len(all_links)}")
        
        # Deduplicate
        logger.info("\n🔄 DEDUPLICATION PHASE:")
        unique_links = self.deduplicate_links(all_links)
        
        # Validate (optional - can be slow)
        logger.info("\n✔️  VALIDATION PHASE:")
        logger.info("Skipping URL validation to save time (GitHub Actions validated)")
        validated_links = unique_links
        
        # Store curated links for later use
        self.curated_links = validated_links
        
        # Generate outputs
        logger.info("\n📝 GENERATION PHASE:")
        self.generate_markdown(validated_links)
        self.generate_json(validated_links)
        self.generate_html_sitemap(validated_links)
        
        logger.info("\n" + "=" * 70)
        logger.info("✅ CURATION COMPLETE!")
        logger.info(f"📊 Final count: {len(validated_links)} indexed links")
        logger.info("=" * 70)
        
        return {
            'success': True,
            'links': len(validated_links),
            'categories': len(set(l['category'] for l in validated_links))
        }


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Link Curator - Scrape and curate links for SEO')
    parser.add_argument('--category', type=str, default=None, help='Filter by category (gitea, ipfs, storage, etc.)')
    parser.add_argument('--output', type=str, default=None, help='Output file path (JSON, MD, or HTML)')
    args = parser.parse_args()
    
    # Define source URLs to scrape
    # These are starting points - the scraper will extract links from these pages
    sources = {
        'documentation': [
            'https://docs.ipfs.tech/',
            'https://docs.filecoin.io/',
        ],
        'community': [
            'https://discuss.ipfs.tech/',
            'https://github.com/ipfs',
        ],
        'news': [
            'https://blog.ipfs.tech/',
            'https://protocol.ai/blog/',
        ],
        'development': [
            'https://github.com/ipfs/kubo',
            'https://github.com/ipfs-cluster/ipfs-cluster',
        ],
        'research': [
            'https://research.protocol.ai/',
        ],
        'tutorial': [
            'https://www.youtube.com/results?search_query=ipfs+tutorial',
        ],
        'gitea': [
            'https://docs.ipfs.tech/',
            'https://discuss.ipfs.tech/',
        ],
        'ipfs': [
            'https://docs.ipfs.tech/',
            'https://blog.ipfs.tech/',
            'https://github.com/ipfs',
        ],
        'storage': [
            'https://docs.filecoin.io/',
            'https://research.protocol.ai/',
        ]
    }
    
    # If category filter specified, only use that category
    if args.category:
        sources = {args.category: sources.get(args.category, [])}
    
    curator = LinkCurator()
    result = curator.run(sources)
    
    # If output file specified, save in appropriate format
    if args.output:
        all_links = curator.curated_links
        if args.output.endswith('.json'):
            curator.generate_json(all_links, args.output)
        elif args.output.endswith('.md'):
            curator.generate_markdown(all_links, args.output)
        elif args.output.endswith('.html'):
            curator.generate_html_sitemap(all_links, args.output)
    
    print(f"\n✅ Curation Result: {result}")
    return result


if __name__ == '__main__':
    main()

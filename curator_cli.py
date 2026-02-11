#!/usr/bin/env python3
"""
Link Curator CLI - Command-line interface for manual link management
Allows adding, removing, and managing curated links
"""

import json
import argparse
from datetime import datetime
from pathlib import Path
from typing import List, Dict
import sys


class CuratorCLI:
    """CLI interface for link curation"""
    
    def __init__(self, data_file: str = 'manual_links.json'):
        self.data_file = data_file
        self.links = self.load_links()
    
    def load_links(self) -> List[Dict]:
        """Load existing links from file"""
        if Path(self.data_file).exists():
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_links(self):
        """Save links to file"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.links, f, indent=2, ensure_ascii=False)
    
    def add_link(self, url: str, title: str, description: str, 
                 keywords: List[str], category: str) -> bool:
        """Add a new link"""
        
        # Validate
        if not url or not url.startswith('http'):
            print("❌ Invalid URL format")
            return False
        
        if not title:
            print("❌ Title cannot be empty")
            return False
        
        if not description:
            print("❌ Description cannot be empty")
            return False
        
        if len(keywords) > 5:
            print("⚠️  Limiting keywords to 5")
            keywords = keywords[:5]
        
        # Check duplicate
        if any(l['url'] == url for l in self.links):
            print("⚠️  Link already exists")
            return False
        
        # Add link
        link = {
            'url': url,
            'title': title,
            'description': description,
            'keywords': keywords,
            'category': category,
            'domain': url.split('/')[2],
            'date_added': datetime.now().isoformat(),
            'source': 'manual'
        }
        
        self.links.append(link)
        self.save_links()
        print(f"✅ Added link: {title}")
        return True
    
    def remove_link(self, url: str) -> bool:
        """Remove a link by URL"""
        before = len(self.links)
        self.links = [l for l in self.links if l['url'] != url]
        
        if len(self.links) < before:
            self.save_links()
            print(f"✅ Removed link: {url}")
            return True
        else:
            print(f"❌ Link not found: {url}")
            return False
    
    def list_links(self, category: str = None) -> None:
        """List all links or by category"""
        links = self.links
        
        if category:
            links = [l for l in links if l['category'] == category]
        
        if not links:
            print("No links found")
            return
        
        print(f"\n{'Index':<6} {'Title':<40} {'Category':<15} {'Added':<10}")
        print("-" * 75)
        
        for idx, link in enumerate(links, 1):
            title = link['title'][:37] + '...' if len(link['title']) > 40 else link['title']
            print(f"{idx:<6} {title:<40} {link['category']:<15} {link['date_added'][:10]:<10}")
    
    def show_link(self, url: str) -> None:
        """Show detailed link information"""
        for link in self.links:
            if link['url'] == url:
                print(f"\n📄 Link Details:")
                print(f"  Title:       {link['title']}")
                print(f"  URL:         {link['url']}")
                print(f"  Domain:      {link['domain']}")
                print(f"  Category:    {link['category']}")
                print(f"  Description: {link['description']}")
                print(f"  Keywords:    {', '.join(link['keywords'])}")
                print(f"  Added:       {link['date_added']}")
                print(f"  Source:      {link.get('source', 'unknown')}\n")
                return
        
        print(f"❌ Link not found: {url}")
    
    def export_markdown(self, output_file: str = 'manual_curated_links.md') -> None:
        """Export links as Markdown"""
        if not self.links:
            print("No links to export")
            return
        
        content = []
        content.append("# 📚 Manually Curated Links\n")
        content.append(f"**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}\n")
        content.append(f"**Total Links:** {len(self.links)}\n\n")
        
        # Group by category
        by_cat = {}
        for link in self.links:
            cat = link['category']
            if cat not in by_cat:
                by_cat[cat] = []
            by_cat[cat].append(link)
        
        for category in sorted(by_cat.keys()):
            cat_links = by_cat[category]
            content.append(f"## {category.title()} ({len(cat_links)})\n\n")
            
            for link in cat_links:
                content.append(f"### {link['title']}\n")
                content.append(f"- **URL:** [{link['domain']}]({link['url']})\n")
                content.append(f"- **Description:** {link['description']}\n")
                content.append(f"- **Keywords:** {', '.join(link['keywords'])}\n\n")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(''.join(content))
        
        print(f"✅ Exported to {output_file}")
    
    def stats(self) -> None:
        """Show statistics"""
        if not self.links:
            print("No links yet")
            return
        
        by_cat = {}
        for link in self.links:
            cat = link['category']
            by_cat[cat] = by_cat.get(cat, 0) + 1
        
        print(f"\n📊 Link Curation Statistics:")
        print(f"  Total Links: {len(self.links)}")
        print(f"  Categories:  {len(by_cat)}")
        print(f"\n  Breakdown by category:")
        for cat in sorted(by_cat.keys()):
            print(f"    • {cat}: {by_cat[cat]} links")
        print()


def main():
    parser = argparse.ArgumentParser(
        description='Link Curator CLI - Manage your curated SEO links',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Add a link
  python curator_cli.py add "https://example.com" "Example Title" "Description" \\
    "keyword1,keyword2,keyword3" "documentation"
  
  # List all links
  python curator_cli.py list
  
  # List by category
  python curator_cli.py list -c documentation
  
  # Show link details
  python curator_cli.py show "https://example.com"
  
  # Remove a link
  python curator_cli.py remove "https://example.com"
  
  # Export as Markdown
  python curator_cli.py export
  
  # Show statistics
  python curator_cli.py stats
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Add command
    add_parser = subparsers.add_parser('add', help='Add a new link')
    add_parser.add_argument('url', help='Link URL')
    add_parser.add_argument('title', help='Link title')
    add_parser.add_argument('description', help='Link description')
    add_parser.add_argument('keywords', help='Keywords (comma-separated, max 5)')
    add_parser.add_argument('category', help='Category')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List all links')
    list_parser.add_argument('-c', '--category', help='Filter by category')
    
    # Show command
    show_parser = subparsers.add_parser('show', help='Show link details')
    show_parser.add_argument('url', help='Link URL')
    
    # Remove command
    remove_parser = subparsers.add_parser('remove', help='Remove a link')
    remove_parser.add_argument('url', help='Link URL')
    
    # Export command
    subparsers.add_parser('export', help='Export as Markdown')
    
    # Stats command
    subparsers.add_parser('stats', help='Show statistics')
    
    args = parser.parse_args()
    cli = CuratorCLI()
    
    if args.command == 'add':
        keywords = [k.strip() for k in args.keywords.split(',')]
        cli.add_link(args.url, args.title, args.description, keywords, args.category)
    
    elif args.command == 'list':
        cli.list_links(args.category)
    
    elif args.command == 'show':
        cli.show_link(args.url)
    
    elif args.command == 'remove':
        cli.remove_link(args.url)
    
    elif args.command == 'export':
        cli.export_markdown()
    
    elif args.command == 'stats':
        cli.stats()
    
    else:
        parser.print_help()


if __name__ == '__main__':
    main()

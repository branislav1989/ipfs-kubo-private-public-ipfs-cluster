# RSS Curation

This folder contains curated IPFS-related links and resources for RSS feed distribution.

## Contents

- `curated_links.json` - Machine-readable curated links with metadata
- `curated_links.md` - Markdown formatted curated links index
- `curated_links.html` - HTML formatted curated links for web display
- `daily_update.sh` - Daily update script that regenerates curated links
- `setup_cron.sh` - Script to install automated daily updates via cron
- `daily_update.log` - Log file for update operations

## Daily Updates

To set up automated daily updates:

```bash
bash setup_cron.sh
```

This will install a cron job that runs daily at 2:00 AM UTC.

## Manual Update

To manually run an update:

```bash
bash daily_update.sh
```

## File Formats

### JSON Format
Structured data with metadata, links, and categorization for programmatic access.

### Markdown Format
Human-readable index with links, descriptions, and keywords.

### HTML Format
Web-ready format for embedding in websites or RSS feeds.

## Last Updated
Check the timestamps in each file for the last update time.

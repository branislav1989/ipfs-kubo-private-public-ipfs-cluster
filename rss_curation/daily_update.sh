#!/bin/bash
# Daily RSS Curation Update Script
# Updates curated links and commits to GitHub

DATE=$(date '+%Y-%m-%d %H:%M:%S')
LOG_FILE="rss_curation/daily_update.log"

echo "[$DATE] Starting daily RSS curation update..." >> $LOG_FILE

# Update curated links from source
if command -v python3 &> /dev/null; then
    python3 link_curator.py >> $LOG_FILE 2>&1
    
    # Copy updated files to rss_curation folder
    cp curated_links.json rss_curation/
    cp curated_links.md rss_curation/
    cp curated_links.html rss_curation/ 2>/dev/null || true
    
    # Git operations
    git add rss_curation/
    git commit -m "Daily RSS curation update - $DATE" >> $LOG_FILE 2>&1
    git push github main >> $LOG_FILE 2>&1
    
    echo "[$DATE] Daily update completed successfully" >> $LOG_FILE
else
    echo "[$DATE] Python3 not found, skipping update" >> $LOG_FILE
fi

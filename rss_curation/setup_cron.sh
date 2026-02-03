#!/bin/bash
# Setup daily cron job for RSS curation updates

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CRON_JOB="0 2 * * * cd $SCRIPT_DIR/.. && bash $SCRIPT_DIR/daily_update.sh"

# Add cron job if not already present
(crontab -l 2>/dev/null | grep -v "daily_update.sh"; echo "$CRON_JOB") | crontab -

echo "Cron job installed successfully!"
echo "Daily update will run at 2:00 AM UTC every day"
crontab -l | grep daily_update.sh

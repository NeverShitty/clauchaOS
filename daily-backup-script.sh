#!/bin/bash
# 💾 DAILY MEMORY BACKUP SCRIPT
# Add to crontab: 0 2 * * * /Users/noshit/MCMANSION/AUTOMATION_LAB/daily_memory_backup.sh

BACKUP_DIR="/Users/noshit/MCMANSION/AUTOMATION_LAB/memory_backups"
MEMORY_DIR="/Users/noshit/MCMANSION/AUTOMATION_LAB/vector_memory"
DATE=$(date +%Y%m%d)
BACKUP_PATH="$BACKUP_DIR/daily_$DATE"

# Create backup directory
mkdir -p "$BACKUP_PATH"

echo "💾 Starting daily memory backup: $(date)"

# Copy memory files
cp -r "$MEMORY_DIR"/* "$BACKUP_PATH/"

# Get memory stats
cd /Users/noshit/MCMANSION/AUTOMATION_LAB
python memory_manager.py stats > "$BACKUP_PATH/stats.json"

# Create summary
echo "📊 Memory Backup Summary - $DATE" > "$BACKUP_PATH/summary.txt"
echo "================================" >> "$BACKUP_PATH/summary.txt"
python memory_manager.py | head -20 >> "$BACKUP_PATH/summary.txt"

# Compress backup
cd "$BACKUP_DIR"
tar -czf "daily_$DATE.tar.gz" "daily_$DATE"
rm -rf "daily_$DATE"

# Keep only last 30 days of backups
find "$BACKUP_DIR" -name "daily_*.tar.gz" -mtime +30 -delete

echo "✅ Backup complete: $BACKUP_DIR/daily_$DATE.tar.gz"

# Optional: Send notification
# osascript -e 'display notification "Memory backup completed" with title "Claude Memory System"'
#!/bin/bash
# Database Backup Script for FastAPI Batik Project
# Usage: ./scripts/backup_database.sh

set -e

# Configuration
BACKUP_DIR="./database_backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
CONTAINER_NAME="db"
DB_USER="${POSTGRES_USER:-postgres}"
DB_NAME="${POSTGRES_DB:-myapp}"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== Database Backup Script ===${NC}"

# Create backup directory if not exists
mkdir -p "$BACKUP_DIR"

echo -e "${YELLOW}Creating backup...${NC}"

# 1. Full backup (structure + data)
echo "📦 Creating full backup..."
docker-compose exec -T "$CONTAINER_NAME" pg_dump -U "$DB_USER" -d "$DB_NAME" \
    > "$BACKUP_DIR/full_backup_${TIMESTAMP}.sql"

# 2. Custom format backup (compressed, can restore partially)
echo "📦 Creating custom format backup (compressed)..."
docker-compose exec -T "$CONTAINER_NAME" pg_dump -U "$DB_USER" -d "$DB_NAME" -Fc \
    > "$BACKUP_DIR/backup_${TIMESTAMP}.dump"

# 3. Schema only
echo "📋 Creating schema-only backup..."
docker-compose exec -T "$CONTAINER_NAME" pg_dump -U "$DB_USER" -d "$DB_NAME" --schema-only \
    > "$BACKUP_DIR/schema_only_${TIMESTAMP}.sql"

# 4. Data only
echo "💾 Creating data-only backup..."
docker-compose exec -T "$CONTAINER_NAME" pg_dump -U "$DB_USER" -d "$DB_NAME" --data-only \
    > "$BACKUP_DIR/data_only_${TIMESTAMP}.sql"

echo -e "${GREEN}✅ Backup completed!${NC}"
echo ""
echo "Backup files created:"
echo "  - Full: $BACKUP_DIR/full_backup_${TIMESTAMP}.sql"
echo "  - Compressed: $BACKUP_DIR/backup_${TIMESTAMP}.dump"
echo "  - Schema: $BACKUP_DIR/schema_only_${TIMESTAMP}.sql"
echo "  - Data: $BACKUP_DIR/data_only_${TIMESTAMP}.sql"
echo ""
echo -e "${YELLOW}Transfer to production:${NC}"
echo "  scp $BACKUP_DIR/backup_${TIMESTAMP}.dump user@server:/path/to/project/"

# Keep only last 7 backups
echo ""
echo "🧹 Cleaning old backups (keeping last 7)..."
ls -t "$BACKUP_DIR"/*.sql "$BACKUP_DIR"/*.dump 2>/dev/null | tail -n +29 | xargs -r rm
echo -e "${GREEN}Done!${NC}"

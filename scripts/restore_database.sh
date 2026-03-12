#!/bin/bash
# Database Restore Script for FastAPI Batik Project
# Usage: ./scripts/restore_database.sh <backup_file>

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check arguments
if [ $# -eq 0 ]; then
    echo -e "${RED}Error: No backup file specified${NC}"
    echo "Usage: $0 <backup_file>"
    echo "Example: $0 database_backups/backup_20251229.dump"
    exit 1
fi

BACKUP_FILE=$1

# Check if file exists
if [ ! -f "$BACKUP_FILE" ]; then
    echo -e "${RED}Error: Backup file not found: $BACKUP_FILE${NC}"
    exit 1
fi

# Configuration
CONTAINER_NAME="db"
DB_USER="${POSTGRES_USER:-postgres}"
DB_NAME="${POSTGRES_DB:-myapp}"

echo -e "${GREEN}=== Database Restore Script ===${NC}"
echo "Backup file: $BACKUP_FILE"
echo "Database: $DB_NAME"
echo ""

# Warning
echo -e "${YELLOW}⚠️  WARNING: This will DROP and recreate the database!${NC}"
read -p "Are you sure you want to continue? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo "Restore cancelled."
    exit 0
fi

echo ""
echo "🔄 Starting restore process..."

# Detect file type
if [[ "$BACKUP_FILE" == *.dump ]]; then
    # Custom format
    echo "📦 Detected custom format (.dump)"
    
    # Drop and recreate database
    echo "🗑️  Dropping database..."
    docker-compose exec -T "$CONTAINER_NAME" psql -U "$DB_USER" -c "DROP DATABASE IF EXISTS $DB_NAME;"
    docker-compose exec -T "$CONTAINER_NAME" psql -U "$DB_USER" -c "CREATE DATABASE $DB_NAME;"
    
    # Restore
    echo "📥 Restoring database..."
    cat "$BACKUP_FILE" | docker-compose exec -T "$CONTAINER_NAME" pg_restore -U "$DB_USER" -d "$DB_NAME" -v
    
elif [[ "$BACKUP_FILE" == *.sql ]]; then
    # SQL format
    echo "📋 Detected SQL format (.sql)"
    
    # Drop and recreate database
    echo "🗑️  Dropping database..."
    docker-compose exec -T "$CONTAINER_NAME" psql -U "$DB_USER" -c "DROP DATABASE IF EXISTS $DB_NAME;"
    docker-compose exec -T "$CONTAINER_NAME" psql -U "$DB_USER" -c "CREATE DATABASE $DB_NAME;"
    
    # Restore
    echo "📥 Restoring database..."
    cat "$BACKUP_FILE" | docker-compose exec -T "$CONTAINER_NAME" psql -U "$DB_USER" -d "$DB_NAME"
    
else
    echo -e "${RED}Error: Unknown backup file format${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}✅ Database restored successfully!${NC}"

# Optional: Stamp alembic
read -p "Do you want to mark Alembic as up-to-date? (yes/no): " stamp_confirm
if [ "$stamp_confirm" == "yes" ]; then
    echo "📌 Stamping Alembic migrations..."
    docker-compose exec web alembic stamp head
    echo -e "${GREEN}✅ Alembic stamped!${NC}"
fi

echo ""
echo "Done! Database is ready to use."

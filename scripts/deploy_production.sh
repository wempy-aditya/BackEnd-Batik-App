#!/bin/bash
# Production Deployment Script for FastAPI Batik Project
# Usage: ./scripts/deploy_production.sh

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   FastAPI Batik Production Deploy     ║${NC}"
echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
echo ""

# Check if .env exists
if [ ! -f "src/.env" ]; then
    echo -e "${RED}❌ Error: src/.env file not found!${NC}"
    echo "Please create src/.env from src/.env.example"
    exit 1
fi

# Check if docker-compose is running
if ! docker-compose ps | grep -q "Up"; then
    echo -e "${YELLOW}⚠️  Docker containers not running${NC}"
    read -p "Start containers now? (yes/no): " start_confirm
    if [ "$start_confirm" == "yes" ]; then
        echo "🚀 Starting Docker containers..."
        docker-compose up -d
        sleep 5
    else
        echo "Please start containers first: docker-compose up -d"
        exit 1
    fi
fi

echo ""
echo -e "${GREEN}📋 Deployment Options:${NC}"
echo "1. Fresh deployment (run migrations)"
echo "2. Restore from backup (with database dump)"
echo "3. Update code only (no DB changes)"
read -p "Select option (1/2/3): " deploy_option

case $deploy_option in
    1)
        echo ""
        echo -e "${YELLOW}🔄 Running migrations...${NC}"
        docker-compose exec web alembic upgrade head
        echo -e "${GREEN}✅ Migrations completed${NC}"
        
        echo ""
        read -p "Create superuser? (yes/no): " create_user
        if [ "$create_user" == "yes" ]; then
            docker-compose exec web python -m scripts.create_first_superuser
        fi
        ;;
        
    2)
        echo ""
        read -p "Enter backup file path: " backup_file
        if [ -f "$backup_file" ]; then
            ./scripts/restore_database.sh "$backup_file"
        else
            echo -e "${RED}❌ Backup file not found${NC}"
            exit 1
        fi
        ;;
        
    3)
        echo ""
        echo -e "${YELLOW}🔄 Updating code...${NC}"
        git pull origin main
        docker-compose down
        docker-compose up -d --build
        echo -e "${GREEN}✅ Code updated${NC}"
        ;;
        
    *)
        echo -e "${RED}Invalid option${NC}"
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}╔════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║      Deployment Completed! 🎉          ║${NC}"
echo -e "${GREEN}╔════════════════════════════════════════╗${NC}"
echo ""
echo "📊 Service Status:"
docker-compose ps

echo ""
echo "🌐 Access points:"
echo "  - API: http://localhost:8000"
echo "  - API Docs: http://localhost:8000/docs"
echo "  - Admin Panel: http://localhost:8000/admin"

echo ""
echo "📝 Useful commands:"
echo "  - View logs: docker-compose logs -f web"
echo "  - Stop services: docker-compose down"
echo "  - Restart: docker-compose restart web"
echo "  - Backup DB: ./scripts/backup_database.sh"

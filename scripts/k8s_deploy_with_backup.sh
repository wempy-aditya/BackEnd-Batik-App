#!/bin/bash
# Database Deployment Helper for Kubernetes
# Handles database restore from backup (for mixed migration + manual query databases)

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

NAMESPACE="batik-api"

echo -e "${BLUE}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  Kubernetes Database Deployment Helper                ║${NC}"
echo -e "${BLUE}║  For databases with mixed migrations + manual queries ║${NC}"
echo -e "${BLUE}╔════════════════════════════════════════════════════════╗${NC}"
echo ""

# Check if kubectl is available
if ! command -v kubectl &> /dev/null; then
    echo -e "${RED}❌ kubectl not found. Please install kubectl first.${NC}"
    exit 1
fi

# Check if backup file exists
if [ ! -f "backup.sql" ]; then
    echo -e "${RED}❌ backup.sql not found in current directory${NC}"
    echo ""
    echo "Please create backup first:"
    echo "  1. On development machine:"
    echo "     docker-compose exec db pg_dump -U postgres -d myapp > backup.sql"
    echo ""
    echo "  2. Copy to this directory and run this script again"
    exit 1
fi

echo -e "${GREEN}✅ Found backup file: backup.sql${NC}"
BACKUP_SIZE=$(du -h backup.sql | cut -f1)
echo -e "   Size: ${BACKUP_SIZE}"
echo ""

# Check backup size - if > 1MB, recommend using PVC instead of ConfigMap
BACKUP_SIZE_BYTES=$(stat -f%z backup.sql 2>/dev/null || stat -c%s backup.sql)
if [ "$BACKUP_SIZE_BYTES" -gt 1048576 ]; then
    echo -e "${YELLOW}⚠️  Backup file is larger than 1MB${NC}"
    echo -e "${YELLOW}   ConfigMap has size limit. Consider using PVC or external storage.${NC}"
    echo ""
    read -p "Continue anyway? (yes/no): " confirm
    if [ "$confirm" != "yes" ]; then
        echo "Deployment cancelled."
        exit 0
    fi
fi

echo -e "${BLUE}Deployment Steps:${NC}"
echo "1. Create namespace (if not exists)"
echo "2. Create ConfigMap from backup.sql"
echo "3. Deploy database restore script"
echo "4. Run database restore job"
echo "5. Stamp Alembic migrations"
echo "6. Deploy application"
echo ""

read -p "Proceed with deployment? (yes/no): " proceed
if [ "$proceed" != "yes" ]; then
    echo "Deployment cancelled."
    exit 0
fi

echo ""
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}Step 1: Create Namespace${NC}"
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

kubectl apply -f k8s/namespace.yaml
echo -e "${GREEN}✅ Namespace created/verified${NC}"
echo ""

echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}Step 2: Create ConfigMap from backup.sql${NC}"
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

# Delete existing ConfigMap if exists
kubectl delete configmap db-backup-sql -n $NAMESPACE 2>/dev/null || true

# Create new ConfigMap from backup file
kubectl create configmap db-backup-sql \
    --from-file=backup.sql=backup.sql \
    -n $NAMESPACE

echo -e "${GREEN}✅ ConfigMap created from backup.sql${NC}"
echo ""

echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}Step 3: Deploy Database Components${NC}"
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

# Apply configurations and secrets
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secrets.yaml
kubectl apply -f k8s/postgres-pvc.yaml
kubectl apply -f k8s/postgres-deployment.yaml
kubectl apply -f k8s/redis-deployment.yaml

echo -e "${GREEN}✅ Database components deployed${NC}"
echo ""

echo -e "${YELLOW}Waiting for PostgreSQL to be ready...${NC}"
kubectl wait --for=condition=ready pod -l app=postgres -n $NAMESPACE --timeout=300s

echo -e "${GREEN}✅ PostgreSQL is ready${NC}"
echo ""

echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}Step 4: Run Database Restore Job${NC}"
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

# Delete old restore job if exists
kubectl delete job db-restore-job -n $NAMESPACE 2>/dev/null || true

# Apply restore script and job
kubectl apply -f k8s/db-restore-configmap.yaml
kubectl apply -f k8s/db-restore-job.yaml

echo -e "${YELLOW}Restore job started. Waiting for completion...${NC}"
echo ""

# Wait for job to complete
kubectl wait --for=condition=complete job/db-restore-job -n $NAMESPACE --timeout=600s

# Show logs
echo -e "${BLUE}Restore Job Logs:${NC}"
kubectl logs -n $NAMESPACE job/db-restore-job
echo ""

if kubectl get job db-restore-job -n $NAMESPACE -o jsonpath='{.status.succeeded}' | grep -q 1; then
    echo -e "${GREEN}✅ Database restored successfully!${NC}"
else
    echo -e "${RED}❌ Database restore failed!${NC}"
    echo "Check logs above for details"
    exit 1
fi
echo ""

echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}Step 5: Stamp Alembic Migrations${NC}"
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

# Delete old stamp job if exists
kubectl delete job alembic-stamp-job -n $NAMESPACE 2>/dev/null || true

# Apply stamp job
kubectl apply -f k8s/alembic-stamp-job.yaml

echo -e "${YELLOW}Alembic stamp job started. Waiting for completion...${NC}"
echo ""

# Wait for job to complete
kubectl wait --for=condition=complete job/alembic-stamp-job -n $NAMESPACE --timeout=300s

# Show logs
echo -e "${BLUE}Alembic Stamp Logs:${NC}"
kubectl logs -n $NAMESPACE job/alembic-stamp-job
echo ""

if kubectl get job alembic-stamp-job -n $NAMESPACE -o jsonpath='{.status.succeeded}' | grep -q 1; then
    echo -e "${GREEN}✅ Alembic migrations stamped!${NC}"
else
    echo -e "${RED}❌ Alembic stamp failed!${NC}"
    exit 1
fi
echo ""

echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}Step 6: Deploy Application${NC}"
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

# Apply application deployments
kubectl apply -f k8s/uploads-pvc.yaml
kubectl apply -f k8s/fastapi-deployment.yaml
kubectl apply -f k8s/worker-deployment.yaml

echo -e "${GREEN}✅ Application deployed${NC}"
echo ""

echo -e "${YELLOW}Waiting for FastAPI pods to be ready...${NC}"
kubectl wait --for=condition=ready pod -l app=fastapi-web -n $NAMESPACE --timeout=300s

echo -e "${GREEN}✅ FastAPI is ready${NC}"
echo ""

echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}Step 7: Deploy Ingress & Monitoring (Optional)${NC}"
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

read -p "Deploy Ingress? (yes/no): " deploy_ingress
if [ "$deploy_ingress" == "yes" ]; then
    kubectl apply -f k8s/ingress.yaml
    echo -e "${GREEN}✅ Ingress deployed${NC}"
fi

read -p "Deploy HPA (Auto-scaling)? (yes/no): " deploy_hpa
if [ "$deploy_hpa" == "yes" ]; then
    kubectl apply -f k8s/hpa.yaml
    echo -e "${GREEN}✅ HPA deployed${NC}"
fi

read -p "Deploy CronJob Backup? (yes/no): " deploy_backup
if [ "$deploy_backup" == "yes" ]; then
    kubectl apply -f k8s/cronjob-backup.yaml
    echo -e "${GREEN}✅ CronJob deployed${NC}"
fi

echo ""
echo -e "${GREEN}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║           Deployment Completed Successfully! 🎉        ║${NC}"
echo -e "${GREEN}╔════════════════════════════════════════════════════════╗${NC}"
echo ""

echo -e "${BLUE}📊 Deployment Summary:${NC}"
kubectl get all -n $NAMESPACE
echo ""

echo -e "${BLUE}🔗 Access Points:${NC}"
echo "  Service: kubectl port-forward -n $NAMESPACE svc/fastapi-service 8000:80"
echo "  Then open: http://localhost:8000"
echo ""

echo -e "${BLUE}📝 Useful Commands:${NC}"
echo "  View logs:     kubectl logs -n $NAMESPACE -l app=fastapi-web -f"
echo "  Get pods:      kubectl get pods -n $NAMESPACE"
echo "  Describe pod:  kubectl describe pod -n $NAMESPACE <pod-name>"
echo "  Shell access:  kubectl exec -it -n $NAMESPACE <pod-name> -- bash"
echo "  Database CLI:  kubectl exec -it -n $NAMESPACE deployment/postgres -- psql -U batik_user -d batik_production"
echo ""

echo -e "${YELLOW}⚠️  Important Notes:${NC}"
echo "  1. Database restored from backup (includes manual queries)"
echo "  2. Alembic migrations marked as applied (stamped to head)"
echo "  3. Future migrations will work normally (use: kubectl exec ... -- alembic upgrade head)"
echo "  4. Auto-migration in init container is DISABLED (to prevent conflicts)"
echo ""

echo -e "${GREEN}Deployment successful! Your application is now running on Kubernetes.${NC}"

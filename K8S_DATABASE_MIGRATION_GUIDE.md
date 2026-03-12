# Database Deployment for Kubernetes - Mixed Migration Strategy

## 🎯 Problem

Database Anda memiliki:
- ✅ Struktur dari Alembic migrations
- ✅ Struktur dari direct SQL query (tidak tercatat di migrations)
- ✅ Data production yang sudah ada

## ✅ Solution

Restore database dari backup, kemudian stamp Alembic agar migration system tetap berfungsi untuk future updates.

---

## 🚀 Quick Deployment (Recommended)

### Step 1: Prepare Backup

Di development machine:

```bash
# Backup database lengkap (struktur + data)
docker-compose exec db pg_dump -U postgres -d myapp > backup.sql

# Copy backup ke project root
# File: backup.sql
```

### Step 2: Deploy to Kubernetes

```bash
# Make script executable
chmod +x scripts/k8s_deploy_with_backup.sh

# Run automated deployment
./scripts/k8s_deploy_with_backup.sh
```

Script akan otomatis:
1. ✅ Create namespace
2. ✅ Create ConfigMap from backup.sql
3. ✅ Deploy PostgreSQL & Redis
4. ✅ Restore database dari backup
5. ✅ Stamp Alembic migrations
6. ✅ Deploy FastAPI application
7. ✅ Deploy workers, ingress, HPA (optional)

**Done!** Database ter-restore dengan semua struktur (migration + manual query) dan data.

---

## 📋 Manual Deployment (Step by Step)

Jika ingin manual control:

### 1. Backup Database Development

```bash
cd /path/to/project
docker-compose exec db pg_dump -U postgres -d myapp > backup.sql
```

### 2. Deploy Basic Components

```bash
# Create namespace & secrets
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secrets.yaml

# Deploy database
kubectl apply -f k8s/postgres-pvc.yaml
kubectl apply -f k8s/postgres-deployment.yaml
kubectl apply -f k8s/redis-deployment.yaml

# Wait for postgres to be ready
kubectl wait --for=condition=ready pod -l app=postgres -n batik-api --timeout=300s
```

### 3. Create ConfigMap dari Backup

```bash
# Create ConfigMap from backup.sql
kubectl create configmap db-backup-sql \
    --from-file=backup.sql=backup.sql \
    -n batik-api
```

**Note**: ConfigMap memiliki size limit ~1MB. Jika backup lebih besar, gunakan PVC:

```bash
# Alternative: Upload to PVC
kubectl apply -f - <<EOF
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: backup-pvc
  namespace: batik-api
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 5Gi
EOF

# Copy backup to PVC (create temporary pod)
kubectl run -n batik-api backup-uploader --image=busybox --restart=Never -- sleep 3600
kubectl cp backup.sql batik-api/backup-uploader:/backup.sql
# Then mount this PVC in restore job
```

### 4. Run Database Restore Job

```bash
# Apply restore script
kubectl apply -f k8s/db-restore-configmap.yaml

# Run restore job
kubectl apply -f k8s/db-restore-job.yaml

# Watch progress
kubectl logs -n batik-api job/db-restore-job -f

# Check if successful
kubectl get job -n batik-api db-restore-job
```

### 5. Stamp Alembic Migrations

```bash
# Run stamp job
kubectl apply -f k8s/alembic-stamp-job.yaml

# Watch progress
kubectl logs -n batik-api job/alembic-stamp-job -f
```

Ini akan mark semua migrations sebagai "applied" tanpa run mereka (karena struktur sudah ada dari backup).

### 6. Deploy Application

```bash
# Deploy app
kubectl apply -f k8s/uploads-pvc.yaml
kubectl apply -f k8s/fastapi-deployment.yaml
kubectl apply -f k8s/worker-deployment.yaml

# Wait for ready
kubectl wait --for=condition=ready pod -l app=fastapi-web -n batik-api --timeout=300s

# Check status
kubectl get pods -n batik-api
```

### 7. Deploy Ingress & Extras (Optional)

```bash
kubectl apply -f k8s/ingress.yaml
kubectl apply -f k8s/hpa.yaml
kubectl apply -f k8s/cronjob-backup.yaml
```

---

## 🔍 Verification

### Check Database

```bash
# Access PostgreSQL
kubectl exec -it -n batik-api deployment/postgres -- \
  psql -U batik_user -d batik_production

# In psql:
\dt          # List tables
SELECT COUNT(*) FROM users;   # Check data
\q           # Exit
```

### Check Alembic Status

```bash
# Check current migration version
kubectl exec -n batik-api deployment/fastapi-web -- alembic current

# Should show: "head" or current version
```

### Check Application

```bash
# Port forward
kubectl port-forward -n batik-api svc/fastapi-service 8000:80

# Test API
curl http://localhost:8000/api/v1/health

# Open in browser
open http://localhost:8000/docs
```

---

## 🔄 Future Migrations

Setelah deployment pertama, future migrations akan berjalan normal:

### Development

```bash
# Edit model
nano src/app/models/user.py

# Generate migration
docker-compose exec web alembic revision --autogenerate -m "add user field"

# Test migration
docker-compose exec web alembic upgrade head

# Commit
git add src/migrations/versions/*.py
git commit -m "Migration: add user field"
git push
```

### Production (Kubernetes)

```bash
# Pull latest code
git pull

# Rebuild & push image
docker build -t ghcr.io/wempy-aditya/backend-web-batik:latest .
docker push ghcr.io/wempy-aditya/backend-web-batik:latest

# Update deployment (will pull new image)
kubectl rollout restart deployment/fastapi-web -n batik-api

# Or run migration manually
kubectl exec -n batik-api deployment/fastapi-web -- alembic upgrade head
```

**Alternative**: Enable auto-migration in init container (edit `k8s/fastapi-deployment.yaml`):

```yaml
# Uncomment migration init container
initContainers:
- name: migration
  image: ghcr.io/wempy-aditya/backend-web-batik:latest
  command: ["alembic", "upgrade", "head"]
```

---

## 🛠️ Troubleshooting

### Restore Job Failed

```bash
# Check logs
kubectl logs -n batik-api job/db-restore-job

# Common issues:
# 1. Backup file not found → Check ConfigMap
kubectl get configmap db-backup-sql -n batik-api

# 2. Database already has tables → Delete & recreate
kubectl exec -n batik-api deployment/postgres -- \
  psql -U batik_user -c "DROP DATABASE batik_production;"
kubectl exec -n batik-api deployment/postgres -- \
  psql -U batik_user -c "CREATE DATABASE batik_production;"

# Then re-run restore job
kubectl delete job db-restore-job -n batik-api
kubectl apply -f k8s/db-restore-job.yaml
```

### Backup File Too Large

```bash
# Instead of ConfigMap, use PVC
kubectl apply -f - <<EOF
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: backup-pvc
  namespace: batik-api
spec:
  accessModes: [ReadWriteOnce]
  resources:
    requests:
      storage: 10Gi
EOF

# Upload backup via temporary pod
kubectl run tmp-uploader --image=postgres:13 -n batik-api -- sleep 3600
kubectl cp backup.sql batik-api/tmp-uploader:/tmp/backup.sql

# Mount PVC in restore job (edit db-restore-job.yaml)
```

### Alembic Out of Sync

```bash
# Check current version
kubectl exec -n batik-api deployment/fastapi-web -- alembic current

# If wrong, re-stamp
kubectl exec -n batik-api deployment/fastapi-web -- alembic stamp head

# Or specific version
kubectl exec -n batik-api deployment/fastapi-web -- alembic stamp <revision-id>
```

---

## 📊 Components Overview

| Component | Purpose | File |
|-----------|---------|------|
| `db-restore-configmap.yaml` | Restore script | Contains bash script |
| `db-restore-job.yaml` | Restore job | Runs restore from backup |
| `alembic-stamp-job.yaml` | Stamp migrations | Marks migrations as applied |
| `fastapi-deployment.yaml` | App deployment | Auto-migration **disabled** |
| `k8s_deploy_with_backup.sh` | Automation | One-command deployment |

---

## ✅ Best Practices

1. **Backup First**: Always backup before migration/deployment
2. **Test in Staging**: Test restore process in staging environment
3. **Use Managed DB**: For production, consider AWS RDS/CloudSQL
4. **Automate Backups**: CronJob sudah included (`cronjob-backup.yaml`)
5. **Monitor**: Setup Prometheus/Grafana untuk monitoring
6. **Version Control**: Commit backup metadata (not file) ke git

---

## 🎯 Summary

**Problem**: Database mixed (migration + manual query)
**Solution**: Restore from backup + stamp Alembic
**Result**: 
- ✅ All data & structure preserved
- ✅ Future migrations will work
- ✅ No need to track manual queries
- ✅ Production-ready Kubernetes deployment

**Command**:
```bash
./scripts/k8s_deploy_with_backup.sh
```

Done! 🚀

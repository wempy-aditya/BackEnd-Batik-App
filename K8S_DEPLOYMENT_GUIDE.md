# 🚢 Kubernetes Deployment Guide - FastAPI Batik Project

## 📋 Prerequisites

1. **Kubernetes Cluster** (salah satu):
   - Minikube (local development)
   - AWS EKS
   - Google GKE
   - Azure AKS
   - DigitalOcean Kubernetes
   - On-premise cluster

2. **Tools**:
   ```bash
   # kubectl
   curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
   sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
   
   # kustomize (optional)
   curl -s "https://raw.githubusercontent.com/kubernetes-sigs/kustomize/master/hack/install_kustomize.sh" | bash
   
   # helm (optional)
   curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
   ```

3. **Docker Image Registry**:
   - GitHub Container Registry (GHCR) - Free
   - Docker Hub
   - AWS ECR
   - Google GCR
   - Azure ACR

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│                   Ingress (NGINX)                   │
│            api.yourdomain.com (HTTPS)               │
└────────────────────┬────────────────────────────────┘
                     │
         ┌───────────┴───────────┐
         │  FastAPI Service (ClusterIP)  │
         └───────────┬───────────┘
                     │
    ┌────────────────┼────────────────┐
    │                │                │
┌───▼────┐     ┌────▼─────┐    ┌────▼─────┐
│FastAPI │     │ FastAPI  │    │ FastAPI  │
│  Pod 1 │     │  Pod 2   │    │  Pod 3   │
└────┬───┘     └────┬─────┘    └────┬─────┘
     │              │               │
     └──────────────┼───────────────┘
                    │
        ┌───────────┼────────────┐
        │           │            │
    ┌───▼───┐  ┌───▼────┐  ┌───▼────┐
    │Postgres│  │ Redis  │  │ Worker │
    │Service │  │Service │  │  Pods  │
    └────────┘  └────────┘  └────────┘
```

---

## 🚀 Quick Start Deployment

### Step 1: Build & Push Docker Image

#### Option A: GitHub Actions (Recommended)

```bash
# 1. Push code to GitHub
git add .
git commit -m "Add Kubernetes configs"
git push origin main

# 2. GitHub Actions will automatically build and push to GHCR
# Image: ghcr.io/wempy-aditya/backend-web-batik:latest
```

#### Option B: Manual Build

```bash
# 1. Build image
docker build -t ghcr.io/wempy-aditya/backend-web-batik:latest .

# 2. Login to GHCR
echo $GITHUB_TOKEN | docker login ghcr.io -u wempy-aditya --password-stdin

# 3. Push image
docker push ghcr.io/wempy-aditya/backend-web-batik:latest
```

---

### Step 2: Update Configuration

#### 2.1 Update Secrets (`k8s/secrets.yaml`)

```bash
# Generate random SECRET_KEY
openssl rand -hex 32

# Edit secrets.yaml
nano k8s/secrets.yaml
```

Update nilai:
- `SECRET_KEY`: Result dari openssl rand
- `POSTGRES_PASSWORD`: Strong password
- `ADMIN_PASSWORD`: Strong admin password

#### 2.2 Update Image Name (`k8s/fastapi-deployment.yaml`)

Replace semua occurence:
```yaml
# Ganti ini:
image: ghcr.io/wempy-aditya/batik-api:latest

# Dengan:
image: ghcr.io/wempy-aditya/backend-web-batik:latest
```

#### 2.3 Update Domain (`k8s/ingress.yaml`)

```yaml
# Ganti:
- host: api.yourdomain.com

# Dengan domain Anda:
- host: api.batik-research.com
```

---

### Step 3: Deploy to Kubernetes

```bash
# 1. Apply all manifests
kubectl apply -f k8s/

# 2. Check deployment status
kubectl get all -n batik-api

# 3. Watch pods starting
kubectl get pods -n batik-api -w

# 4. Check logs
kubectl logs -n batik-api -l app=fastapi-web -f
```

---

## 📊 Deployment dengan Database Dump

Untuk database yang mixed (migration + manual query):

### Option 1: Restore dari Backup

```bash
# 1. Backup database development (di local)
docker-compose exec db pg_dump -U postgres -d myapp > backup.sql

# 2. Copy backup ke pod PostgreSQL
kubectl cp backup.sql batik-api/postgres-<pod-id>:/tmp/backup.sql

# 3. Restore di pod
kubectl exec -n batik-api postgres-<pod-id> -- \
  psql -U batik_user -d batik_production < /tmp/backup.sql

# 4. Stamp Alembic
kubectl exec -n batik-api fastapi-web-<pod-id> -- \
  alembic stamp head
```

### Option 2: Using Init Job

Create `k8s/db-restore-job.yaml`:

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: db-restore
  namespace: batik-api
spec:
  template:
    spec:
      restartPolicy: Never
      containers:
      - name: restore
        image: postgres:13
        command:
        - sh
        - -c
        - |
          echo "Restoring database..."
          psql -h postgres-service -U $POSTGRES_USER -d $POSTGRES_DB < /backup/backup.sql
          echo "Restore completed"
        env:
        - name: POSTGRES_USER
          valueFrom:
            secretKeyRef:
              name: batik-api-secrets
              key: POSTGRES_USER
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: batik-api-secrets
              key: POSTGRES_PASSWORD
        - name: POSTGRES_DB
          valueFrom:
            configMapKeyRef:
              name: batik-api-config
              key: POSTGRES_DB
        volumeMounts:
        - name: backup
          mountPath: /backup
      volumes:
      - name: backup
        configMap:
          name: db-backup-sql
```

Apply:
```bash
# Create ConfigMap from backup file
kubectl create configmap db-backup-sql --from-file=backup.sql -n batik-api

# Run restore job
kubectl apply -f k8s/db-restore-job.yaml

# Check logs
kubectl logs -n batik-api job/db-restore -f
```

---

## 🔐 Using Managed Database (Recommended)

Untuk production, gunakan managed database:

### AWS RDS Example

```yaml
# k8s/configmap.yaml - Update:
data:
  POSTGRES_SERVER: "batik-db.xxxxx.us-east-1.rds.amazonaws.com"
  POSTGRES_PORT: "5432"
  POSTGRES_DB: "batik_production"
```

Kemudian **hapus/disable** `postgres-deployment.yaml`:

```bash
# Deploy tanpa postgres
kubectl apply -f k8s/ --exclude=postgres-deployment.yaml --exclude=postgres-pvc.yaml
```

### Supabase/Neon Example

```yaml
# k8s/configmap.yaml
data:
  POSTGRES_SERVER: "db.xxxxx.supabase.co"
  POSTGRES_PORT: "5432"
  POSTGRES_DB: "postgres"

# k8s/secrets.yaml
stringData:
  POSTGRES_USER: "postgres.xxxxx"
  POSTGRES_PASSWORD: "your-supabase-password"
```

---

## 📁 File Storage Strategy

### Option 1: Persistent Volume (Simple)

Already configured in `k8s/uploads-pvc.yaml`.

**Requirements**: Storage class yang support ReadWriteMany (NFS, EFS, Azure Files, GCP Filestore)

### Option 2: Cloud Storage (Recommended)

Gunakan S3/GCS/Azure Blob untuk uploads.

Install SDK:
```bash
# AWS S3
pip install boto3

# Google Cloud Storage
pip install google-cloud-storage

# Azure Blob
pip install azure-storage-blob
```

Update code untuk upload ke cloud storage instead of local filesystem.

---

## 🔄 CI/CD Pipeline

### GitHub Actions Workflow

Already configured in `.github/workflows/docker-build.yml`.

**Automatic triggers**:
- Push to `main` → Build & push image with `latest` tag
- Create tag `v1.0.0` → Build & push with version tag

### ArgoCD (GitOps)

```bash
# Install ArgoCD
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Create Application
cat <<EOF | kubectl apply -f -
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: batik-api
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/wempy-aditya/BackEnd-Web-Batik
    targetRevision: main
    path: k8s
  destination:
    server: https://kubernetes.default.svc
    namespace: batik-api
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
EOF
```

---

## 📈 Monitoring & Logging

### Install Prometheus & Grafana

```bash
# Add helm repo
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

# Install Prometheus
helm install prometheus prometheus-community/kube-prometheus-stack -n monitoring --create-namespace

# Access Grafana
kubectl port-forward -n monitoring svc/prometheus-grafana 3000:80
# Username: admin, Password: prom-operator
```

### Logging with ELK/Loki

```bash
# Install Loki
helm repo add grafana https://grafana.github.io/helm-charts
helm install loki grafana/loki-stack -n logging --create-namespace
```

---

## 🛠️ Useful Commands

### Deployment Management

```bash
# Scale deployment
kubectl scale deployment fastapi-web -n batik-api --replicas=5

# Update image
kubectl set image deployment/fastapi-web -n batik-api \
  fastapi=ghcr.io/wempy-aditya/backend-web-batik:v1.1.0

# Rollback
kubectl rollout undo deployment/fastapi-web -n batik-api

# Check rollout status
kubectl rollout status deployment/fastapi-web -n batik-api
```

### Debugging

```bash
# Get pod logs
kubectl logs -n batik-api -l app=fastapi-web --tail=100 -f

# Execute command in pod
kubectl exec -it -n batik-api fastapi-web-<pod-id> -- bash

# Port forward untuk testing
kubectl port-forward -n batik-api svc/fastapi-service 8000:80

# Describe pod (untuk troubleshooting)
kubectl describe pod -n batik-api fastapi-web-<pod-id>
```

### Database Management

```bash
# Access PostgreSQL
kubectl exec -it -n batik-api postgres-<pod-id> -- \
  psql -U batik_user -d batik_production

# Run migrations
kubectl exec -n batik-api fastapi-web-<pod-id> -- \
  alembic upgrade head

# Create superuser
kubectl exec -n batik-api fastapi-web-<pod-id> -- \
  python -m scripts.create_first_superuser
```

### Backup & Restore

```bash
# Manual backup
kubectl exec -n batik-api postgres-<pod-id> -- \
  pg_dump -U batik_user batik_production > backup_$(date +%Y%m%d).sql

# Copy file from pod
kubectl cp batik-api/postgres-<pod-id>:/backups/backup.sql ./backup.sql

# Copy file to pod
kubectl cp ./backup.sql batik-api/postgres-<pod-id>:/tmp/backup.sql
```

---

## 🔒 Security Best Practices

1. **Secrets Management**:
   ```bash
   # Use external secrets (recommended)
   helm install external-secrets external-secrets/external-secrets -n external-secrets-system --create-namespace
   ```

2. **Network Policies**:
   ```yaml
   apiVersion: networking.k8s.io/v1
   kind: NetworkPolicy
   metadata:
     name: fastapi-network-policy
     namespace: batik-api
   spec:
     podSelector:
       matchLabels:
         app: fastapi-web
     policyTypes:
     - Ingress
     - Egress
     ingress:
     - from:
       - podSelector:
           matchLabels:
             app: nginx-ingress
     egress:
     - to:
       - podSelector:
           matchLabels:
             app: postgres
       - podSelector:
           matchLabels:
             app: redis
   ```

3. **RBAC**:
   ```bash
   # Create service account with limited permissions
   kubectl create serviceaccount batik-api-sa -n batik-api
   ```

4. **Pod Security**:
   ```yaml
   securityContext:
     runAsNonRoot: true
     runAsUser: 1000
     fsGroup: 1000
     capabilities:
       drop:
       - ALL
   ```

---

## 💰 Cost Optimization

1. **Vertical Pod Autoscaling**:
   ```bash
   kubectl apply -f - <<EOF
   apiVersion: autoscaling.k8s.io/v1
   kind: VerticalPodAutoscaler
   metadata:
     name: fastapi-vpa
     namespace: batik-api
   spec:
     targetRef:
       apiVersion: apps/v1
       kind: Deployment
       name: fastapi-web
     updatePolicy:
       updateMode: "Auto"
   EOF
   ```

2. **Resource Limits**: Already configured in deployments

3. **Use spot instances** (cloud providers):
   - AWS: Spot instances
   - GCP: Preemptible VMs
   - Azure: Spot VMs

---

## 🎯 Production Checklist

- [ ] Update secrets dengan nilai production
- [ ] Setup managed database (RDS/CloudSQL/Azure DB)
- [ ] Configure cloud storage untuk uploads (S3/GCS/Blob)
- [ ] Setup ingress dengan domain & SSL certificate
- [ ] Enable HPA untuk auto-scaling
- [ ] Configure backup CronJob
- [ ] Setup monitoring (Prometheus/Grafana)
- [ ] Setup logging (ELK/Loki)
- [ ] Configure network policies
- [ ] Setup CI/CD pipeline
- [ ] Document runbook untuk ops team
- [ ] Load testing
- [ ] Disaster recovery plan

---

## 📞 Troubleshooting

### Pods CrashLoopBackOff

```bash
# Check logs
kubectl logs -n batik-api fastapi-web-<pod-id> --previous

# Check events
kubectl get events -n batik-api --sort-by='.lastTimestamp'

# Common issues:
# - Database connection failed → Check secrets & configmap
# - Migration error → Check init container logs
# - Resource limits → Increase memory/cpu limits
```

### Image Pull Error

```bash
# Create image pull secret
kubectl create secret docker-registry ghcr-secret \
  --docker-server=ghcr.io \
  --docker-username=wempy-aditya \
  --docker-password=$GITHUB_TOKEN \
  -n batik-api

# Add to deployment:
# imagePullSecrets:
# - name: ghcr-secret
```

### Database Connection Timeout

```bash
# Check if postgres is running
kubectl get pods -n batik-api -l app=postgres

# Check service
kubectl get svc -n batik-api postgres-service

# Test connection from pod
kubectl exec -n batik-api fastapi-web-<pod-id> -- \
  nc -zv postgres-service 5432
```

---

Deployment to Kubernetes is ready! 🚀

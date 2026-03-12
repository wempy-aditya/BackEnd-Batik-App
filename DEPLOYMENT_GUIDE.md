# 🚀 Deployment Guide - FastAPI Batik Project

## Situasi Database Anda

Database sudah ada dengan:
- ✅ Struktur dari Alembic migrations
- ✅ Struktur dari direct SQL query (tidak tercatat di migrations)
- ✅ Data development yang sudah ada

## 📋 Strategi Deployment Database

### **Opsi 1: Dump & Restore (RECOMMENDED)**

Cara paling aman karena database Anda mixed (migration + manual query).

#### Step 1: Backup Database Development

```bash
# Jalankan script backup
chmod +x scripts/backup_database.sh
./scripts/backup_database.sh
```

File backup akan tersimpan di `database_backups/`:
- `backup_YYYYMMDD_HHMMSS.dump` - Compressed (recommended untuk transfer)
- `full_backup_YYYYMMDD_HHMMSS.sql` - Full SQL format
- `schema_only_YYYYMMDD_HHMMSS.sql` - Hanya struktur
- `data_only_YYYYMMDD_HHMMSS.sql` - Hanya data

#### Step 2: Transfer ke Production Server

```bash
# Copy backup ke server production
scp database_backups/backup_20251229.dump user@server-ip:/path/to/project/
```

#### Step 3: Restore di Production

```bash
# Di server production
chmod +x scripts/restore_database.sh
./scripts/restore_database.sh database_backups/backup_20251229.dump
```

Script akan:
1. Drop database lama (if exists)
2. Create database baru
3. Restore semua struktur + data
4. Tanya apakah mau stamp Alembic (jawab YES)

---

### **Opsi 2: Fresh Migration (Kalau DB Production Masih Kosong)**

Hanya untuk production yang belum ada data.

```bash
# Di production
docker-compose exec web alembic upgrade head
docker-compose exec web python -m scripts.create_first_superuser
```

⚠️ **Masalah**: Struktur dari manual query tidak akan ter-create!

---

## 🔧 Automated Deployment

### Quick Deploy Script

```bash
chmod +x scripts/deploy_production.sh
./scripts/deploy_production.sh
```

Menu interaktif:
1. **Fresh deployment** - Run migrations (kalau DB kosong)
2. **Restore from backup** - Restore database dump (kalau DB ada data)
3. **Update code only** - Git pull + rebuild (kalau cuma update code)

---

## 📦 Complete Deployment Steps

### A. Setup Server Production (First Time)

```bash
# 1. Update system
sudo apt update && sudo apt upgrade -y

# 2. Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# 3. Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 4. Clone project
git clone https://github.com/wempy-aditya/BackEnd-Web-Batik.git
cd BackEnd-Web-Batik

# 5. Setup environment
cp src/.env.example src/.env
nano src/.env  # Edit untuk production
```

### B. Environment Variables Production

Edit `src/.env`:

```env
# App
ENVIRONMENT=production
APP_NAME="Batik Research API"

# Security (GENERATE NEW SECRET!)
SECRET_KEY="<generate-random-64-chars>"
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# Database
POSTGRES_USER=batik_user
POSTGRES_PASSWORD=<strong-password>
POSTGRES_SERVER=db
POSTGRES_PORT=5432
POSTGRES_DB=batik_production

# Redis
REDIS_CACHE_HOST=redis
REDIS_QUEUE_HOST=redis
REDIS_RATE_LIMIT_HOST=redis

# Admin
ADMIN_NAME="Admin Name"
ADMIN_EMAIL="admin@yourdomain.com"
ADMIN_USERNAME="admin"
ADMIN_PASSWORD=<strong-admin-password>

# Security
CRUD_ADMIN_ENABLED=true
SESSION_SECURE_COOKIES=true
```

### C. Deploy with Database

**Option 1: With Backup Restore**

```bash
# 1. Transfer backup dari development
scp database_backups/backup_20251229.dump user@server:/path/to/project/

# 2. Di server production
chmod +x scripts/deploy_production.sh
./scripts/deploy_production.sh
# Pilih option 2 (Restore from backup)
```

**Option 2: Fresh Database**

```bash
chmod +x scripts/deploy_production.sh
./scripts/deploy_production.sh
# Pilih option 1 (Fresh deployment)
```

### D. Enable Production Mode

Edit `docker-compose.yml`:

```yaml
services:
  web:
    # Ganti uvicorn dengan gunicorn
    command: gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
    
    # Jangan expose port langsung (pakai nginx)
    # ports:
    #   - "8000:8000"
    expose:
      - "8000"

  db:
    # Jangan expose port database ke public
    # ports:
    #   - "5433:5432"
    expose:
      - "5432"
```

Uncomment NGINX service untuk reverse proxy:

```yaml
  nginx:
    image: nginx:latest
    ports:
      - "80:80"
      - "443:443"  # Untuk SSL
    volumes:
      - ./default.conf:/etc/nginx/conf.d/default.conf
      - ./ssl:/etc/nginx/ssl  # SSL certificates
    depends_on:
      - web
```

---

## 🔐 SSL Setup (Production)

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto renewal (already setup by certbot)
sudo certbot renew --dry-run
```

---

## 💾 Database Backup Automation

Setup cron job untuk backup otomatis:

```bash
# Edit crontab
crontab -e

# Tambahkan (backup tiap hari jam 2 pagi)
0 2 * * * cd /path/to/project && ./scripts/backup_database.sh >> /var/log/db_backup.log 2>&1
```

---

## 🔄 Update Aplikasi (Future Updates)

```bash
# 1. Backup database dulu
./scripts/backup_database.sh

# 2. Update code
git pull origin main

# 3. Rebuild & restart
docker-compose down
docker-compose up -d --build

# 4. Run migrations (kalau ada)
docker-compose exec web alembic upgrade head
```

Atau pakai shortcut:

```bash
./scripts/deploy_production.sh
# Pilih option 3 (Update code only)
```

---

## 🐛 Troubleshooting

### Database Connection Error

```bash
# Check database container
docker-compose ps db

# Check logs
docker-compose logs db

# Restart database
docker-compose restart db
```

### Migration Error

```bash
# Check current migration version
docker-compose exec web alembic current

# Check migration history
docker-compose exec web alembic history

# Force stamp to latest
docker-compose exec web alembic stamp head
```

### Port Already in Use

```bash
# Stop services using port 8000
sudo lsof -ti:8000 | xargs kill -9

# Or change port in docker-compose.yml
```

---

## 📊 Monitoring

```bash
# View logs
docker-compose logs -f web
docker-compose logs -f db
docker-compose logs -f redis

# Check resource usage
docker stats

# Check service status
docker-compose ps
```

---

## 🎯 Rekomendasi untuk Anda

Berdasarkan situasi Anda (DB mixed manual + migration):

1. ✅ **Gunakan Opsi 1: Dump & Restore**
2. ✅ **Jalankan `./scripts/backup_database.sh` sekarang**
3. ✅ **Stamp Alembic setelah restore**: `alembic stamp head`
4. ✅ **Setup backup automation** (cron job)
5. ✅ **Future changes**: Gunakan migration, jangan manual query lagi

### Migration Best Practice (Kedepannya)

```bash
# Setiap kali ada perubahan struktur database:

# 1. Edit model di src/app/models/
# 2. Generate migration
docker-compose exec web alembic revision --autogenerate -m "description"

# 3. Review migration file
# 4. Test di development
docker-compose exec web alembic upgrade head

# 5. Commit migration file
git add src/migrations/versions/*.py
git commit -m "Add migration: description"

# 6. Di production, tinggal pull & migrate
git pull
docker-compose exec web alembic upgrade head
```

---

## 📞 Support

Jika ada masalah saat deployment:
1. Check logs: `docker-compose logs -f`
2. Check database connection: `docker-compose exec db psql -U user -d dbname`
3. Check Alembic status: `docker-compose exec web alembic current`

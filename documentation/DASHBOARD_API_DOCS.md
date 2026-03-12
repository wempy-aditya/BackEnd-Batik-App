# Dashboard API — Dokumentasi Integrasi Frontend

## Endpoint

**`GET /api/v1/dashboard/summary`**

Mengembalikan ringkasan statistik seluruh data di sistem. Cocok untuk ditampilkan di halaman dashboard admin.

**Akses:** Hanya user dengan `role: admin` atau `is_superuser: true`. User `registered`/`premium` akan mendapat `403 Forbidden`.

---

## Request

```javascript
const res = await fetch("/api/v1/dashboard/summary", {
  headers: {
    "Authorization": `Bearer ${accessToken}`,
  },
});

const data = await res.json();
```

---

## Response `200 OK`

```json
{
  "users": {
    "total": 6,
    "active": 6,
    "inactive": 0,
    "new_this_month": 1,
    "by_role": {
      "admin": 2,
      "registered": 4,
      "premium": 0,
      "superuser": 2
    }
  },
  "projects": {
    "total": 9,
    "by_status": {
      "published": 6,
      "draft": 3
    },
    "by_access": {
      "public": 9,
      "restricted": 0
    }
  },
  "datasets": {
    "total": 4,
    "by_status": {
      "published": 3,
      "draft": 1
    },
    "total_views": 30,
    "total_downloads": 6
  },
  "publications": {
    "total": 28,
    "by_status": {
      "published": 26,
      "draft": 2
    },
    "total_citations": 514,
    "total_views": 72,
    "total_downloads": 6
  },
  "news": {
    "total": 2,
    "by_status": {
      "published": 2,
      "draft": 0
    }
  },
  "ai_models": {
    "total": 3,
    "by_status": {
      "published": 1,
      "draft": 2
    },
    "by_access": {
      "public": 3,
      "restricted": 0
    }
  },
  "gallery": {
    "total": 5
  },
  "contributors": {
    "total": 2
  },
  "files": {
    "total": 9,
    "total_size_bytes": 6440257,
    "total_size_mb": 6.14
  },
  "categories": {
    "projects": 3,
    "datasets": 4,
    "publications": 2,
    "news": 4,
    "ai_models": 1,
    "gallery": 2
  }
}
```

---

## Penjelasan Field

### `users`
| Field | Keterangan |
|---|---|
| `total` | Total user terdaftar (tidak termasuk yang dihapus) |
| `active` | User dengan `is_active: true` |
| `inactive` | User dengan `is_active: false` (belum diaktifkan / dinonaktifkan) |
| `new_this_month` | User yang mendaftar di bulan berjalan |
| `by_role.admin` | Jumlah user dengan role admin |
| `by_role.registered` | Jumlah user dengan role registered |
| `by_role.premium` | Jumlah user dengan role premium |
| `by_role.superuser` | Jumlah user dengan `is_superuser: true` |

### `projects` / `datasets` / `publications` / `news` / `ai_models`
| Field | Keterangan |
|---|---|
| `total` | Total seluruh data |
| `by_status.published` | Jumlah yang sudah dipublikasikan |
| `by_status.draft` | Jumlah yang masih draft |
| `by_access.public` | Dapat diakses publik |
| `by_access.restricted` | Akses terbatas (registered/premium) |

### `publications` (tambahan)
| Field | Keterangan |
|---|---|
| `total_citations` | Total sitasi dari seluruh publikasi |
| `total_views` | Total jumlah view |
| `total_downloads` | Total jumlah download |

### `files`
| Field | Keterangan |
|---|---|
| `total` | Total file yang terupload |
| `total_size_bytes` | Total ukuran dalam bytes |
| `total_size_mb` | Total ukuran dalam megabytes (dibulatkan 2 desimal) |

### `categories`
Jumlah kategori yang tersedia per domain konten.

---

## Error

| Status | Pesan | Penyebab |
|---|---|---|
| `401` | `User not authenticated.` | Token tidak ada / expired |
| `403` | `Only admin users can access the dashboard.` | User bukan admin/superuser |

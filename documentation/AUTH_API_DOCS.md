# Auth API — Dokumentasi Integrasi Frontend


---

## 1. Register Akun

**`POST /auth/register`**

Endpoint publik untuk daftar akun baru. Hanya email dari domain UMM yang diizinkan. Akun yang baru didaftar **tidak langsung aktif** — admin perlu mengaktifkan terlebih dahulu.

### Request Body

```json
{
  "name": "Budi Santoso",
  "email": "budi@webmail.umm.ac.id",
  "username": "budisantoso",
  "password": "Password123!"
}
```

| Field | Tipe | Wajib | Keterangan |
|---|---|---|---|
| `name` | string | ✅ | Min 2, maks 255 karakter |
| `email` | string | ✅ | Hanya `@webmail.umm.ac.id` atau `@umm.ac.id` |
| `username` | string | ✅ | Min 2, maks 50 karakter, hanya huruf kecil & angka |
| `password` | string | ✅ | Min 8 karakter |

### Response `201 Created`

```json
{
  "id": "019ccb23-2849-72fa-a769-a36485c032cf",
  "name": "Budi Santoso",
  "username": "budisantoso",
  "email": "budi@webmail.umm.ac.id",
  "profile_image_url": null,
  "role": "registered",
  "is_active": false,
  "is_superuser": false,
  "tier_id": null,
  "created_at": "2026-03-08T01:50:00+00:00",
  "updated_at": null
}
```

> ⚠️ `is_active: false` — user belum bisa login sampai diaktifkan oleh admin.

### Error

| Status | Pesan | Penyebab |
|---|---|---|
| `422` | `Email harus menggunakan domain @webmail.umm.ac.id atau @umm.ac.id` | Email bukan dari domain UMM |
| `409` | `Email sudah terdaftar` | Email sudah dipakai akun lain |
| `409` | `Username sudah digunakan` | Username sudah dipakai akun lain |

---

## 2. Login

**`POST /login`**

Login menggunakan email atau username + password. Mengembalikan `access_token` dan menyimpan `refresh_token` di HTTP-only cookie.

> ⚠️ Endpoint ini menggunakan format `application/x-www-form-urlencoded`, bukan JSON.

### Request Body (form-data)

| Field | Tipe | Keterangan |
|---|---|---|
| `username` | string | Bisa diisi email atau username |
| `password` | string | Password akun |

### Contoh (JavaScript / fetch)

```javascript
const formData = new URLSearchParams();
formData.append("username", "budi@webmail.umm.ac.id"); // atau "budisantoso"
formData.append("password", "Password123!");

const res = await fetch("/api/v1/login", {
  method: "POST",
  headers: { "Content-Type": "application/x-www-form-urlencoded" },
  body: formData,
  credentials: "include", // penting agar cookie refresh_token tersimpan
});

const data = await res.json();
// { "access_token": "eyJ...", "token_type": "bearer" }
```

### Response `200 OK`

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

> 🍪 `refresh_token` otomatis disimpan sebagai HTTP-only cookie (tidak bisa dibaca JS).

### Token Expiry

| Token | Masa berlaku |
|---|---|
| `access_token` | 30 menit |
| `refresh_token` (cookie) | 7 hari |

### Error

| Status | Pesan | Penyebab |
|---|---|---|
| `401` | `Wrong username, email or password.` | Kredensial salah atau akun tidak aktif |

---

## 3. Refresh Access Token

**`POST /refresh`**

Memperbarui `access_token` yang sudah expired menggunakan `refresh_token` dari cookie.

### Request

Tidak perlu body. Cookie `refresh_token` dikirim otomatis oleh browser (pastikan `credentials: "include"`).

### Contoh (JavaScript / fetch)

```javascript
const res = await fetch("/api/v1/refresh", {
  method: "POST",
  credentials: "include", // kirim cookie refresh_token
});

const data = await res.json();
// { "access_token": "eyJ...", "token_type": "bearer" }
```

### Response `200 OK`

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Error

| Status | Pesan | Penyebab |
|---|---|---|
| `401` | `Refresh token missing.` | Cookie tidak ada / sudah expired |
| `401` | `Invalid refresh token.` | Token tidak valid |

---

## 4. Cara Pakai Access Token

Setiap request ke endpoint yang butuh autentikasi, sertakan `access_token` di header:

```javascript
const res = await fetch("/api/v1/user/me/", {
  headers: {
    "Authorization": `Bearer ${accessToken}`,
  },
  credentials: "include",
});
```

---

## 5. Flow Lengkap di Frontend

```
1. User isi form register → POST /auth/register
   └─ Tampilkan pesan: "Akun berhasil dibuat, menunggu aktivasi admin"

2. Setelah diaktifkan admin → User login → POST /login
   └─ Simpan access_token di memory (jangan localStorage)
   └─ refresh_token tersimpan otomatis di cookie

3. Setiap request API → sertakan Authorization: Bearer <access_token>

4. Jika dapat 401 (token expired) → POST /refresh
   └─ Dapat access_token baru → ulangi request sebelumnya

5. Logout → POST /logout (hapus cookie refresh_token)
```

---

## 6. Endpoint `/user/me/`

Untuk mengambil data user yang sedang login:

**`GET /user/me/`** *(butuh Authorization header)*

### Response

```json
{
  "id": "019aac02-ac77-7338-ac5b-3a8446f4a76d",
  "name": "Super New User",
  "username": "superuser",
  "email": "supernew@example.com",
  "profile_image_url": null,
  "role": "registered",
  "is_active": true,
  "is_superuser": false,
  "tier_id": null,
  "created_at": "2025-11-22T14:40:47+00:00",
  "updated_at": null
}
```

Field `role` yang mungkin muncul: `registered` | `admin` | `premium`

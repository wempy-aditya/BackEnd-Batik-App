# User Management Quick Reference

## 🎯 Quick Commands

### Get Admin Users
```bash
GET /api/v1/users/role/admin
```

### Get Premium Users
```bash
GET /api/v1/users/role/premium
```

### Get Registered Users
```bash
GET /api/v1/users/role/registered
```

### Get Active Users
```bash
GET /api/v1/users/status/active
```

### Get Inactive Users
```bash
GET /api/v1/users/status/inactive
```

## 🔧 Admin Operations

### Promote to Premium
```bash
PATCH /api/v1/user/{username}/admin
{
  "role": "premium"
}
```

### Deactivate User
```bash
PATCH /api/v1/user/{username}/admin
{
  "is_active": false
}
```

### Make User Admin
```bash
PATCH /api/v1/user/{username}/admin
{
  "role": "admin",
  "is_superuser": true
}
```

### Reactivate User
```bash
PATCH /api/v1/user/{username}/admin
{
  "is_active": true
}
```

## 🔑 Roles
- **admin**: Full admin access
- **registered**: Standard user
- **premium**: Premium features

## ✅ Status
- **active**: Can login
- **inactive**: Cannot login

## 📚 Full Documentation
See `USER_MANAGEMENT_GUIDE.md` for complete details.

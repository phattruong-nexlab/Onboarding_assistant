# Design: oauth-google

> ⚠️ VÍ DỤ MẪU — để team hiểu format.

---

## Metadata

```yaml
feature: oauth-google
status: tasks
based-on-requirements: 2026-01-02
updated: 2026-01-10
```

---

## Kiến trúc tổng quan

```
User → FE Button → BE /auth/google → Google OAuth → BE /auth/google/callback
                                                          ↓
                                              Tạo/link user trong DB
                                                          ↓
                                              Return JWT → FE redirect dashboard
```

---

## API Contracts

### GET /api/v1/auth/google

```http
GET /api/v1/auth/google
Authorization: không cần

// Response 302 — redirect đến Google OAuth URL
// Google URL được build với: client_id, redirect_uri, state, scope
```

### GET /api/v1/auth/google/callback

```http
GET /api/v1/auth/google/callback?code=xxx&state=yyy
Authorization: không cần
```

**Response — Success (200):**
```json
{
  "success": true,
  "data": {
    "accessToken": "string",
    "user": {
      "id": "uuid",
      "email": "string",
      "name": "string",
      "avatarUrl": "string | null",
      "isNewUser": true
    }
  }
}
```

**Response — Error (400/401):**
```json
{
  "success": false,
  "error": {
    "code": "OAUTH_FAILED | INVALID_STATE",
    "message": "Đăng nhập Google thất bại. Vui lòng thử lại."
  }
}
```

---

## Database Changes

```sql
-- Migration: 2026-01-10_add-google-oauth.sql

-- UP
ALTER TABLE users ADD COLUMN google_id VARCHAR(255) UNIQUE;
ALTER TABLE users ADD COLUMN avatar_url TEXT;
CREATE INDEX idx_users_google_id ON users(google_id);

-- DOWN
DROP INDEX idx_users_google_id;
ALTER TABLE users DROP COLUMN avatar_url;
ALTER TABLE users DROP COLUMN google_id;
```

---

## FE Implementation Notes

- **Components cần tạo:** `GoogleLoginButton` trong `components/ui/`
- **Flow:** Click → gọi `GET /auth/google` → redirect → callback xử lý token → lưu vào auth store → redirect dashboard
- **Error state:** Toast notification khi callback trả về error

---

## BE Implementation Notes

- **Library:** `authlib` (đã audit security)
- **State param:** UUID random, lưu trong Redis 10 phút
- **Scope:** `openid email profile` — tối thiểu cần thiết

---

## Security Considerations

- Validate `state` param để prevent CSRF
- Không lưu Google access token — chỉ dùng để lấy user info
- PKCE flow không cần vì server-side flow

---

## Architectural Decisions

### Decision: Server-side OAuth flow (không phải client-side)
**Context:** Cần giữ client_secret an toàn
**Options:**
1. Server-side flow — client_secret ở server
2. Client-side flow — client_secret expose ở FE
**Decision:** Server-side flow
**Rationale:** Security — client_secret không bao giờ ra client

---

## Human Review Gate ②

- [x] API contracts đủ rõ
- [x] DB schema có migration + rollback
- [x] Security được address
- [x] FE + BE owners đồng ý

**FE reviewed by:** @fe-lead  **BE reviewed by:** @be-lead
**Date:** 2026-01-10  **Status:** ✅ Approved

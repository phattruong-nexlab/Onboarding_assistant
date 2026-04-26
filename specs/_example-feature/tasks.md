# Tasks: oauth-google

> ⚠️ VÍ DỤ MẪU — để team hiểu format.

---

## Metadata

```yaml
feature: oauth-google
status: implementing
total-tasks: 4
completed-tasks: 1
updated: 2026-01-15
```

---

## Thứ tự implementation

```
TASK-001 (BE: DB migration)
    ↓
TASK-002 (BE: OAuth service + endpoints)
    ↓
TASK-003 (FE: Google login button + flow)
    ↓
TASK-004 (BE+FE: Integration tests)
```

---

## Tasks

### TASK-001: DB Migration — Add Google OAuth fields

```yaml
id: TASK-001
scope: BE
status: done
depends-on: []
estimate: 20min
assignee: Claude
```

**Mô tả:** Tạo migration file thêm `google_id` và `avatar_url` vào bảng `users`.

**Acceptance Criteria:**
- [x] Migration file có cả UP và DOWN
- [x] `google_id` là VARCHAR(255) UNIQUE
- [x] Index được tạo trên `google_id`
- [x] Migration chạy thành công trên local

**Files đã thay đổi:**
- `backend/migrations/2026-01-10_add-google-oauth.sql` — tạo mới

---

### TASK-002: BE — OAuth Service và Endpoints

```yaml
id: TASK-002
scope: BE
status: in-progress
depends-on: [TASK-001]
estimate: 2h
assignee: Claude
```

**Mô tả:** Implement Google OAuth flow: redirect endpoint và callback endpoint.

**Acceptance Criteria:**
- [ ] `GET /api/v1/auth/google` redirect đến Google OAuth URL
- [ ] State param được tạo và lưu vào Redis với TTL 10 phút
- [ ] `GET /api/v1/auth/google/callback` validate state param
- [ ] Nếu user mới: tạo account tự động
- [ ] Nếu user cũ cùng email: link Google account
- [ ] Trả về accessToken và set refresh token cookie
- [ ] Unit tests với mock Google API pass

**Files sẽ thay đổi:**
- `backend/src/services/google-oauth.service.ts` — tạo mới
- `backend/src/api/v1/auth.routes.ts` — thêm 2 routes
- `backend/tests/services/google-oauth.service.test.ts` — tạo mới

---

### TASK-003: FE — Google Login Button và Flow

```yaml
id: TASK-003
scope: FE
status: pending
depends-on: [TASK-002]
estimate: 1.5h
assignee: Claude
```

**Mô tả:** Thêm Google login button vào trang auth, handle OAuth callback.

**Acceptance Criteria:**
- [ ] `GoogleLoginButton` component hiển thị đúng design
- [ ] Click button gọi `GET /api/v1/auth/google` và redirect
- [ ] Callback page đọc token từ response và lưu vào auth store
- [ ] Redirect đến dashboard sau khi thành công
- [ ] Hiển thị error toast nếu OAuth fail
- [ ] Component test pass

**Files sẽ thay đổi:**
- `frontend/src/components/ui/GoogleLoginButton.tsx` — tạo mới
- `frontend/src/app/(auth)/login/page.tsx` — thêm button
- `frontend/src/app/(auth)/callback/page.tsx` — tạo mới
- `frontend/src/services/auth.service.ts` — thêm google auth methods

---

### TASK-004: Integration Tests

```yaml
id: TASK-004
scope: BE
status: pending
depends-on: [TASK-002, TASK-003]
estimate: 1h
assignee: Claude
```

**Mô tả:** End-to-end integration tests cho OAuth flow.

**Acceptance Criteria:**
- [ ] Test: new user flow hoàn thành được
- [ ] Test: existing user linking hoàn thành được
- [ ] Test: invalid state param bị reject
- [ ] Test: Google error được handle gracefully

---

## Human Review Gate ③

- [x] Mỗi task < 4h
- [x] Dependencies map rõ
- [x] Acceptance criteria measurable
- [x] Không có task mơ hồ

**Reviewed by:** @tech-lead  **Date:** 2026-01-12  **Status:** ✅ Approved

---

## Implementation Log

| Task | Started | Completed | Agent | Notes |
|------|---------|-----------|-------|-------|
| TASK-001 | 2026-01-13 | 2026-01-13 | Claude | Done |
| TASK-002 | 2026-01-14 | — | Claude | In progress |
| TASK-003 | — | — | — | — |
| TASK-004 | — | — | — | — |

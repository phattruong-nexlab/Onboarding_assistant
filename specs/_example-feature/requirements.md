# Requirements: oauth-google

> ⚠️ ĐÂY LÀ VÍ DỤ MẪU — để team hiểu format. Xóa folder này khi không cần nữa.

---

## Metadata

```yaml
feature: oauth-google
scope: Both
fe-owner: "@fe-lead"
be-owner: "@be-lead"
status: tasks
depends-on: []
created: 2026-01-01
updated: 2026-01-15
```

---

## Mục tiêu & Business Value

Cho phép người dùng đăng nhập bằng tài khoản Google, giảm friction onboarding và tăng conversion rate.

**Business value:**
- Giảm bỏ cuộc ở bước đăng ký (không cần tạo password)
- Tăng trust (dùng Google auth)

---

## User Stories

- Là new user, tôi muốn đăng nhập bằng Google để không cần tạo mật khẩu mới
- Là user cũ có cùng email với Google account, tôi muốn link tài khoản tự động

---

## Acceptance Criteria (EARS Format)

### Happy Path
```
WHEN  user click nút "Tiếp tục với Google"
THEN  app mở OAuth consent screen của Google

IF    user đồng ý và xác thực thành công
THEN  app redirect về dashboard với user đã đăng nhập

IF    email Google account chưa có trong hệ thống
THEN  tạo tài khoản mới tự động và redirect dashboard

IF    email Google account đã có trong hệ thống
THEN  link Google account vào tài khoản hiện có và redirect dashboard
```

### Edge Cases
```
IF    user từ chối consent trên Google
THEN  redirect về trang login với message "Đăng nhập bị hủy"

IF    Google OAuth bị lỗi (network, service down)
THEN  hiện error message rõ ràng, không crash app

WHEN  state parameter không hợp lệ (CSRF attempt)
THEN  reject request, log security event, redirect login
```

### Out of Scope
- Facebook, GitHub OAuth (sprint sau)
- Mobile app OAuth deep link
- Disconnect Google account

---

## Non-Functional Requirements

- **Performance:** OAuth redirect phải hoàn thành trong < 3s
- **Security:** PKCE flow, validate state param chống CSRF

---

## Human Review Gate ①

- [x] Acceptance criteria đủ rõ
- [x] Out of scope define rõ
- [x] Không còn câu hỏi bỏ ngỏ

**Reviewed by:** @pm  **Date:** 2026-01-02  **Status:** ✅ Approved

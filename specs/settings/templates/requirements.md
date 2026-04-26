# Requirements: [Feature Name]

<!--
TEMPLATE — Xóa comment này khi dùng thật.
Format: EARS (Easy Approach to Requirements Syntax)
  WHEN  [điều kiện xảy ra] THEN [kết quả mong đợi]
  IF    [điều kiện đúng]   THEN [kết quả]
  WHILE [đang trong trạng thái X] [hành vi mong đợi]
-->

---

## Metadata

```yaml
feature: [feature-name]           # kebab-case, khớp với tên folder
scope: Both                        # FE | BE | Both
fe-owner: "@member"
be-owner: "@member"
status: requirements               # requirements | design | tasks | implementing | done
depends-on: []                     # VD: [oauth-google, user-profile]
created: YYYY-MM-DD
updated: YYYY-MM-DD
```

---

## Mục tiêu & Business Value

[Mô tả ngắn gọn: Feature này giải quyết vấn đề gì? Tại sao cần build?]

**Business value:**
- [Benefit 1]
- [Benefit 2]

---

## User Stories

- Là **[vai trò]**, tôi muốn **[hành động]** để **[mục đích]**
- Là **[vai trò]**, tôi muốn **[hành động]** để **[mục đích]**

---

## Acceptance Criteria (EARS Format)

### Happy Path
```
WHEN  [người dùng thực hiện hành động X]
THEN  [hệ thống phản hồi Y]

IF    [điều kiện A thỏa mãn]
THEN  [kết quả B xảy ra]
```

### Edge Cases
```
IF    [điều kiện đặc biệt]
THEN  [hành vi mong đợi]

WHEN  [lỗi xảy ra]
THEN  [error handling]
```

### Không thuộc scope (Out of Scope)
- [Thứ gì đó liên quan nhưng KHÔNG build trong feature này]
- [Thứ gì đó sẽ làm sau]

---

## Non-Functional Requirements

- **Performance:** [VD: API response < 200ms p95]
- **Security:** [VD: Endpoint cần authentication]
- **Accessibility:** [VD: WCAG 2.1 AA]
- **Browser support:** [VD: Chrome, Safari, Firefox latest 2]

---

## Câu hỏi cần làm rõ (Trả lời trước khi vào Design)

- [ ] [Câu hỏi 1 — ai trả lời, deadline]
- [ ] [Câu hỏi 2]

---

## Human Review Gate ①

- [ ] Acceptance criteria đủ rõ để implement không cần hỏi thêm?
- [ ] Out of scope được define rõ?
- [ ] Non-functional requirements realistic?
- [ ] Không còn câu hỏi nào chưa được trả lời?

**Reviewed by:** @____  **Date:** YYYY-MM-DD  **Status:** ☐ Approved / ☐ Changes needed

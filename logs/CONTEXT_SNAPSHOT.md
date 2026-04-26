# Context Snapshot

> File này là trạng thái hiện tại của project.
> **Human:** Đọc Section A để biết tình hình.
> **Claude:** Đọc cả 2 sections khi bắt đầu session mới.
> **Cập nhật:** Cuối mỗi session — chạy `/log-session`

---

## Section A — Human View

**Cập nhật lần cuối:** YYYY-MM-DD bởi [@member | Claude]

### Sprint hiện tại
- **Sprint:** [Sprint name / số]
- **Mục tiêu:** [Đang build gì?]
- **Deadline:** YYYY-MM-DD

### Đang làm
| Feature | Task | Owner | Status |
|---------|------|-------|--------|
| [feature-name] | TASK-001 | @member | 🔄 In Progress |

### Blocked
| Feature | Task | Lý do | Cần gì để unblock |
|---------|------|-------|-------------------|
| | | | |

### Hoàn thành gần đây (3 items)
- ✅ [Feature/Task] — YYYY-MM-DD
- ✅ [Feature/Task] — YYYY-MM-DD
- ✅ [Feature/Task] — YYYY-MM-DD

### Bước tiếp theo (Next session)
1. [Hành động cụ thể]
2. [Hành động cụ thể]

---

## Section B — Agent View

> Claude đọc phần này để hiểu technical state.

### Active Spec
```
Feature:    [feature-name]
Phase:      requirements | design | tasks | implementing
File:       specs/[feature-name]/[phase].md
Last task:  TASK-XXX (status: pending | in-progress)
```

### Quyết định kỹ thuật gần nhất (3 items)
1. **[YYYY-MM-DD]** [Quyết định gì] — Lý do: [tại sao]
2. **[YYYY-MM-DD]** [Quyết định gì] — Lý do: [tại sao]
3. **[YYYY-MM-DD]** [Quyết định gì] — Lý do: [tại sao]

### Files quan trọng đang thay đổi
```
frontend/src/[path]/   ← [đang làm gì]
backend/src/[path]/    ← [đang làm gì]
```

### Dependency đang chờ
- [Feature X] đang chờ [TASK-YYY] của [Feature Z] trước khi có thể tiếp tục

### Known issues / Tech debt cần nhớ
- [Issue 1 — xem TECH_DEBT.md để biết thêm]

### Contracts mới nhất
```
Đã update API_CONTRACTS.md: YYYY-MM-DD
Endpoint mới nhất: [POST /api/v1/...]
```

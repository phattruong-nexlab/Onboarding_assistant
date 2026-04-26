# Tasks: [Feature Name]

<!--
TEMPLATE — Xóa comment này khi dùng thật.
Điền vào sau khi design.md được approved.
Mỗi task phải atomic — có thể implement độc lập trong 1 session.

SCOPE:
  [BE]     → Backend task
  [FE]     → Frontend task
  [Mobile] → Mobile task
  [All]    → Ảnh hưởng nhiều layers (thường là DB migration, API contract change)

CROSS-LAYER RULE:
  Nếu TASK-A là [BE] và TASK-B là [FE] depend on TASK-A
  → FE mock API trước, implement thật sau khi BE done
  → KHÔNG block nhau nếu có thể mock
-->

---

## Metadata

```yaml
feature: [feature-name]
status: tasks
layers: [FE, BE, Mobile]   # Xóa layer không có
total-tasks: 0
completed-tasks: 0
updated: YYYY-MM-DD
```

---

## Dependency Graph

```
[TASK-001] BE: DB migration
    ↓
[TASK-002] BE: API endpoints
    ↓              ↓
[TASK-003] FE   [TASK-004] Mobile   ← Song song được
    ↓              ↓
[TASK-005] Integration tests
```

---

## Tasks

### TASK-001: [Tên task]

```yaml
id: TASK-001
scope: BE          # BE | FE | Mobile | All
status: pending    # pending | in-progress | done | blocked
depends-on: []
estimate: [VD: 30min | 1h | 2h]
assignee: Claude
```

**Mô tả:** [Giải thích task làm gì — 1-2 câu]

**Acceptance Criteria:**
- [ ] [Criterion 1 — measurable, testable]
- [ ] [Criterion 2]
- [ ] Tests pass

**Files sẽ thay đổi:**
- `[path/to/file]` — [tạo mới / sửa / xóa]

---

### TASK-002: [Tên task]

```yaml
id: TASK-002
scope: FE
status: pending
depends-on: [TASK-001]
estimate: 1h
assignee: Claude
```

**Mô tả:** [Giải thích task làm gì]

**Acceptance Criteria:**
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] Tests pass

**Files sẽ thay đổi:**
- `[path/to/file]` — [mô tả]

---

### TASK-003: [Tên task — Mobile]

```yaml
id: TASK-003
scope: Mobile
status: pending
depends-on: [TASK-001]
estimate: 2h
assignee: Claude
```

**Mô tả:** [Giải thích task làm gì]

**Acceptance Criteria:**
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] Tests pass
- [ ] Human verify trên app thật ← BẮT BUỘC với mọi Mobile task

**Files sẽ thay đổi:**
- `[path/to/file]` — [mô tả]

---

## Human Review Gate ③

- [ ] Mỗi task < 4h?
- [ ] Dependencies map rõ — biết task nào có thể song song?
- [ ] Acceptance criteria measurable — không mơ hồ?
- [ ] Mobile tasks có "verify trên app thật" trong AC?
- [ ] Cross-layer tasks được đánh dấu rõ?

**Reviewed by:** @[name] **Date:** YYYY-MM-DD **Status:** [ ] Approved

---

## Implementation Log

| Task | Scope | Started | Completed | Agent | Notes |
|------|-------|---------|-----------|-------|-------|
| TASK-001 | BE | — | — | — | — |
| TASK-002 | FE | — | — | — | — |
| TASK-003 | Mobile | — | — | — | — |

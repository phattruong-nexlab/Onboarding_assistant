# Skill: spec-impl

## Trigger
`/spec-impl [feature-name]` — chỉ chạy sau khi tasks.md được human approve (Gate ③).

## Mục đích
Implement tất cả tasks trong `specs/[feature-name]/tasks.md` bằng subagents.
1 task = 1 subagent = 1 context sạch.

## Pre-condition
- `specs/[feature-name]/tasks.md` phải có trạng thái Approved ở Human Review Gate ③
- `docs/API_CONTRACTS.md` phải đã được update với contracts từ design.md
- Nếu chưa đủ điều kiện → STOP, báo human

## Các bước thực hiện

### 1. Đọc và parse tasks.md
- List tất cả tasks có `status: pending`
- Build dependency graph
- Xác định tasks có thể chạy song song (không có dependency vào nhau)

### 2. Xác định thứ tự thực hiện
```
Ví dụ dependency graph:
TASK-001 (BE, no deps) ─┐
TASK-002 (BE, deps: 001) ─┤→ TASK-004 (FE, deps: 002)
TASK-003 (BE, no deps) ─┘
```

### 3. Implement từng task (theo thứ tự)

Với mỗi task, spawn subagent với context:

```
Bạn là implementation agent cho [TASK-XXX].

Đọc trước:
- specs/[feature]/tasks.md (phần TASK-XXX)
- specs/[feature]/design.md (contracts liên quan)
- [frontend|backend]/CLAUDE.md (rules của side này)
- .claude/rules/[frontend|backend].md

Yêu cầu:
- Implement đúng acceptance criteria
- Viết tests (TDD nếu có thể: test trước, code sau)
- Không hardcode secrets
- Follow conventions trong steering/conventions.md
- Nếu blocked: ghi vào tasks.md và report lại

Chỉ làm TASK-XXX. Không làm task khác.
```

### 4. Sau mỗi task

```
Chạy tests:
  cd [frontend|backend] && [test command]

Nếu pass:
  → @spec-compliance-reviewer: "Review TASK-XXX theo specs/[feature]/tasks.md"
  → Nếu Stage 1 pass → @code-quality-reviewer: "Review TASK-XXX quality"
  → Nếu Stage 2 pass → /finish-task TASK-XXX

Nếu fail:
  → Fix, chạy lại tests
  → Tối đa 3 lần retry, sau đó escalate lên human
```

### 5. Khi bị blocked

```
IF task blocked (unclear requirement, missing dependency):
  → Update tasks.md: status: blocked, reason: "[lý do cụ thể]"
  → Update logs/CONTEXT_SNAPSHOT.md section Blocked
  → Skip task này, tiếp tục task tiếp theo nếu có thể
  → Báo human cuối batch: "[TASK-XXX] bị blocked vì [lý do]"

KHÔNG assume và tự giải quyết khi không chắc chắn.
```

### 6. Báo cáo khi xong batch

```
## Implementation Report: [feature-name]
Date: YYYY-MM-DD

✅ Completed: TASK-001, TASK-002, TASK-003
🚫 Blocked: TASK-004 — [lý do]
⏭️ Skipped: none

Bước tiếp theo:
- Human resolve TASK-004 blocker
- Chạy /run-evaluation [fe|be|both] khi ready
```

## Rules
- KHÔNG bắt đầu implement nếu tasks.md chưa được approve
- KHÔNG implement task có dependency chưa done
- KHÔNG commit khi tests fail
- KHÔNG tự quyết định khi spec mơ hồ — hỏi human
- Commit message format: `feat([feature-name]): TASK-XXX [mô tả ngắn]`

# Skill: log-session

## Trigger
`/log-session` — cuối mỗi session làm việc.
Cũng được nhắc tự động bởi instinct `always-update-log.md`.

## Mục đích
Update CONTEXT_SNAPSHOT.md và SESSION_LOG.md để session sau biết đang ở đâu.

## Các bước thực hiện

### 1. Thu thập thông tin session hiện tại

Tự hỏi và trả lời:
- Đã làm xong những gì?
- Quyết định kỹ thuật quan trọng nào đã đưa ra?
- Task nào đang dở hoặc blocked?
- Bước tiếp theo là gì?
- Có thay đổi gì về contracts/architecture không?

### 2. Update CONTEXT_SNAPSHOT.md

**Section A (Human View):**
```markdown
**Cập nhật lần cuối:** [today] bởi Claude

### Đang làm
[Cập nhật status hiện tại]

### Blocked
[Thêm blockers mới nếu có, xóa những cái đã resolve]

### Hoàn thành gần đây
[Thêm những thứ done trong session này, giữ 3 items gần nhất]

### Bước tiếp theo
[Cập nhật next actions cụ thể]
```

**Section B (Agent View):**
```markdown
### Active Spec
[Cập nhật phase và task hiện tại]

### Quyết định kỹ thuật gần nhất
[Thêm decisions mới trong session này, giữ 3 items gần nhất]

### Files quan trọng đang thay đổi
[Cập nhật files đang modify]
```

### 3. Append vào SESSION_LOG.md

```markdown
## Session [YYYY-MM-DD] [HH:MM]

**Who:** Claude | @member
**Feature:** [feature-name]

### Hoàn thành
- [TASK-XXX] [mô tả ngắn gọn]
- [Việc gì khác đã làm]

### Quyết định đưa ra
- [Quyết định] — lý do: [tại sao]

### Blocked / Issues
- [Nếu có]

### Session tiếp theo
- [Bước tiếp theo cụ thể]
```

### 4. Báo cáo
```
✅ Logs đã được update:
  - logs/CONTEXT_SNAPSHOT.md
  - logs/SESSION_LOG.md

Session có thể đóng an toàn.
Session tiếp theo bắt đầu bằng: đọc .claude/skills/getting-started/SKILL.md
```

# Skill: finish-task

## Trigger
`/finish-task [TASK-XXX]` — sau khi task pass cả 2 review stages.

## Mục đích
Verify task thực sự done, commit, và update logs.

## Các bước thực hiện

### 1. Verify Definition of Done
Đọc `process/DEFINITION_OF_DONE.md` và check từng tiêu chí:

```
Task Level checklist:
[ ] Acceptance criteria trong tasks.md đều pass?
[ ] Tests viết và pass?
[ ] Không có linting errors?
[ ] Spec Compliance review đã pass?
[ ] Code Quality review đã pass?
[ ] Không có hardcoded secrets?
[ ] Error handling đầy đủ?
```

Nếu bất kỳ item nào chưa pass → STOP, không commit, fix trước.

### 2. Run final checks
```bash
# Chạy lần cuối trước khi commit
cd [frontend|backend]
[lint command]
[test command]
```

### 3. Commit
```bash
git add [files liên quan đến task này]
git commit -m "feat([feature-name]): TASK-XXX [mô tả ngắn gọn]"
```

### 4. Update tasks.md
```yaml
# Trong specs/[feature]/tasks.md — task vừa done
status: done
completed: YYYY-MM-DD
agent: Claude | @member
```

### 5. Update Implementation Log trong tasks.md
```markdown
| TASK-XXX | [started] | [today] | Claude | [notes nếu có] |
```

### 6. Update ALL_TASKS.md nếu toàn bộ feature done

### 7. Báo cáo
```
✅ TASK-XXX hoàn thành và committed.

Nếu đây là task cuối của feature:
→ Chạy /run-evaluation [fe|be|both] để evaluate
→ Hoặc tiếp tục với task tiếp theo trong batch
```

# Skill: validate-design

## Trigger
`/validate-design [feature-name]` — optional, chạy sau spec-tasks trước khi human review Gate ③.

## Mục đích
Verify tasks trong `specs/[feature]/tasks.md` align với architecture tổng thể.
Phát hiện tasks có thể conflict với patterns đang có trong codebase.

## Các bước thực hiện

### 1. Đọc tasks cần validate
- `specs/[feature]/tasks.md`
- `specs/[feature]/design.md`

### 2. Check alignment với architecture
- `docs/ARCHITECTURE.md` — folder structure có đúng không?
- `steering/conventions.md` — conventions có được follow không?
- Existing code patterns — tasks có theo đúng pattern đang dùng không?

```bash
# Scan existing patterns
find frontend/src/services/ -name "*.ts" | head -5   # FE service pattern
find backend/src/services/ -name "*.ts" | head -5    # BE service pattern
find backend/migrations/ -name "*.sql" | tail -3     # Migration pattern
```

### 3. Verify task estimates thực tế

Với mỗi task estimate, check:
- Số files cần tạo/sửa có khớp với estimate không?
- Complexity có bị underestimate không?

### 4. Check dependency conflicts

- Có task nào modify cùng file mà không có dependency link?
- Có circular dependency nào không?

### 5. Báo cáo

```markdown
## Validate Design Report: [feature-name]

### ✅ Aligned
- Tasks follow existing folder structure
- API patterns consistent với codebase

### ⚠️ Concerns

#### Architecture Misalignment
- TASK-002 tạo service trong `backend/src/api/` — nên là `backend/src/services/`

#### Estimate Review
- TASK-003 estimate 30min nhưng cần sửa 5 files — recommend: 2h

#### Missing Dependencies
- TASK-004 sửa `auth.service.ts` — TASK-001 cũng sửa file này, cần thêm dependency

### Recommendation
[Fix những concerns trên trước khi human review Gate ③]
```

## Rules
- Không sửa tasks.md — chỉ báo cáo
- Nếu không có concerns → nói rõ "Không phát hiện vấn đề" thay vì im lặng

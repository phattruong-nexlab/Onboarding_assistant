# Skill: spec-check

## Trigger
`/spec-check [feature-name]` hoặc `/spec-check [TASK-XXX]`
Thường chạy trước khi escalate lên human hoặc khi muốn tự verify.

## Mục đích
Audit implementation đang có so với acceptance criteria trong spec.
Tương tự spec-compliance-reviewer nhưng chạy bởi Generator tự check — không phải reviewer độc lập.

## Phân biệt với spec-compliance-reviewer

| | spec-check | spec-compliance-reviewer |
|---|---|---|
| Chạy bởi | Generator tự kiểm tra | Reviewer độc lập |
| Khi nào | Trước khi submit review | Sau khi Generator nói "xong" |
| Mục đích | Self-check | Independent verification |

## Các bước thực hiện

### 1. Đọc spec
```
specs/[feature]/tasks.md  → acceptance criteria
specs/[feature]/design.md → API contracts, expected behavior
```

### 2. Verify từng criterion

```
Với mỗi acceptance criterion:
→ Tìm trong code: file nào implement?
→ Tìm trong tests: test nào cover?
→ Kết luận: DONE / MISSING / PARTIAL
```

### 3. Tạo báo cáo self-check

```markdown
## Spec Check: [TASK-XXX]

### Acceptance Criteria

✅ [Criterion 1] — `services/auth.service.ts:45`, test: `auth.test.ts:12`
✅ [Criterion 2] — `routes/auth.ts:23`
⚠️ [Criterion 3] — PARTIAL: happy path done, error case missing
❌ [Criterion 4] — MISSING: chưa implement

### Missing Items
1. [Criterion 3]: cần add error handling cho case X
2. [Criterion 4]: chưa có, cần implement Y

### Verdict
NOT READY for review — fix 2 items trên trước.
```

### 4. Nếu không sẵn sàng
Fix những thứ còn thiếu rồi chạy lại `/spec-check`.

### 5. Nếu sẵn sàng
```
✅ Spec Check PASS — sẵn sàng submit review.
→ @spec-compliance-reviewer để bắt đầu Stage 1 review.
```

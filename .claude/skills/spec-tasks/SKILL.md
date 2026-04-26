# Skill: spec-tasks

## Trigger
`/spec-tasks [feature-name]` — chỉ chạy sau khi design.md được human approve (Gate ②).

## Mục đích
Break feature thành atomic tasks trong `specs/[feature-name]/tasks.md`.
Mỗi task phải implement được trong 1 session (< 4h) bởi 1 subagent.

## Pre-condition
- `specs/[feature-name]/design.md` phải có trạng thái Approved ở Human Review Gate ②
- Nếu chưa approved → STOP, báo human

## Các bước thực hiện

### 1. Đọc design.md đầy đủ
- API contracts — bao nhiêu endpoints?
- DB changes — có migration không?
- FE vs BE implementation notes
- Security considerations

### 2. Identify atomic units

Atomic task = một trong các loại sau:
- Một migration file
- Một service/module mới
- Một group endpoints liên quan chặt chẽ
- Một component FE
- Một batch tests

**KHÔNG** gộp FE và BE vào cùng 1 task trừ khi cực kỳ nhỏ.

### 3. Map dependencies

```
Hỏi với mỗi task: "Task này có thể bắt đầu ngay không?"
Nếu không: "Cần task nào xong trước?"
```

### 4. Estimate từng task

```
S: < 1h  (thêm 1 field, sửa 1 validation)
M: 1-3h  (1 service mới, 1 component với tests)
L: 3-6h  (complex feature, nhiều files)
XL: > 6h → PHẢI tách nhỏ hơn
```

### 5. Viết tasks.md theo template

Điền đầy đủ cho mỗi task:
- `id`, `scope`, `depends-on`, `estimate`
- Mô tả rõ ràng
- Acceptance criteria measurable
- Files sẽ thay đổi

### 6. Draw dependency diagram

```
TASK-001 → TASK-002 → TASK-004
               ↘ TASK-003 (song song với 004)
```

### 7. Update thứ tự implementation trong tasks.md

### 8. Nhắc validate-design (optional)

```
💡 Chạy /validate-design [feature-name] để verify tasks align với architecture hiện có.
```

### 9. Nhắc Human Review Gate ③

```
✅ tasks.md sẵn sàng review.

Tổng: [X] tasks — FE: [X], BE: [X], Both: [X]
Estimate tổng: ~[Xh]
Critical path: TASK-001 → TASK-002 → TASK-004

Sau khi approve → /spec-impl [feature-name]
```

## Rules

- Không có task nào > 6h — phải tách nhỏ hơn
- Mỗi task phải có ít nhất 1 acceptance criteria verifiable
- Không để task scope "Both" nếu có thể tách FE/BE riêng
- Không tự approve — phải human review Gate ③

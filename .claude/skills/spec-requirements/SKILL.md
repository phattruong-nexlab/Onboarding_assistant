# Skill: spec-requirements

## Trigger
`/spec-requirements [feature-name]` hoặc "viết requirements cho [feature]"

## Mục đích
Generate `specs/[feature-name]/requirements.md` theo EARS format.
Đặt câu hỏi làm rõ TRƯỚC — không assume, không implement.

## Các bước thực hiện

### 1. Đọc context
- `specs/[feature-name]/requirements.md` (template đã có)
- `logs/CONTEXT_SNAPSHOT.md` (hiểu project context)
- `steering/tech-stack.md` (hiểu môi trường)
- `ALL_TASKS.md` (xem feature này liên quan gì)

### 2. Đặt câu hỏi làm rõ (QUAN TRỌNG)
Trước khi viết bất cứ thứ gì, hỏi human những điểm chưa rõ:

```
Trước khi viết requirements cho [feature-name], tôi cần làm rõ:

1. [Câu hỏi về user role / ai dùng feature này]
2. [Câu hỏi về happy path chính]
3. [Câu hỏi về edge cases quan trọng]
4. [Câu hỏi về out of scope]
5. [Câu hỏi về non-functional nếu cần]

Trả lời xong, tôi sẽ viết requirements.md ngay.
```

### 3. Viết requirements.md
Dựa trên thông tin nhận được, fill in theo template:
- User stories từ góc nhìn người dùng
- Acceptance criteria theo EARS (WHEN/IF/WHILE/THEN)
- Define rõ Out of Scope
- Non-functional requirements nếu có

### 4. Highlight những điểm còn mơ hồ
Sau khi viết xong, liệt kê:
```
⚠️ Những điểm vẫn cần làm rõ trước khi approve:
1. [Điểm mơ hồ 1]
2. [Điểm mơ hồ 2]
```

### 5. Nhắc Human Review Gate ①
```
✅ requirements.md đã sẵn sàng cho review.
📋 Checklist review: specs/[feature-name]/requirements.md (cuối file)

Sau khi approve → chạy /spec-design [feature-name]
```

## Rules
- KHÔNG viết solution trong requirements (không đề cập API, database, component)
- KHÔNG assume business logic — hỏi nếu không chắc
- KHÔNG bỏ qua Out of Scope — rất quan trọng để tránh scope creep

# Skill: spec-design

## Trigger
`/spec-design [feature-name]` — chỉ chạy sau khi requirements.md được human approve.

## Mục đích
Generate `specs/[feature-name]/design.md` — technical contract giữa FE và BE.

## Pre-condition
- `specs/[feature-name]/requirements.md` phải có trạng thái Approved ở Human Review Gate ①
- Nếu chưa approved → STOP, báo human

## Các bước thực hiện

### 1. Đọc context
- `specs/[feature-name]/requirements.md` (approved)
- `docs/API_CONTRACTS.md` (existing contracts — tránh conflict)
- `docs/ARCHITECTURE.md` (existing architecture)
- `steering/api-standards.md` (response format, naming...)
- `steering/security.md` (security requirements)

### 2. Phân tích và design

**API Contracts:**
- List tất cả endpoints cần thiết
- Define request/response schema đầy đủ
- Đảm bảo tuân theo `steering/api-standards.md`
- Check không conflict với `docs/API_CONTRACTS.md`

**Database:**
- List mọi schema changes cần thiết
- Viết migration SQL (up + down)
- Thêm indexes cần thiết

**Security:**
- Endpoint nào cần auth?
- Input nào cần validate?
- Có sensitive data nào không?

**ADR (nếu có quyết định kỹ thuật quan trọng):**
- Document alternatives đã xem xét
- Giải thích lý do chọn approach này
- Nêu trade-offs

### 3. Viết design.md theo template

### 4. Nhắc về validate-gap (optional)
```
💡 Tip: Chạy /validate-gap [feature-name] để check xem design có conflict
với code hiện tại không (đặc biệt quan trọng nếu đây là brownfield feature).
```

### 5. Nhắc Human Review Gate ②
```
✅ design.md sẵn sàng review — cần cả FE owner và BE owner review.
📋 Đặc biệt chú ý: API contracts và DB schema.

Sau khi approve:
1. Copy API contracts vào docs/API_CONTRACTS.md
2. Chạy /spec-tasks [feature-name]
```

## Rules
- KHÔNG design nếu requirements chưa approved
- Contract phải đủ rõ để FE và BE implement độc lập — không cần hỏi nhau
- Mọi endpoint phải tuân theo api-standards.md
- Migration phải có cả up và down

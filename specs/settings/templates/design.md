# Design: [Feature Name]

<!--
TEMPLATE — Xóa comment này khi dùng thật.
Điền vào sau khi requirements.md được approved.
Đây là technical contract — tất cả layers phải đồng ý trước khi implement.

CÁCH DÙNG SECTIONS:
- "## API Contracts" → TẤT CẢ layers đọc — đây là nguồn sự thật duy nhất
- "## BE Implementation" → chỉ BE đọc và implement
- "## FE Implementation" → chỉ FE đọc và implement
- "## Mobile Implementation" → chỉ Mobile đọc và implement
- Xóa section của layer nào không có trong project
-->

---

## Metadata

```yaml
feature: [feature-name]
status: design
layers: [FE, BE, Mobile]        # Xóa layer không có trong project
based-on-requirements: YYYY-MM-DD
updated: YYYY-MM-DD
```

---

## Kiến trúc tổng quan

[Mô tả ngắn: feature này fit vào system như thế nào?]

```
[Diagram đơn giản — luồng từ user đến data]
User → FE/Mobile → API → BE Service → DB
```

---

## API Contracts
<!-- ★ TẤT CẢ LAYERS ĐỌC — Single source of truth ★ -->
<!-- Sau khi approved: copy section này vào docs/API_CONTRACTS.md -->

### [METHOD] /api/v1/[resource]

**Request:**
```json
{
  "field": "type"
}
```

**Response (200):**
```json
{
  "data": {},
  "meta": {}
}
```

**Error cases:**
| Status | Code | Khi nào |
|--------|------|---------|
| 400 | VALIDATION_ERROR | [mô tả] |
| 401 | UNAUTHORIZED | [mô tả] |
| 404 | NOT_FOUND | [mô tả] |

---

## Database Changes
<!-- ★ TẤT CẢ LAYERS ĐỌC để hiểu data model ★ -->

### Migration
```sql
-- UP
ALTER TABLE [table] ADD COLUMN [col] [type];

-- DOWN
ALTER TABLE [table] DROP COLUMN [col];
```

### Schema sau thay đổi
```
[table]: [mô tả ngắn]
  - [col]: [type] — [mô tả]
```

---

## BE Implementation
<!-- Chỉ BE đọc — FE/Mobile không cần -->

### Services cần tạo/sửa
- `[service-name]`: [làm gì]

### Business logic quan trọng
- [Logic 1]
- [Logic 2]

### Security
- Auth required: [yes/no]
- Input validation: [mô tả]
- Rate limiting: [có/không, giới hạn]

---

## FE Implementation
<!-- Chỉ FE đọc — BE/Mobile không cần -->

### Components cần tạo/sửa
- `[ComponentName]`: [làm gì]

### State management
- [Mô tả state cần manage]

### API calls
- Dùng service layer — không fetch trực tiếp từ component
- Handle: loading / success / error states

### UX notes
- [Behavior cụ thể cần chú ý]
- [Loading state trông như thế nào]
- [Error message hiển thị gì]

---

## Mobile Implementation
<!-- Chỉ Mobile đọc — BE/FE không cần -->

### Screens/Components cần tạo/sửa
- `[ScreenName]`: [làm gì]

### API/GraphQL operations
<!-- Nếu dùng GraphQL: liệt kê queries/mutations cần thêm vào GRAPHQL_CONTRACTS.md -->
<!-- Nếu dùng REST: liệt kê endpoints từ API Contracts section ở trên cần gọi -->
- `[OperationName]`: [mô tả]

### Navigation flow
```
[Screen A] → [action] → [Screen B]
```

### Platform notes
- iOS: [nếu có gì đặc biệt]
- Android: [nếu có gì đặc biệt]

### Verify guide (draft)
<!-- Flutter generator sẽ tự động tạo how-to-verify chi tiết sau khi implement -->
- [ ] [Bước verify 1]
- [ ] [Bước verify 2]

---

## Cross-Layer Dependencies
<!-- Điền nếu layers có dependency với nhau -->

```
BE phải xong TASK-XXX trước khi FE/Mobile có thể làm TASK-YYY
FE và Mobile có thể làm song song sau khi BE done
```

---

## Human Review Gate ②

- [ ] API contracts đủ rõ để FE/BE/Mobile implement độc lập không cần hỏi nhau?
- [ ] DB migration có cả UP và DOWN?
- [ ] Security được address (auth, validation, sensitive data)?
- [ ] Cross-layer dependencies được map rõ?

**Reviewed by:** @[name] **Date:** YYYY-MM-DD **Status:** [ ] Approved

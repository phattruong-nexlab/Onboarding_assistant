# Skill: spec-init

## Trigger
Khi human nói "tạo feature mới", "bắt đầu feature X", hoặc gọi `/spec-init [feature-name]`

## Mục đích
Khởi tạo folder structure cho một feature mới theo chuẩn SDD.

## Các bước thực hiện

### 1. Validate input
- `[feature-name]` phải là kebab-case (VD: `oauth-google`, `user-profile`)
- Kiểm tra `specs/[feature-name]/` chưa tồn tại — nếu có, hỏi human có muốn overwrite không

### 2. Tạo folder structure
```bash
mkdir -p specs/[feature-name]
```

### 3. Copy templates
```bash
cp specs/settings/templates/requirements.md specs/[feature-name]/requirements.md
cp specs/settings/templates/design.md       specs/[feature-name]/design.md
cp specs/settings/templates/tasks.md        specs/[feature-name]/tasks.md
```

### 4. Fill in metadata
Trong mỗi file vừa copy, update phần metadata:
```yaml
feature: [feature-name]   # Tên feature vừa nhập
status: requirements      # Bắt đầu từ phase 1
created: [today date]
updated: [today date]
```

### 5. Update ALL_TASKS.md
Thêm feature vào section "📋 Đang spec":
```markdown
| [feature-name] | requirements | — | — | specs/[feature-name]/ |
```

### 6. Báo cáo
```
✅ Đã tạo: specs/[feature-name]/
   ├── requirements.md  ← Bước tiếp theo
   ├── design.md
   └── tasks.md

Bước tiếp theo: /spec-requirements [feature-name]
```

## Lưu ý
- KHÔNG bắt đầu viết requirements ngay — đó là skill khác (`spec-requirements`)
- KHÔNG hỏi thêm thông tin kỹ thuật ở bước này — đó là phase sau

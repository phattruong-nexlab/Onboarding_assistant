# Skill: validate-gap

## Trigger
`/validate-gap [feature-name]` — optional, chạy sau spec-design trước khi human review.

## Mục đích
So sánh requirements mới với code hiện có — phát hiện conflicts, gaps, assumptions sai.
Đặc biệt quan trọng với brownfield projects (thêm feature vào codebase đang chạy).

## Các bước thực hiện

### 1. Đọc spec mới
- `specs/[feature-name]/requirements.md`
- `specs/[feature-name]/design.md`

### 2. Scan code hiện tại
```bash
# Tìm code liên quan đến feature này
grep -r "[feature-keywords]" frontend/src/ backend/src/ --include="*.ts" --include="*.py"

# Check existing API routes
grep -r "router\|Route\|endpoint\|@app\." backend/src/

# Check existing DB schema
ls backend/migrations/ | sort
```

### 3. So sánh và báo cáo

**Format báo cáo:**
```markdown
## Validate Gap Report: [feature-name]
Generated: YYYY-MM-DD

### ✅ No Conflicts
- [Những thứ design đề xuất không conflict với existing code]

### ⚠️ Potential Conflicts
- **[File/Module]:** Design đề xuất X, nhưng existing code đang dùng Y
  → Cần quyết định: update existing hay tạo new?

### 🔍 Existing Code Reusable
- **[Module/Service]:** Có thể reuse thay vì viết mới
  → Tiết kiệm ước tính: [X hours]

### ❓ Assumptions Cần Verify
- [Assumption trong design có thể sai với thực tế code]
  → Cần human confirm trước khi implement
```

### 4. Không tự quyết — báo human
Nếu phát hiện conflict nghiêm trọng:
```
🚨 Phát hiện conflict quan trọng cần human quyết định trước khi tiếp tục.
Xem chi tiết trong báo cáo ở trên.
```

# Skill: create-skill

## Trigger
`/create-skill [skill-name]` hoặc "tôi muốn tạo skill mới cho workflow X"

## Mục đích
Giúp team tạo SKILL.md mới đúng format mà không cần viết tay.
Đây là meta-skill — skill để tạo skills.

## Các bước thực hiện

### 1. Thu thập thông tin từ human

```
Để tạo skill [skill-name], tôi cần biết:

1. Trigger: Khi nào skill này được gọi? (command / tự động / event)
2. Mục đích: Skill này giải quyết vấn đề gì?
3. Input: Cần đọc files/context nào trước?
4. Output: Tạo ra file gì / thay đổi gì?
5. Rules: Có gì KHÔNG được làm?
6. Ví dụ: Một use case cụ thể?
```

### 2. Generate SKILL.md

Tạo file `.claude/skills/[skill-name]/SKILL.md` với structure:

```markdown
# Skill: [skill-name]

## Trigger
[Khi nào kích hoạt]

## Mục đích
[Giải quyết vấn đề gì]

## Các bước thực hiện
[Step by step — cụ thể, actionable]

## Rules
[Những gì KHÔNG được làm]
```

### 3. Tạo folder và file

```bash
mkdir -p .claude/skills/[skill-name]
# Tạo SKILL.md với nội dung đã generate
```

### 4. Update getting-started/SKILL.md

Thêm skill mới vào bảng "Skills có sẵn":
```markdown
| `[skill-name]` | [Dùng khi nào — 1 câu] |
```

### 5. Báo cáo

```
✅ Đã tạo: .claude/skills/[skill-name]/SKILL.md
✅ Đã update: .claude/skills/getting-started/SKILL.md

Skill sẵn sàng dùng. Gọi bằng: /[skill-name]
```

## Rules
- KHÔNG tạo skill trùng với skill đã có (check getting-started/SKILL.md trước)
- Skill mới phải có Trigger rõ ràng — không phải "dùng khi cần"
- Mỗi skill làm đúng 1 việc — nếu skill quá phức tạp thì tách thành 2 skills

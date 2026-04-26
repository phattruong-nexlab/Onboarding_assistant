# Skill: doctor

## Trigger
`/doctor` — chạy sau `/init-from-specflow` hoặc `/init-project` để verify package đúng chuẩn.
Cũng dùng khi nghi ngờ cấu trúc bị hỏng, hoặc sau khi merge từ branch khác.

## Mục đích
Tự động kiểm tra toàn bộ SDD package structure — báo cáo thiếu gì, sai gì, còn placeholder chưa fill.
Thay thế cho việc human check tay từng file.

---

## Các bước thực hiện

### BƯỚC 1 — Check folder structure

```bash
echo "=== FOLDER STRUCTURE CHECK ==="
for dir in \
  steering specs docs logs process frontend backend \
  .claude/agents .claude/skills .claude/instincts .claude/rules; do
  [ -d "$dir" ] && echo "✅ $dir" || echo "❌ THIẾU: $dir"
done
```

### BƯỚC 1B — Check layers đã install

```bash
echo "=== LAYERS CHECK ==="
has_fe=false; has_be=false; has_mobile=false

[ -d "frontend" ] && { echo "✅ FE layer installed"; has_fe=true; } || echo "ℹ️  FE layer: không có"
[ -d "backend" ]  && { echo "✅ BE layer installed"; has_be=true; } || echo "ℹ️  BE layer: không có"
[ -d "mobile" ]   && { echo "✅ Mobile layer installed"; has_mobile=true; } || echo "ℹ️  Mobile layer: không có"

# Nếu không có layer nào → cảnh báo
$has_fe || $has_be || $has_mobile || echo "⚠️ Không có layer nào được install — chạy /install-layer [fe|be|mobile]"

# Check layer files có đủ không
$has_fe     && [ ! -f "frontend/CLAUDE.md" ]         && echo "❌ FE: frontend/CLAUDE.md thiếu"
$has_be     && [ ! -f "backend/CLAUDE.md" ]           && echo "❌ BE: backend/CLAUDE.md thiếu"
$has_mobile && [ ! -f "mobile/CLAUDE.md" ]            && echo "❌ Mobile: mobile/CLAUDE.md thiếu"
$has_mobile && [ ! -f "docs/SCREEN_FLOWS.md" ]        && echo "❌ Mobile: docs/SCREEN_FLOWS.md thiếu"

# Check mobile adapter
if $has_mobile; then
  echo "--- Mobile adapter check ---"
  [ -f ".claude/rules/flutter.md" ]         && echo "✅ Flutter adapter" ||   [ -f ".claude/rules/react-native.md" ]    && echo "✅ React Native adapter" ||   echo "⚠️  Mobile adapter chưa install — chạy /install-layer mobile"
fi
```

### BƯỚC 2 — Check files quan trọng tồn tại

```bash
echo "=== CORE FILES CHECK ==="
for file in \
  CLAUDE.md README.md AGENTS.md ALL_TASKS.md .env.example \
  steering/tech-stack.md steering/conventions.md \
  steering/api-standards.md steering/security.md \
  docs/ARCHITECTURE.md docs/API_CONTRACTS.md \
  docs/DECISIONS.md docs/TECH_DEBT.md docs/ENVIRONMENTS.md \
  logs/CONTEXT_SNAPSHOT.md logs/SESSION_LOG.md logs/TASK_LOG.md \
  logs/CHANGE_LOG.md logs/SPRINT_CONTRACT.md logs/EVALUATION_REPORT.md \
  process/WORKFLOW.md process/ONBOARDING.md \
  process/DEFINITION_OF_DONE.md process/REVIEW_CHECKLIST.md \
  process/DEPLOY_CHECKLIST.md \
  .claude/settings.json; do
  [ -f "$file" ] && echo "✅ $file" || echo "❌ THIẾU: $file"
done

# Check layer files — chỉ check nếu layer folder tồn tại
echo ""
echo "=== LAYER FILES CHECK ==="
[ -d "frontend" ] && {
  [ -f "frontend/CLAUDE.md" ] && echo "✅ frontend/CLAUDE.md" || echo "❌ frontend/CLAUDE.md"
  [ -f ".claude/agents/fe-generator.md" ] && echo "✅ fe-generator" || echo "❌ fe-generator"
  [ -f ".claude/rules/frontend.md" ] && echo "✅ rules/frontend.md" || echo "❌ rules/frontend.md"
} || echo "ℹ️  Frontend layer: không có (OK nếu project không cần)"

[ -d "backend" ] && {
  [ -f "backend/CLAUDE.md" ] && echo "✅ backend/CLAUDE.md" || echo "❌ backend/CLAUDE.md"
  [ -f ".claude/agents/be-generator.md" ] && echo "✅ be-generator" || echo "❌ be-generator"
  [ -f ".claude/rules/backend.md" ] && echo "✅ rules/backend.md" || echo "❌ rules/backend.md"
} || echo "ℹ️  Backend layer: không có (OK nếu project không cần)"

[ -d "mobile" ] && {
  [ -f "mobile/CLAUDE.md" ] && echo "✅ mobile/CLAUDE.md" || echo "❌ mobile/CLAUDE.md"
  [ -f ".claude/rules/non-expert-guard.md" ] && echo "✅ non-expert-guard" || echo "❌ non-expert-guard"
  [ -f ".claude/skills/explain-changes/SKILL.md" ] && echo "✅ explain-changes" || echo "❌ explain-changes"
  [ -f ".claude/skills/how-to-verify/SKILL.md" ] && echo "✅ how-to-verify" || echo "❌ how-to-verify"
  [ -f "docs/SCREEN_FLOWS.md" ] && echo "✅ SCREEN_FLOWS.md" || echo "❌ SCREEN_FLOWS.md"
  # Flutter-specific
  [ -f "steering/flutter-patterns.md" ] && echo "✅ flutter-patterns.md (Flutter)" || echo "ℹ️  flutter-patterns.md: không có (OK nếu không dùng Flutter)"
} || echo "ℹ️  Mobile layer: không có (OK nếu project không cần)"
```

### BƯỚC 3 — Check skills và agents

```bash
echo "=== SKILLS CHECK (expect 18+) ==="
skill_count=$(ls .claude/skills/ 2>/dev/null | wc -l)
echo "Skills found: $skill_count"
ls .claude/skills/ 2>/dev/null

echo ""
echo "=== AGENTS CHECK (expect 10) ==="
agent_count=$(ls .claude/agents/ 2>/dev/null | wc -l)
echo "Agents found: $agent_count"
ls .claude/agents/ 2>/dev/null
```

### BƯỚC 4 — Check folder rác (literal braces, spaces)

```bash
echo "=== GARBAGE FOLDER CHECK ==="
# Folder tên có literal braces
junk=$(find . -maxdepth 3 -name "*{*" -type d 2>/dev/null)
if [ -n "$junk" ]; then
  echo "❌ FOLDER RÁC PHÁT HIỆN:"
  echo "$junk"
  echo "→ Chạy: find . -maxdepth 3 -name '*{*' -type d -exec rm -rf {} +"
else
  echo "✅ Không có folder rác"
fi
```

### BƯỚC 5 — Check placeholder chưa fill

```bash
echo "=== PLACEHOLDER CHECK ==="
# Check trong files quan trọng (không check templates/)
placeholder_files=$(grep -rln "\[điền vào\]\|\[VD:\|\[CẦN ĐIỀN\]\|\[TODO\]\|\[feature-name\]\|\[member\]\|\[YYYY-MM-DD\]" \
  steering/ README.md CLAUDE.md .env.example \
  frontend/CLAUDE.md backend/CLAUDE.md \
  docs/ARCHITECTURE.md docs/ENVIRONMENTS.md \
  logs/CONTEXT_SNAPSHOT.md 2>/dev/null \
  | grep -v "templates/")

if [ -n "$placeholder_files" ]; then
  echo "⚠️ Còn placeholder chưa fill:"
  echo "$placeholder_files"
  echo ""
  echo "Chi tiết:"
  grep -rn "\[điền vào\]\|\[VD:\|\[CẦN ĐIỀN\]\|\[TODO\]\|\[feature-name\]\|\[member\]\|\[YYYY-MM-DD\]" \
    $placeholder_files 2>/dev/null | head -20
else
  echo "✅ Không còn placeholder trong files quan trọng"
fi
```

### BƯỚC 6 — Check CLAUDE.md length

```bash
echo "=== CLAUDE.md LENGTH CHECK (max 80 lines) ==="
lines=$(wc -l < CLAUDE.md)
if [ "$lines" -gt 80 ]; then
  echo "⚠️ CLAUDE.md có $lines dòng (vượt quá 80) — cần rút gọn"
else
  echo "✅ CLAUDE.md có $lines dòng (OK)"
fi
```

### BƯỚC 7 — Báo cáo tổng hợp

Sau khi chạy tất cả checks, output:

```
╔══════════════════════════════════════════════════════╗
║              SDD DOCTOR REPORT                       ║
╠══════════════════════════════════════════════════════╣
║ ✅ PASS  │ [X] checks                               ║
║ ❌ FAIL  │ [Y] checks — cần fix                     ║
║ ⚠️ WARN  │ [Z] items — nên xem lại                  ║
╚══════════════════════════════════════════════════════╝

❌ PHẢI FIX NGAY:
  [list các lỗi critical]

⚠️ NÊN XEM LẠI:
  [list warnings]

✅ OK:
  [list những gì đã đúng]
```

Nếu tất cả pass → "🎉 SDD package healthy — sẵn sàng làm việc!"

---

## Rules

- Chỉ đọc và check — KHÔNG tự sửa bất kỳ file nào
- Báo cáo đầy đủ tất cả vấn đề trong 1 lần chạy — không stop ở lỗi đầu tiên
- Với folder rác literal braces: đưa ra lệnh xóa để human chạy thủ công, không tự xóa

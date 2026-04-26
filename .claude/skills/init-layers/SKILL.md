# Skill: init-layers

## Trigger
`/init-layers` — chạy khi khởi tạo project mới (không từ SpecFlow)
hoặc khi thêm layer mới vào project đang có.

Cũng trigger khi `/init-from-specflow` hoàn thành Bước 1 và cần copy layers.

## Mục đích
Hỏi human cần layers nào, copy đúng files từ `layers/` vào project root.
Đây là bước setup one-time per layer — chạy lại khi thêm layer mới.

---

## BƯỚC 1 — Detect layers hiện có

```bash
# Kiểm tra layers đã có trong project
[ -d "frontend" ] && echo "FE: ✅" || echo "FE: ❌"
[ -d "backend" ]  && echo "BE: ✅" || echo "BE: ❌"
[ -d "mobile" ]   && echo "Mobile: ✅" || echo "Mobile: ❌"
```

---

## BƯỚC 2 — Hỏi human

```
Project này cần những layers nào?

Layers hiện có: [list từ Bước 1, hoặc "Chưa có layer nào"]

Chọn layers cần thêm:
  [1] Frontend  (Next.js / Vue / React / ...)
  [2] Backend   (FastAPI / NestJS / Laravel / ...)
  [3] Mobile    (Flutter / React Native / Native iOS / ...)

Gõ số, VD: "1,2" hoặc "1,2,3" hoặc "3"
```

Nếu chọn [3] Mobile → hỏi thêm:
```
Mobile tech stack là gì?
  [A] Flutter
  [B] React Native
  [C] Native iOS (Swift/Objective-C)
  [D] Native Android (Kotlin/Java)
  [E] Khác: ___

Đây là project:
  [G] Greenfield (app mới, chưa có code)
  [B] Brownfield (app đang production, đã có code)
```

---

## BƯỚC 3 — Copy layer files vào project

### Nếu chọn Frontend:
```bash
# Tạo folder
mkdir -p frontend

# Copy từ layers/frontend/
cp layers/frontend/frontend/CLAUDE.md frontend/CLAUDE.md

# Copy rules
cp layers/frontend/.claude/rules/frontend.md .claude/rules/frontend.md

# Copy agents
cp layers/frontend/.claude/agents/fe-generator.md .claude/agents/fe-generator.md
cp layers/frontend/.claude/agents/fe-evaluator.md .claude/agents/fe-evaluator.md
```

### Nếu chọn Backend:
```bash
mkdir -p backend
cp layers/backend/backend/CLAUDE.md backend/CLAUDE.md
cp layers/backend/.claude/rules/backend.md .claude/rules/backend.md
cp layers/backend/.claude/agents/be-generator.md .claude/agents/be-generator.md
cp layers/backend/.claude/agents/be-evaluator.md .claude/agents/be-evaluator.md
```

### Nếu chọn Mobile:
```bash
mkdir -p mobile

# Core mobile (mọi stack)
cp layers/mobile/core/mobile/CLAUDE.md mobile/CLAUDE.md
cp layers/mobile/core/docs/SCREEN_FLOWS.md docs/SCREEN_FLOWS.md
cp layers/mobile/core/process/RELEASE_CHECKLIST.md process/RELEASE_CHECKLIST.md
cp layers/mobile/core/process/NON-EXPERT-DEV-WORKFLOW.md process/NON-EXPERT-DEV-WORKFLOW.md
cp layers/mobile/core/.claude/rules/non-expert-guard.md .claude/rules/non-expert-guard.md
cp layers/mobile/core/.claude/skills/explain-changes/SKILL.md .claude/skills/explain-changes/SKILL.md
cp layers/mobile/core/.claude/skills/how-to-verify/SKILL.md .claude/skills/how-to-verify/SKILL.md

# Brownfield-only (nếu chọn [B])
if brownfield:
  cp layers/mobile/core/process/BROWNFIELD-ONBOARDING.md process/BROWNFIELD-ONBOARDING.md
  cp layers/mobile/core/.claude/skills/debug-mobile/SKILL.md .claude/skills/debug-mobile/SKILL.md

# Adapter theo tech stack
if flutter:
  cp layers/mobile/adapters/flutter/steering/flutter-patterns.md steering/flutter-patterns.md
  cp layers/mobile/adapters/flutter/docs/GRAPHQL_CONTRACTS.md docs/GRAPHQL_CONTRACTS.md
  cp layers/mobile/adapters/flutter/.claude/rules/flutter.md .claude/rules/flutter.md
  cp layers/mobile/adapters/flutter/.claude/rules/graphql.md .claude/rules/graphql.md
  cp layers/mobile/adapters/flutter/.claude/agents/flutter-generator.md .claude/agents/flutter-generator.md
  cp layers/mobile/adapters/flutter/.claude/agents/graphql-checker.md .claude/agents/graphql-checker.md
  cp layers/mobile/adapters/flutter/.claude/agents/flutter-evaluator.md .claude/agents/flutter-evaluator.md
  cp -r layers/mobile/adapters/flutter/.claude/skills/brownfield-audit .claude/skills/
  cp -r layers/mobile/adapters/flutter/.claude/skills/setup-environment .claude/skills/
  cp -r layers/mobile/adapters/flutter/.claude/skills/discover-graphql .claude/skills/
  cp layers/mobile/adapters/flutter/.claude/instincts/always-check-graphql.md .claude/instincts/
```

> ⚠️ KHÔNG dùng brace expansion `{a,b,c}` — dùng từng lệnh `cp` riêng biệt.

---

## BƯỚC 4 — Update CLAUDE.md root

Thêm layer mới vào section "Pointers":
```markdown
| Rules cho [Layer] | `[layer]/CLAUDE.md` + `.claude/rules/[layer].md` |
```

Thêm hard rule nếu Mobile:
```markdown
- **KHÔNG ship mobile** khi chưa có human verify trên app thật
```

---

## BƯỚC 5 — Update AGENTS.md

Thêm agents của layer mới vào Agent Registry.

---

## BƯỚC 6 — Update getting-started/SKILL.md

Thêm agents và skills mới vào bảng index.

---

## BƯỚC 7 — Update docs/API_CONTRACTS.md (nếu thêm Mobile)

Nếu Mobile dùng GraphQL → thêm note:
```markdown
> Mobile (Flutter/RN) dùng GraphQL — xem docs/GRAPHQL_CONTRACTS.md
> Web FE và BE dùng REST — xem bên dưới
```

---

## BƯỚC 8 — Báo cáo

```
✅ Layer [tên] đã được thêm vào project!

Files đã copy:
  [list files]

⚠️ Cần điền thêm:
  - [layer]/CLAUDE.md → điền tech stack thật
  - steering/[layer]-patterns.md → điền patterns thật (nếu có)
  [list tùy theo layer]

Bước tiếp theo:
  → /doctor để verify cấu trúc đúng
  [Nếu Mobile Brownfield]: → /setup-environment để chạy app local trước
  [Nếu Greenfield]: → /spec-init [feature] để bắt đầu feature đầu tiên
```

---

## Rules

- KHÔNG overwrite file đã có nội dung thật — hỏi human trước
- Nếu layer đã tồn tại → báo "Layer [X] đã có, bỏ qua" thay vì overwrite
- Chạy `/doctor` sau khi copy xong để verify không thiếu file

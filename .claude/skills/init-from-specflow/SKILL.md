# Skill: init-from-specflow

## Trigger
`/init-from-specflow` — chạy ngay sau khi SpecFlow export folder vào project.
Hoặc khi human nói "setup SDD package", "transform SpecFlow output", "init project structure".

## Mục đích
Đọc **toàn bộ** folder do SpecFlow generate và tự động transform thành SDD Architecture đầy đủ.
Đây là bridge duy nhất giữa SpecFlow tool và SDD Package chuẩn của team.

---

## Pre-condition

Kiểm tra trước khi chạy:
```bash
# Verify đây là SpecFlow output — phải có ít nhất CLAUDE.md
ls -la | grep -E "CLAUDE\.md|README\.md"
```

Nếu không tìm thấy `CLAUDE.md` → báo human: "Không tìm thấy SpecFlow output. Chạy SpecFlow export trước."

---

## PRE-STEP — Chọn layers cho project

Trước khi đọc SpecFlow output, xác định project có những layers nào:

```
Project này có những layers nào?

[1] FE — Web Frontend (Next.js / Vue / React / ...)
[2] BE — Backend API (FastAPI / NestJS / Express / ...)
[3] Mobile — Mobile App (Flutter / React Native / ...)

→ Chọn một hoặc nhiều, VD: "1,2" hoặc "1,2,3" hoặc "2,3"
```

**Chờ human trả lời.** Ghi nhận layers được chọn — sẽ dùng trong Bước 3 để install đúng layers.

Nếu human không chắc → gợi ý: "Nhìn vào SpecFlow output, tôi thấy có đề cập đến [web/mobile/api]... → có vẻ project có layers: [X]"

---

## BƯỚC 0 — Inventory toàn bộ SpecFlow output

**Quét hết tất cả file trong folder hiện tại trước khi làm bất cứ gì:**

```bash
# Liệt kê toàn bộ cấu trúc, không bỏ sót
find . \( -path "./.git" -o -path "./node_modules" \) -prune \
  -o -type f -print | sort

# Liệt kê riêng thư mục docs/specs nếu có
find . -path "*/docs/specs*" -type f | sort
find . -path "*/docs/specs*" -type d | sort
```

**Đọc TẤT CẢ file tìm được theo thứ tự ưu tiên:**

| Thứ tự | File | Dữ liệu khai thác |
|--------|------|-------------------|
| 1 | `CLAUDE.md` | Tech stack, hard rules, coding standards, build commands |
| 2 | `README.md` | Tên project, mô tả bài toán, mục tiêu |
| 3 | `docs/specs/PRD.md` hoặc `PRD.md` | User personas, functional requirements, wireframes, success metrics, cold-start plan, fallback strategy |
| 4 | `docs/specs/architecture.md` hoặc `ARCHITECTURE.md` | C4 diagram, DB schema (ERD), API endpoints, folder structure, deployment |
| 5 | `docs/specs/tasks/ALL_TASKS.md` hoặc `ALL_TASKS.md` | Task list đầy đủ với ID, complexity, AC, dependencies |
| 6 | `docs/specs/tasks/*.md` | Task breakdown chi tiết từng file riêng |
| 7 | `.claude/commands/*.md` hoặc `skills/*.md` | Slash commands hiện có |
| 8 | **Bất kỳ `.md` nào còn lại (file lạ)** | Đọc hết — **xử lý bắt buộc ở Bước 1D** |

> ⚠️ **KHÔNG bỏ qua file nào.** Mỗi file có thể chứa thông tin bổ sung không có ở file khác.

**Báo cáo inventory:**
```
📖 Đã quét SpecFlow output:
- Files tìm thấy: [liệt kê tên và path đầy đủ]

- Files đã biết (known):
    CLAUDE.md, README.md, PRD.md, architecture.md,
    ALL_TASKS.md, tasks/*.md, commands/*.md, skills/*.md

- Files lạ (unknown — cần phân loại ở Bước 1A):
    [liệt kê các file không thuộc danh sách trên]

- Files KHÔNG đọc được: [nếu có, lý do]
```

---

## BƯỚC 1 — Phân tích và cross-reference

### 1A. Trích xuất dữ liệu từ từng nguồn

**Từ CLAUDE.md:**
- Tech stack: FE framework + version, BE framework, database, deploy platform
- Hard rules
- Build commands
- Coding standards

**Từ README.md:**
- Tên project (kebab-case cho folder, Title Case cho display)
- Mô tả ngắn: project giải quyết vấn đề gì
- Target users (nếu có)

**Từ PRD.md (nếu có):**
- User personas (vai trò, nhu cầu, pain points)
- Feature list đầy đủ với mô tả chi tiết
- Scope & Constraints (budget, timeline, platform)
- Auth mechanism (Email/Password, OAuth, SSO...)
- AI/LLM provider và cấu hình
- Fallback strategy (nếu có)
- Non-functional requirements (performance, security, UX)
- Success metrics
- Launch checklist
- Cold-start plan (nếu có)
- Env vars được nhắc đến

**Từ architecture.md (nếu có):**
- System diagram (C4, ASCII, Mermaid)
- Component breakdown và trách nhiệm từng thành phần
- DB schema / ERD đầy đủ
- API endpoints list
- Sequence diagrams (RAG flow, auth flow...)
- Folder structure đề xuất
- Deployment architecture
- Security architecture

**Từ ALL_TASKS.md + tasks/*.md:**
- Số lượng task
- Task IDs, tên, complexity (S/M/L), priority (P0/P1/P2), story points
- Acceptance criteria từng task
- Dependency graph giữa tasks
- Phân chia FE / BE

**Từ .claude/commands/*.md hoặc skills/*.md:**
- Danh sách slash commands hiện có
- Logic từng command → sẽ merge/upgrade sang skills mới

### 1B. Cross-reference consistency check

**BẮT BUỘC** — Kiểm tra mâu thuẫn giữa **tất cả** nguồn đã đọc (bao gồm cả file lạ):

```
Tiêu chí cứng (luôn check):
□ Auth mechanism       → nhất quán qua tất cả files?
□ LLM/AI provider      → cùng 1 provider + model qua tất cả files?
□ Framework version    → cùng version qua tất cả files?
□ Database             → cùng DB + extensions qua tất cả files?
□ Deploy platform      → cùng platform qua tất cả files?
□ Feature list         → task list có cover đủ features trong PRD/requirements?

Tiêu chí động (từ file lạ — thêm vào nếu phát hiện):
□ [Bất kỳ giá trị nào xuất hiện > 1 lần với giá trị khác nhau giữa các files]
```

**Nếu phát hiện conflict → DỪNG và báo human:**

```
⚠️ PHÁT HIỆN CONFLICT — Cần human quyết định trước khi tiếp tục:

┌─────────────────┬──────────────────────────┬──────────────────────────┐
│ Chủ đề          │ Nguồn A (file: ...)      │ Nguồn B (file: ...)      │
├─────────────────┼──────────────────────────┼──────────────────────────┤
│ [chủ đề]        │ [giá trị A]              │ [giá trị B]              │
│ [chủ đề 2]      │ [giá trị A2]             │ [giá trị B2]             │
└─────────────────┴──────────────────────────┴──────────────────────────┘

→ Dùng giá trị nào? (Gõ số thứ tự hoặc nhập giá trị mới)
```

Chờ human xác nhận từng conflict rồi mới tiếp tục.

### 1C. Nhóm tasks thành features

Từ task list đã đọc, nhóm các task liên quan thành features:

**Heuristic nhóm (áp dụng theo thứ tự):**
1. Nếu tasks đã được gắn nhãn feature rõ (e.g., `[Auth]`, `[Search]`) → dùng nhãn đó
2. Nếu tasks có dependency chain chặt chẽ (A → B → C) → gom thành 1 feature
3. Nếu tasks mô tả cùng 1 domain (user, article, search...) → gom thành 1 feature
4. Nếu vẫn không rõ → liệt kê nhóm đề xuất, hỏi human confirm

**Báo cáo kết quả phân tích:**
```
📊 Kết quả phân tích SpecFlow output:

Project:    [Tên]
Tech stack: FE=[framework + version] | BE=[framework] | DB=[database] | AI=[provider]
Auth:       [cơ chế xác thực — đã confirm]
Tasks:      [X] tasks → nhóm thành [Y] features:
  - [feature-1]: TASK-001, TASK-002, TASK-003
  - [feature-2]: TASK-004, TASK-005
  - ...
Slash commands cũ: [list]

Files lạ đã xử lý:
  - [tên file] → merged vào [target SDD file]
  - (nếu không có file lạ → "Không có")

Conflicts: [đã xử lý X conflicts / không có]

Tiếp tục transform? [yes/no]
```

### 1D. Xử lý file lạ (BƯỚC BẮT BUỘC — không skip dù không có file lạ)

**Lấy danh sách "Files lạ" từ báo cáo Bước 0.**

Nếu danh sách rỗng → ghi `"Không có file lạ"` vào báo cáo rồi chuyển sang Bước 2.

Nếu có file lạ → **hỏi human từng file, không tự quyết**. Thực hiện theo trình tự:

---

**Với từng file lạ:**

**1. Đọc toàn bộ nội dung file**

**2. Tóm tắt nội dung** — 2-3 dòng, ngắn gọn, không dùng jargon

**3. Hỏi human theo format sau:**

```
📎 File lạ: [tên file]

Nội dung tóm tắt:
  [2-3 dòng mô tả file này đang nói về gì]

Tôi đề xuất map vào: [SDD target — dựa trên bảng gợi ý bên dưới]
Lý do: [1 câu giải thích]

→ Bạn quyết định:
  [1] Đồng ý — merge vào [SDD target đề xuất]
  [2] Map vào chỗ khác: ___
  [3] Bỏ qua file này
```

**Chờ human trả lời trước khi xử lý file tiếp theo.**

---

**Bảng gợi ý để Claude đề xuất** (không tự map — chỉ dùng để đưa ra đề xuất cho human):

| Nội dung nhận ra trong file | Đề xuất SDD target |
|---|---|
| Sprint plan, timeline, milestone | `logs/CONTEXT_SNAPSHOT.md` + `ALL_TASKS.md` |
| User stories, personas, use cases | `specs/[feature]/requirements.md` |
| Technical spec, system design | `docs/ARCHITECTURE.md` + `specs/[feature]/design.md` |
| Data model, DB schema, ERD | `docs/ARCHITECTURE.md` phần Database + `specs/[feature]/design.md` |
| API spec, endpoint list, OpenAPI | `docs/API_CONTRACTS.md` |
| Security policy, auth design | `steering/security.md` + `specs/[feature]/design.md` |
| ADR, technical decision log | `docs/DECISIONS.md` |
| Coding conventions, style guide | `steering/conventions.md` |
| Environment config, deployment notes | `docs/ENVIRONMENTS.md` + `steering/tech-stack.md` |
| Risk list, known issues, tech debt | `docs/TECH_DEBT.md` |
| Test plan, QA scenarios, test cases | `specs/[feature]/tasks.md` (acceptance criteria) |
| Không nhận ra loại nào | Đề xuất: `docs/DECISIONS.md` mục `## Imported from SpecFlow` |

---

**Sau khi human quyết định:**

**Nếu [1] hoặc [2] — merge:**
- Merge nội dung vào target file human chọn
- Thêm dòng này ở đầu section vừa merge:
  ```
  > Imported from: [tên file lạ] — [ngày migrate]
  ```
- Kiểm tra conflict với nội dung đã đọc từ known files → nếu có mâu thuẫn → thêm vào danh sách conflict Bước 1B

**Nếu [3] — bỏ qua:**
- KHÔNG merge, KHÔNG xóa file gốc
- Ghi vào `docs/DECISIONS.md` theo format:

```markdown
## Imported from SpecFlow — Đã bỏ qua

### [tên file]
**Ngày:** [hôm nay]
**Quyết định:** Human chọn bỏ qua khi chạy /init-from-specflow
**Nội dung tóm tắt:** [2-3 dòng summary]
**Xem lại nếu cần:** File gốc vẫn còn tại [path gốc trong SpecFlow output]
```

> Ghi vào DECISIONS.md để không mất dấu — agent khác đọc DECISIONS.md vẫn biết file này tồn tại.

---

**Báo cáo Bước 1D** (sau khi xử lý xong tất cả file lạ):

```
📎 Kết quả xử lý file lạ:
  - [tên file] → merged vào [target] | human chọn: [1/2]
  - [tên file] → bỏ qua | ghi vào DECISIONS.md
  (hoặc "Không có file lạ")
```

> ⚠️ **Không bỏ qua bước này dù danh sách rỗng.** Phải có báo cáo rõ để human biết skill đã xử lý tất cả.

---

### 1E. Chọn layers cho project

Sau khi Bước 1D xong, hỏi human về layers:

```
Project này cần những layers nào?
(Dựa trên tech stack đã đọc, tôi đề xuất: [layers detect được từ CLAUDE.md])

  [1] Frontend  — [FE framework đã detect, hoặc "chưa detect được"]
  [2] Backend   — [BE framework đã detect, hoặc "chưa detect được"]
  [3] Mobile    — [nếu detect được mobile tech, hoặc "chưa detect được"]

Gõ số layers cần có, VD: "1,2" hoặc "1,2,3"
(Enter để dùng đề xuất của tôi)
```

Nếu human chọn Mobile → hỏi thêm:
```
Mobile tech stack là gì?
  [A] Flutter
  [B] React Native
  [C] Native iOS (Swift)
  [D] Native Android (Kotlin)
  [E] Khác: ___

Đây là project:
  [G] Greenfield (app mới, chưa có code)
  [B] Brownfield (app đang production)
```

Ghi nhớ kết quả layer selection — dùng ở Bước 3 khi chạy `/init-layers`.

---

## BƯỚC 2 — Tạo folder structure

```bash
mkdir -p steering
mkdir -p specs/settings/templates
mkdir -p docs
mkdir -p logs
mkdir -p process
mkdir -p frontend
mkdir -p backend
mkdir -p .claude/agents
mkdir -p .claude/skills/getting-started
mkdir -p .claude/skills/init-project
mkdir -p .claude/skills/init-from-specflow
mkdir -p .claude/skills/spec-init
mkdir -p .claude/skills/spec-requirements
mkdir -p .claude/skills/spec-design
mkdir -p .claude/skills/validate-gap
mkdir -p .claude/skills/validate-design
mkdir -p .claude/skills/spec-tasks
mkdir -p .claude/skills/spec-impl
mkdir -p .claude/skills/spec-check
mkdir -p .claude/skills/finish-task
mkdir -p .claude/skills/quality-gate
mkdir -p .claude/skills/research
mkdir -p .claude/skills/log-session
mkdir -p .claude/skills/run-evaluation
mkdir -p .claude/skills/run-harness
mkdir -p .claude/skills/create-skill
mkdir -p .claude/instincts
mkdir -p .claude/rules
```

> ⚠️ Dùng từng lệnh `mkdir -p` riêng biệt — **KHÔNG** dùng brace expansion `{a,b,c}` vì sẽ tạo ra folder tên literal.

---

## BƯỚC 3 — Fill content từ dữ liệu đã phân tích

### 3-ZERO. Install layers đã chọn ở PRE-STEP

Gọi skill `/install-layer` cho từng layer được chọn:

```
# Với mỗi layer trong danh sách đã chọn:
/install-layer fe      # nếu có FE
/install-layer be      # nếu có BE
/install-layer mobile  # nếu có Mobile
```

> install-layer sẽ hỏi thêm về tech stack từng layer.
> Dùng thông tin đã đọc từ SpecFlow output (CLAUDE.md, architecture.md) để trả lời.
> Sau khi install xong tất cả layers → tiếp tục 3A.

---

### 3A. Rewrite CLAUDE.md (≤ 80 dòng)

Cấu trúc cố định:
- Section "Hard Rules": lấy từ CLAUDE.md cũ + bổ sung conflict-resolved values
- Section "Pointers": trỏ đến steering/, specs/, docs/, logs/, process/
- Section "Agent & Skill Index": pointer đến AGENTS.md
- Section "Instincts": 3 instincts chuẩn

**KHÔNG** giữ: tech stack chi tiết, coding standards, security rules → chuyển sang steering/

### 3B. Rewrite README.md

Fill đầy đủ từ dữ liệu đã đọc:
```markdown
# [Tên project thật — từ README.md cũ]

## Vấn đề
[Mô tả bài toán — từ README.md cũ + PRD mục Problem Statement]

## Giải pháp
[Vision — từ PRD mục Solution & Vision]

## Bắt đầu nhanh
[Build commands thật — từ CLAUDE.md cũ, không để placeholder]

## Tech Stack
[Table với giá trị thật — từ CLAUDE.md cũ + architecture.md]

## Tài liệu
[Links đến docs/ và specs/]

## Team
[Nếu có trong PRD/README cũ]
```

### 3C. Generate steering/ (4 files)

**`steering/tech-stack.md`** — Fill đầy đủ, không để `[VD: ...]`:
```markdown
## Frontend
Framework:     [Giá trị thật — VD: Next.js 14+]
Styling:       [Giá trị thật]
State:         [Giá trị thật hoặc "None (Server Components)"]
Auth client:   [Giá trị thật]
HTTP client:   [Giá trị thật]
Testing:       [Giá trị thật]
Linting:       [Giá trị thật]
Package mgr:   [Giá trị thật]

## Backend
Framework:     [Giá trị thật]
Language:      [Giá trị thật + version]
ORM/Query:     [Giá trị thật]
Auth:          [Giá trị thật]
AI/LLM:        [Giá trị thật — provider + model]
Testing:       [Giá trị thật]

## Database
Primary:       [Giá trị thật]
Extensions:    [VD: pgvector]
Migrations:    [Giá trị thật hoặc "manual SQL"]

## Infrastructure
Deploy FE:     [Giá trị thật]
Deploy BE:     [Giá trị thật]
CI/CD:         [Giá trị thật hoặc "Chưa có"]

## Build Commands
# Frontend
[lệnh dev thật]
[lệnh build thật]
[lệnh test thật]
[lệnh lint thật]

# Backend
[lệnh dev thật]
[lệnh test thật]
```

**`steering/conventions.md`** — Fill từ Coding Style trong CLAUDE.md cũ + template defaults.

**`steering/api-standards.md`** — Dùng template chuẩn (tech-agnostic).

**`steering/security.md`** — Merge security rules từ CLAUDE.md cũ + template chuẩn.

### 3D. Transform ALL_TASKS.md → Dashboard

Rewrite `ALL_TASKS.md` thành dashboard format — điền dữ liệu thật từ task list:

```markdown
## 🔄 Đang làm (In Progress)
[Để trống nếu chưa bắt đầu]

## ⏳ Chờ implement (Approved)
[Liệt kê features đã có tasks approved]

## 📋 Đang spec (In Spec)
[Liệt kê features đang trong quá trình spec]

## 📊 Sprint Summary
Sprint: Sprint 1 (MVP)
Period: [Ngày bắt đầu] → [Ngày bắt đầu + 2 tuần]
Goal: [Mục tiêu sprint — từ PRD timeline]
Total features: [X]
```

### 3E. Generate specs/ từ task groups

Với mỗi feature group đã xác định ở Bước 1C:

```bash
mkdir -p specs/[feature-name]
```

**`specs/[feature-name]/tasks.md`** — Migrate tasks từ ALL_TASKS.md cũ:
- Copy đầy đủ TASK-XXX, acceptance criteria, complexity, priority
- Thêm frontmatter: `scope`, `depends-on`, `estimate`
- Đánh dấu rõ status: `pending` (chưa làm)

**`specs/[feature-name]/requirements.md`** — Điền từ PRD:
- User story từ PRD feature description
- Acceptance criteria theo EARS format (từ task ACs)
- Out of scope (từ PRD Scope & Constraints)
- Non-functional (từ PRD NFRs)
- Để trống section nào PRD không cover, ghi `[CẦN ĐIỀN]`

**`specs/[feature-name]/design.md`** — Điền từ architecture.md:
- API endpoints liên quan đến feature này (từ architecture.md API list)
- DB schema liên quan (từ architecture.md ERD)
- Sequence diagram nếu có trong architecture.md
- Security considerations (auth, RLS...)
- Để trống section nào chưa có, ghi `[CẦN ĐIỀN]`

### 3F. Generate .env.example

Collect tất cả env vars đã tìm thấy trong PRD, CLAUDE.md, architecture.md:

```bash
# Ví dụ với NexWiki:
# Database
SUPABASE_URL=
SUPABASE_ANON_KEY=
SUPABASE_SERVICE_KEY=
DATABASE_URL=

# Auth
JWT_SECRET=

# AI
CLAUDE_API_KEY=
CLAUDE_API_TIMEOUT=10
CLAUDE_MAX_RETRIES=2
CLAUDE_RATE_LIMIT_COOLDOWN=3600

# App
APP_ENV=development
PORT=8000
CORS_ORIGINS=http://localhost:3000

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=
```

Chỉ liệt kê env vars đã xuất hiện trong SpecFlow output — không tự thêm.

### 3G. Generate docs/ (skeleton có nội dung thật)

**`docs/ARCHITECTURE.md`** — Fill từ architecture.md cũ:
- Copy system diagram (ASCII/Mermaid) đã có
- Copy DB schema đã có
- Copy component breakdown
- Copy deployment architecture
- Đánh dấu sections cần human review với `> ⚠️ Cần verify`

**`docs/API_CONTRACTS.md`** — Fill skeleton từ architecture.md:
- Liệt kê tất cả endpoints đã phát hiện trong architecture.md
- Để request/response schema trống với `[TODO: fill schema]`

**`docs/DECISIONS.md`** — Tạo ADR từ conflicts đã resolve:
```markdown
## ADR-001: [Tên quyết định]
Date: [hôm nay]
Status: Accepted
Deciders: [Human + Claude]

Context: [Mô tả conflict đã gặp]
Decision: [Giá trị đã chọn]
Reason: [Lý do human chọn]
```

**`docs/TECH_DEBT.md`** — Liệt kê những gì biết là làm tạm từ PRD:
- Nếu PRD có note "Post-MVP" items → ghi vào đây như tech debt

**`docs/ENVIRONMENTS.md`** — Fill từ architecture.md deployment + PRD:
- Hosting URLs (Vercel, Render, Supabase...)
- Local dev URLs (từ CLAUDE.md build commands)

### 3H. Generate logs/ (khởi tạo)

**`logs/CONTEXT_SNAPSHOT.md`** — Fill với thông tin thực:
```markdown
## Section A — Human View
Cập nhật: [hôm nay] bởi /init-from-specflow

### Sprint hiện tại
Sprint: Sprint 1 (MVP)
Mục tiêu: [Từ PRD timeline/goal]
Deadline: [Từ PRD — VD: 2 tuần từ hôm nay]

### Trạng thái
Project vừa được init từ SpecFlow output.
Tất cả [X] features đang ở phase: specs chưa approved.
Bước tiếp theo: Human review specs/ → approve → /spec-impl

### Features cần làm
[List từ task groups — không để trống]
```

`logs/SESSION_LOG.md`, `TASK_LOG.md`, `CHANGE_LOG.md` — empty với format header.
`logs/SPRINT_CONTRACT.md`, `EVALUATION_REPORT.md` — empty với format header.

### 3I. Migrate skills cũ → .claude/skills/

Map từ SpecFlow command format sang SDD Skill format:

| SpecFlow command | SDD Skill |
|---|---|
| `implement-task.md` | `.claude/skills/spec-impl/SKILL.md` (merge + upgrade) |
| `finish-task.md` | `.claude/skills/finish-task/SKILL.md` (merge + upgrade) |
| `research.md` | `.claude/skills/research/SKILL.md` (merge + upgrade) |
| `spec-check.md` | `.claude/skills/spec-check/SKILL.md` (merge + upgrade) |
| Bất kỳ command nào khác | Tạo skill mới tương ứng |

**Upgrade rule:** Giữ nguyên logic cũ + thêm `## Context` pointer đến file locations mới trong SDD structure.

### 3J. Copy skills mới từ SDD Package template

Copy tất cả skills chưa có (từ SDD package đi kèm):
`getting-started`, `init-project`, `spec-init`, `spec-requirements`, `spec-design`,
`validate-gap`, `validate-design`, `spec-tasks`, `quality-gate`, `log-session`,
`run-evaluation`, `run-harness`, `create-skill`

### 3K. Copy agents, instincts, rules, settings

Copy tất cả từ SDD Package template:
- `.claude/agents/` — 10 agents
- `.claude/instincts/` — 3 instincts
- `.claude/rules/` — 5 rules
- `.claude/settings.json` — hooks config

### 3L. Copy layers theo kết quả Bước 1E

Chạy `/init-layers` với layer selection đã ghi nhận ở Bước 1E.

`/init-layers` sẽ tự động:
- Copy đúng layer files (frontend/, backend/, mobile/) vào project
- Copy agents, rules, skills của từng layer
- Fill tech stack từ data đã đọc ở Bước 1A

Sau khi `/init-layers` xong → fill nội dung thật vào các CLAUDE.md của layer:

**`frontend/CLAUDE.md`** (nếu có FE layer):
```markdown
## Tech Stack (FE)
Framework: [giá trị thật từ Bước 1A]
Styling: [giá trị thật]
State: [giá trị thật]
Test: [giá trị thật]

## Build Commands
[lệnh thật từ CLAUDE.md cũ]

## FE-specific Rules
[Rules từ Coding Style phần FE trong CLAUDE.md cũ]
```

**`backend/CLAUDE.md`** (nếu có BE layer): Tương tự cho BE.

**`mobile/CLAUDE.md`** (nếu có Mobile layer): Fill tech stack detect được.

### 3M. Copy process/ và templates

Copy 5 process files + 3 template files (đã update cho multi-layer) từ SDD Package.

### 3N. Generate AGENTS.md

Generate AGENTS.md dựa trên layers đã chọn — chỉ list agents thực sự có trong project.

---

## BƯỚC 4 — Cleanup SpecFlow artifacts cũ

```bash
# Kiểm tra xem có folder/file cũ cần xóa không
ls -la docs/specs/ 2>/dev/null
ls -la .claude/commands/ 2>/dev/null
ls -la skills/ 2>/dev/null
```

Hỏi human trước khi xóa bất kỳ thứ gì:
```
Các artifacts SpecFlow cũ sau đã được migrate, muốn xóa không?
  - docs/specs/tasks/ALL_TASKS.md (đã migrate vào specs/[feature]/tasks.md)
  - .claude/commands/ (đã migrate vào .claude/skills/)
  - [list thêm nếu có]

[yes/no] (mặc định: no — giữ lại để review)
```

Nếu có folder tên lạ (literal braces, spaces, special chars) → xóa ngay không cần hỏi:
```bash
# Xóa folder rác nếu có
find . -maxdepth 2 -name "*{*" -type d -exec rm -rf {} + 2>/dev/null
find . -maxdepth 2 -name "* *" -type d 2>/dev/null  # kiểm tra có folder tên có space không
```

---

## BƯỚC 5 — Verification

Tự kiểm tra trước khi báo cáo xong:

```bash
# Check không còn placeholder [điền vào] hay [VD: ...] trong files quan trọng
grep -rn "\[điền vào\]\|\[VD:\|\[CẦN ĐIỀN\]" \
  steering/ README.md CLAUDE.md .env.example 2>/dev/null \
  | grep -v "templates/"  # templates được phép có placeholder

# Check không còn folder rác
find . -maxdepth 3 -name "*{*" -type d 2>/dev/null

# Check tất cả folders quan trọng tồn tại
for dir in steering specs docs logs process frontend backend \
  .claude/agents .claude/skills .claude/instincts .claude/rules; do
  [ -d "$dir" ] && echo "✅ $dir" || echo "❌ THIẾU: $dir"
done

# Đếm số skills
ls .claude/skills/ | wc -l
```

---

## BƯỚC 6 — Báo cáo và next steps

```
✅ Transform hoàn thành!

📁 Đã tạo:
  - steering/                (4 files — điền từ SpecFlow data)
  - specs/                   ([X] feature folders)
    [liệt kê từng feature]
  - docs/                    (5 files — skeleton có nội dung thật)
  - logs/                    (6 files — khởi tạo)
  - process/                 (5 files)
  - .claude/agents/          (10 agents)
  - .claude/skills/          ([X] skills)
  - .claude/instincts/       (3 instincts)
  - .claude/rules/           (5 rules)
  - .claude/settings.json

📋 ADRs đã ghi nhận:
  [Liệt kê các quyết định đã resolve từ conflicts]

⚠️ Cần human verify (không có placeholder nhưng cần xác nhận):
  1. steering/tech-stack.md  → verify build commands chạy được chưa
  2. docs/ARCHITECTURE.md    → verify diagram còn đúng không
  3. specs/*/requirements.md → verify acceptance criteria đủ chưa
  4. docs/API_CONTRACTS.md   → điền request/response schemas
  5. .env.example            → thêm env vars còn thiếu (nếu có)

🚀 Bước tiếp theo:
  Option A — Implement ngay (nếu specs từ SpecFlow đã đủ):
    Chạy: /spec-impl [feature-name] cho feature P0 đầu tiên

  Option B — Review spec trước (khuyên dùng):
    1. Đọc specs/[feature]/requirements.md — confirm đúng intent
    2. Đọc specs/[feature]/design.md — confirm đúng architecture
    3. Approve → /spec-impl [feature-name]

  Option C — Thêm feature mới chưa có trong SpecFlow:
    Chạy: /spec-init [feature-name]
```

---

## Rules

- **KHÔNG invent** thông tin không có trong SpecFlow output — để `[CẦN ĐIỀN]` rõ ràng
- **KHÔNG xóa** file cũ mà không hỏi human (ngoại trừ folder rác tên literal braces)
- **KHÔNG bỏ qua** bất kỳ file `.md` nào trong SpecFlow output — đọc hết Bước 0
- **KHÔNG dùng** brace expansion `{a,b,c}` khi tạo folders — dùng lệnh `mkdir -p` riêng từng cái
- **DỪNG lại** khi phát hiện conflict — không tự chọn, không tiếp tục khi chưa có human confirm
- **Chạy đầy đủ** tất cả bước, không skip — đây là one-time migration skill

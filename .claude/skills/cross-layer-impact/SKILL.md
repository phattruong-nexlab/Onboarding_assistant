# Skill: cross-layer-impact

## Trigger
`/cross-layer-impact [feature-name]` — chạy sau khi design.md được approve.
Hoặc tự động trigger khi `docs/API_CONTRACTS.md` thay đổi.

## Mục đích
Phân tích thay đổi trong design.md → detect tất cả layers bị ảnh hưởng
→ tạo tasks cross-layer rõ ràng → update SPRINT_CONTRACT với dependency map.

Không để dev một layer không biết layer khác đang thay đổi gì liên quan đến mình.

---

## BƯỚC 1 — Đọc context

```bash
# Detect layers có trong project
[ -d "frontend" ] && echo "FE layer"
[ -d "backend" ]  && echo "BE layer"
[ -d "mobile" ]   && echo "Mobile layer"

# Đọc design.md của feature
cat specs/[feature-name]/design.md
cat docs/API_CONTRACTS.md  # contracts hiện tại
```

---

## BƯỚC 2 — Phân tích impact

Với mỗi thay đổi trong design.md, tự hỏi:

```
API Contract thay đổi?
  → BE: cần update implementation
  → FE: cần update service layer + types
  → Mobile: cần update API calls / GraphQL queries

DB Schema thay đổi?
  → BE: cần migration + update models
  → FE: có thể cần update nếu display data mới
  → Mobile: có thể cần update models

New feature (không phải thay đổi)?
  → Xác định layer nào cần implement gì
  → Xác định layer nào có thể làm song song
  → Xác định layer nào phải đợi layer khác
```

---

## BƯỚC 3 — Generate impact report

```
⚡ CROSS-LAYER IMPACT ANALYSIS — [feature-name]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Thay đổi phát hiện:
  [Mô tả thay đổi cụ thể từ design.md]

Layers bị ảnh hưởng:

  🔧 BE — [X] tasks
     [mô tả cụ thể BE cần làm gì]

  🖥  FE — [X] tasks  (hoặc "Không ảnh hưởng")
     [mô tả cụ thể FE cần làm gì]

  📱 Mobile — [X] tasks  (hoặc "Không ảnh hưởng")
     [mô tả cụ thể Mobile cần làm gì]

Dependency:
  [Layer A] phải xong trước [Layer B] vì [lý do]
  [Layer X] và [Layer Y] có thể làm song song

⚠️ Sync point bắt buộc:
  Tất cả layers phải done trước khi merge vào [branch]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## BƯỚC 4 — Tạo tasks trong specs/[feature]/tasks.md

Với mỗi layer bị ảnh hưởng, tạo tasks với scope rõ ràng:

```markdown
### TASK-XXX: [Tên — Layer]

```yaml
id: TASK-XXX
scope: [BE | FE | Mobile]
status: pending
depends-on: [TASK-YYY]  ← điền nếu có dependency
estimate: [thời gian]
```

**Mô tả:** [Claude tự viết từ phân tích Bước 2]

**Acceptance Criteria:**
- [ ] [Criterion cụ thể, measurable]
- [ ] Tests pass
[Mobile only]:
- [ ] Human verify trên app thật
```

---

## BƯỚC 5 — Update SPRINT_CONTRACT

Append vào `logs/SPRINT_CONTRACT.md`:

```markdown
## Cross-Layer Sync — [feature-name]

**Ngày phân tích:** [hôm nay]
**Trigger:** design.md approved

### Dependency Map
```
[TASK-001 BE] → [TASK-003 FE]
             ↘ [TASK-004 Mobile]  ← song song với TASK-003
[TASK-003 FE] + [TASK-004 Mobile] → [TASK-005 Integration]
```

### Sync Rule
KHÔNG merge bất kỳ layer nào vào develop trước khi:
  □ BE: TASK-001, TASK-002 done
  □ FE: TASK-003 done
  □ Mobile: TASK-004 done + human verified

### Người chịu trách nhiệm cross-layer
@[tech-lead hoặc PM]
```

---

## BƯỚC 6 — Update ALL_TASKS.md

Move feature từ "Approved" sang "In Progress" với đầy đủ layer info:

```markdown
| [feature-name] | implementing | FE+BE+Mobile | @fe | @be | @mobile | 🔄 TASK-001/5 |
```

---

## Rules

- Không tạo task mơ hồ — mỗi task phải rõ layer, rõ scope
- Nếu không chắc layer nào bị ảnh hưởng → hỏi human, không đoán
- Luôn tạo sync point rõ ràng trong SPRINT_CONTRACT
- Mobile tasks luôn có "human verify trên app thật" trong AC

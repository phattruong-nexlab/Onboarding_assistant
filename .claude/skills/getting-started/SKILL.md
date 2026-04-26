# Getting Started

> Đọc file này ĐẦU TIÊN khi bắt đầu session mới.
> File này là index — nó cho bạn biết mọi thứ có sẵn trong project.

---

## Bước 1 — Nắm trạng thái hiện tại

Đọc ngay: `logs/CONTEXT_SNAPSHOT.md`

File này cho bạn biết:
- Sprint hiện tại đang làm gì
- Task nào đang dở, task nào blocked
- Quyết định quan trọng gần nhất
- Bước tiếp theo cần làm

---

## Bước 2 — Hiểu project

| Cần biết | Đọc file |
|---|---|
| Tech stack, build commands | `steering/tech-stack.md` |
| Coding conventions | `steering/conventions.md` |
| API standards (REST) | `steering/api-standards.md` |
| Mobile patterns | `steering/flutter-patterns.md` *(nếu có Mobile layer)* |
| Security rules | `steering/security.md` |
| Architecture tổng quan | `docs/ARCHITECTURE.md` |
| API contracts (REST) | `docs/API_CONTRACTS.md` |
| API contracts (GraphQL) | `docs/GRAPHQL_CONTRACTS.md` *(nếu Mobile dùng GraphQL)* |
| Screen flows (Mobile) | `docs/SCREEN_FLOWS.md` *(nếu có Mobile layer)* |
| Quyết định kỹ thuật | `docs/DECISIONS.md` |
| Layers của project này | `AGENTS.md` → xem Agent Registry |

---

## Bước 3 — Chọn workflow

### Khởi động từ SpecFlow output (chạy 1 lần)
```
/init-from-specflow
  → Đọc toàn bộ SpecFlow output
  → Cross-check conflicts
  → Hỏi layer selection (FE/BE/Mobile)
  → Gọi /init-layers để copy đúng layer files
  → Transform thành SDD Architecture đầy đủ
```

### Thêm layer mới vào project đang có
```
/init-layers
  → Hỏi layer nào cần thêm (FE/BE/Mobile)
  → Hỏi Mobile tech stack (nếu chọn Mobile)
  → Copy đúng files từ layers/ vào project
```

### Brownfield Mobile (đã có app đang production)
```
/setup-environment  → Chạy được app local trước
/brownfield-audit   → Hiểu app làm gì, generate docs
/brownfield-risk-scan → Biết risks trước khi touch code
```

### Bắt đầu feature mới
```
1. /spec-init [feature-name]
2. /spec-requirements [feature]  → Human review gate ①
3. /spec-design [feature]        → Human review gate ②
   /cross-layer-impact [feature] → Tạo tasks cho tất cả layers bị ảnh hưởng
4. /spec-tasks [feature]         → Human review gate ③
5. /spec-impl [feature]          → Subagents implement theo layer
```

### Tiếp tục task đang dở
```
1. Đọc logs/CONTEXT_SNAPSHOT.md
2. Đọc specs/[feature]/tasks.md — task nào chưa done
3. /spec-impl [feature] --resume
```

### Review & finish
```
1. @spec-compliance-reviewer → Stage 1: đúng spec?
2. @code-quality-reviewer    → Stage 2: code clean?
[Mobile only]:
3. /explain-changes          → Giải thích bằng tiếng Việt
4. /how-to-verify            → Human verify trên app thật
5. Human confirm ✓
6. /quality-gate             → Chạy checklist
7. /finish-task [task-id]    → Commit + update log
```

### Evaluate (Human trigger)
```
/run-evaluation fe     → FE Evaluator
/run-evaluation be     → BE Evaluator
/run-evaluation mobile → Mobile Evaluator
/run-evaluation both   → FE + BE
/run-evaluation all    → FE + BE + Mobile
```

---

## Skills có sẵn (21 core + mobile layer skills)

### Core skills (mọi project)

| Skill | Dùng khi |
|---|---|
| `init-from-specflow` | Chạy ngay sau SpecFlow export — đọc hết, cross-check, hỏi layers |
| `init-project` | Brownfield web — scan codebase → auto-gen docs |
| `init-layers` | Thêm layer FE/BE/Mobile vào project |
| `doctor` | Verify package structure đúng chuẩn |
| `spec-init` | Bắt đầu feature mới |
| `spec-requirements` | Phase 1 — requirements (EARS format) |
| `spec-design` | Phase 2 — design (API contracts, DB schema, per-layer sections) |
| `cross-layer-impact` | Sau design approved — detect impact + tạo tasks cho tất cả layers |
| `validate-gap` | Check design vs code hiện có |
| `validate-design` | Check tasks vs architecture |
| `spec-tasks` | Phase 3 — break thành atomic tasks |
| `spec-impl` | Phase 4 — implement bằng subagents |
| `spec-check` | Self-audit vs acceptance criteria |
| `finish-task` | Verify done + commit + update log |
| `quality-gate` | Checklist trước khi merge |
| `research` | Research kỹ thuật |
| `log-session` | Update CONTEXT_SNAPSHOT cuối session |
| `run-evaluation` | Trigger evaluators chấm điểm |
| `run-harness` | Full pipeline: Planner→Generator→Evaluator |
| `create-skill` | Tạo skill mới cho team |
| `getting-started` | File này |

### Mobile layer skills (chỉ có nếu project có Mobile layer)

| Skill | Dùng khi |
|---|---|
| `explain-changes` | Tự động sau mỗi Mobile task — giải thích tiếng Việt |
| `how-to-verify` | Hướng dẫn human verify trên app thật |
| `debug-mobile` | App có lỗi — debug theo từng bước |
| `setup-environment` | *(Brownfield)* Cài môi trường, chạy app local |
| `brownfield-audit` | *(Brownfield Flutter)* Hiểu app, generate docs |
| `discover-graphql` | *(Flutter + GraphQL)* Update GRAPHQL_CONTRACTS.md |

---

## Agents có sẵn

### Core agents (mọi project)

| Agent | Gọi bằng | Làm gì |
|---|---|---|
| `planner` | @planner | Tạo SPRINT_CONTRACT |
| `spec-compliance-reviewer` | @spec-compliance-reviewer | Stage 1: đúng spec? |
| `code-quality-reviewer` | @code-quality-reviewer | Stage 2: code clean? |
| `api-contract-checker` | @api-contract-checker | Check FE-BE-Mobile drift |
| `researcher` | @researcher | Research + recommend |
| `doc-writer` | @doc-writer | Generate/update docs |

### Layer agents (chỉ có nếu layer tương ứng được init)

| Agent | Layer | Làm gì |
|---|---|---|
| `fe-generator` | Frontend | Implement FE tasks |
| `fe-evaluator` | Frontend | Chấm FE (0-50) |
| `be-generator` | Backend | Implement BE tasks |
| `be-evaluator` | Backend | Chấm BE (0-50) |
| `flutter-generator` | Mobile/Flutter | Implement Flutter tasks |
| `flutter-evaluator` | Mobile/Flutter | Chấm Mobile (0-50) |
| `graphql-checker` | Mobile/Flutter+GraphQL | Check GraphQL drift |

---

## Instincts (Tự động)

- Chạm REST API file → tự check `docs/API_CONTRACTS.md`
- Chạm GraphQL file → tự check `docs/GRAPHQL_CONTRACTS.md` *(nếu có)*
- Sau Mobile task → tự chạy `explain-changes` + `how-to-verify`
- Trước finish-task → tự chạy tests
- Session kết thúc → nhắc update `logs/CONTEXT_SNAPSHOT.md`

---

## Evaluator Rubric

**FE** (pass ≥40/50): Spec | UI Quality | Responsive | Error Handling | API Integration

**BE** (pass ≥40/50): Spec | Contract | Error Responses | Security | Tests

**Mobile** (pass ≥40/50): Spec | UI/UX | Platform behavior | Code Quality | Tests

> Security fail bất kỳ tiêu chí → BLOCK ngay

---

## Quy trình kết thúc session

```
/log-session
→ Update logs/CONTEXT_SNAPSHOT.md
→ Append logs/SESSION_LOG.md
→ Commit tất cả thay đổi
```

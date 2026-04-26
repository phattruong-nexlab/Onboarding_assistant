# Skill: run-evaluation

## Trigger
`/run-evaluation [fe|be|both]` — Human trigger. Không tự động chạy.

## Mục đích
Trigger FE/BE Evaluator agents chấm điểm implementation theo rubric.
Kết quả ghi vào `logs/EVALUATION_REPORT.md`.

## Pre-condition
- Feature phải đang chạy được (not broken build)
- Với FE evaluation: cần Playwright MCP được cài và kết nối
- Với BE evaluation: cần server đang chạy (local hoặc staging)

## Các bước thực hiện

### Nếu `/run-evaluation fe`
```
Trigger: @fe-evaluator

Rubric chấm điểm (0-10 mỗi tiêu chí):
1. Spec Compliance    — Có đủ tính năng theo tasks.md không?
2. UI Quality         — Có đúng design system / style guide không?
3. Responsive         — Hoạt động trên mobile + desktop?
4. Error Handling     — Empty state, loading state, error state đủ chưa?
5. API Integration    — Gọi đúng contract trong API_CONTRACTS.md không?

Pass threshold: >= 40/50
```

### Nếu `/run-evaluation be`
```
Trigger: @be-evaluator

Rubric chấm điểm (0-10 mỗi tiêu chí):
1. Spec Compliance    — Đủ endpoints theo tasks.md không?
2. Contract Adherence — Response schema khớp API_CONTRACTS.md không?
3. Error Responses    — 400/401/404/500 đúng format không?
4. Security           — Không hardcode secrets, validation đủ không?
5. Test Coverage      — Tests pass? Coverage đạt threshold?

Pass threshold: >= 40/50
Security fail bất kỳ tiêu chí → BLOCK ngay, không đợi tổng điểm
```

### Nếu `/run-evaluation both`
Chạy FE evaluator trước, sau đó BE evaluator.

## Output format (logs/EVALUATION_REPORT.md)

```markdown
## Evaluation Report: [feature-name]
Date: YYYY-MM-DD
Triggered by: @member

### FE Evaluation
| Tiêu chí | Điểm | Notes |
|----------|------|-------|
| Spec Compliance | 9/10 | Thiếu empty state ở danh sách |
| UI Quality | 8/10 | |
| Responsive | 10/10 | |
| Error Handling | 7/10 | Chưa có loading skeleton |
| API Integration | 10/10 | |
| **TOTAL** | **44/50** | ✅ PASS |

**Feedback cho Generator:**
- [Cụ thể cần fix gì]

### BE Evaluation
| Tiêu chí | Điểm | Notes |
|----------|------|-------|
| Spec Compliance | 10/10 | |
| Contract Adherence | 10/10 | |
| Error Responses | 9/10 | 422 chưa có details |
| Security | 10/10 | |
| Test Coverage | 8/10 | Coverage 76%, threshold 80% |
| **TOTAL** | **47/50** | ✅ PASS |

**Feedback cho Generator:**
- [Cụ thể cần fix gì]

### Decision
Human quyết định: ☐ Ship as-is / ☐ Fix issues / ☐ Iterate
```

## Sau khi có kết quả

Human đọc report và quyết định:
- **PASS + Ship:** Merge, deploy
- **PASS + Fix minor:** Generator fix theo feedback, không cần re-evaluate
- **FAIL:** Generator iterate, chạy `/run-evaluation` lại sau khi fix

# Skill: quality-gate

## Trigger
`/quality-gate` — chạy trước khi tạo PR / merge branch.

## Mục đích
Chủ động chạy checklist thay vì markdown thụ động.
Báo cáo pass/fail từng tiêu chí — không phải chỉ nhắc nhở.

## Các bước thực hiện

### 1. Chạy automated checks

```bash
# Linting
cd frontend && [lint command] 2>&1 | tail -5
cd backend && [lint command] 2>&1 | tail -5

# Tests
cd frontend && [test command] 2>&1 | tail -10
cd backend && [test command] 2>&1 | tail -10

# Check for secrets (basic)
grep -rn "password\s*=\s*['\"]" --include="*.ts" --include="*.py" frontend/src backend/src
grep -rn "api_key\s*=\s*['\"]" --include="*.ts" --include="*.py" frontend/src backend/src
```

### 2. Manual checks (Claude verify)

```
[ ] API_CONTRACTS.md đã được update với contracts mới?
[ ] Migration files có cả up và down?
[ ] Không có TODO comment nào thiếu ticket reference?
[ ] TECH_DEBT.md đã update nếu có trade-off tạm thời?
[ ] DECISIONS.md đã update nếu có ADR mới?
```

### 3. Báo cáo

```markdown
## Quality Gate Report
Feature: [feature-name]
Date: YYYY-MM-DD

### Automated Checks
| Check | Result | Details |
|-------|--------|---------|
| FE Lint | ✅ PASS | 0 errors |
| BE Lint | ✅ PASS | 0 errors |
| FE Tests | ✅ PASS | 45/45 passed |
| BE Tests | ⚠️ FAIL | 2 tests failing |
| Secrets scan | ✅ PASS | No hardcoded secrets |

### Manual Checks
| Check | Result |
|-------|--------|
| API_CONTRACTS.md updated | ✅ |
| Migration files complete | ✅ |
| TODO comments clean | ⚠️ 1 TODO without ticket |
| TECH_DEBT.md updated | ✅ |
| DECISIONS.md updated | ✅ |

### Verdict
❌ FAIL — Fix trước khi merge:
1. BE Tests: [tên 2 tests failing]
2. TODO: [file:line] thiếu ticket reference
```

### 4. Nếu FAIL
KHÔNG tạo PR. Báo human và/hoặc fix ngay nếu đơn giản.

### 5. Nếu PASS
```
✅ Quality Gate PASS — sẵn sàng tạo PR.

Bước tiếp theo:
- Tạo PR với description đầy đủ (what, why, how to test)
- Assign reviewer
- Chạy /run-evaluation nếu chưa chạy
```

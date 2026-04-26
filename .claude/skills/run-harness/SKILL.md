# Skill: run-harness

## Trigger
`/run-harness [feature-name]` — Human trigger duy nhất. Không chạy tự động.

## Mục đích
Chạy full pipeline: Planner → Generator → Evaluator cho một feature.
Dùng khi muốn autonomous implementation với quality control.

## Quan trọng — Human quyết định

Harness tốn token đáng kể. Human phải:
1. Confirm feature spec đã approved đầy đủ (cả 3 gates)
2. Confirm app đang chạy được (không có broken build)
3. Confirm sẵn sàng review evaluation report sau

## Pipeline

```
BƯỚC 1: PLANNER
@planner → đọc spec → tạo SPRINT_CONTRACT
→ Human review SPRINT_CONTRACT → confirm proceed

BƯỚC 2: GENERATOR (FE + BE song song nếu có thể)
@fe-generator → implement FE tasks
@be-generator → implement BE tasks
→ Mỗi task: spec-check → Stage 1 review → Stage 2 review → finish-task

BƯỚC 3: EVALUATOR (Human trigger sau khi Generator done)
/run-evaluation [fe|be|both]
→ Output: EVALUATION_REPORT.md
→ Human quyết định: ship / fix minor / iterate
```

## Checkpoint sau mỗi bước

```
Sau Planner:
"SPRINT_CONTRACT đã tạo. Review tại logs/SPRINT_CONTRACT.md.
Xác nhận để bắt đầu Generator? [yes/no]"

Sau Generator:
"Generator hoàn thành. X/Y tasks done, Z blocked.
Chạy Evaluator? [yes/no]"

Sau Evaluator:
"Evaluation report tại logs/EVALUATION_REPORT.md.
Quyết định: ship / fix minor / iterate?"
```

## Rules bắt buộc

- Hỏi human confirm sau mỗi bước — KHÔNG tự động tiếp tục
- Nếu Generator bị blocked > 30% tasks → pause, báo human ngay
- Không skip Evaluator kể cả Generator báo cáo success
- Human là người duy nhất quyết định "ship"

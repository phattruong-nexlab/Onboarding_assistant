# Instinct: Always Run Tests Before Finishing

## Trigger

Trước khi chạy skill `finish-task` hoặc trước khi commit.

## Hành động bắt buộc

```bash
# FE tasks
cd frontend && [test command từ steering/tech-stack.md]

# BE tasks
cd backend && [test command từ steering/tech-stack.md]

# Both
cd frontend && [test] && cd ../backend && [test]
```

## Nếu tests fail

- KHÔNG commit
- KHÔNG bỏ qua
- Fix failing tests trước
- Nếu test sai (test cần update vì requirements thay đổi) → báo human confirm trước khi sửa test

## Nếu không có tests

- Ghi vào `docs/TECH_DEBT.md`: "TASK-XXX thiếu test coverage"
- Vẫn phải có ít nhất 1 happy path test mới được commit

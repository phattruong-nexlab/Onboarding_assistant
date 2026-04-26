# Rules: Common (Áp dụng cho cả FE lẫn BE)

> File này được Claude đọc khi làm việc trong bất kỳ phần nào của project.

---

## Code Quality

- Không dùng magic numbers — đặt tên constant có nghĩa
- Không để dead code — xóa thay vì comment out
- Không dùng `any` type (TypeScript) — narrow type hoặc dùng `unknown`
- Function phải có tên mô tả hành động: `getUserById` không phải `getUser`
- Boolean variables/functions: dùng prefix `is`, `has`, `can`, `should`

## Error Handling

- Không bao giờ catch error mà không làm gì cả (empty catch)
- Log error với đủ context để debug được
- User-facing error messages phải human-readable — không phải stack trace
- Phân biệt rõ: lỗi của user (4xx) vs lỗi của system (5xx)

## Testing

- Test phải độc lập — không phụ thuộc order chạy
- Tên test mô tả scenario: `should return 404 when user not found`
- Mock external dependencies trong unit tests
- Không test implementation details — test behavior

## Security (luôn luôn)

- Không hardcode secrets — xem `steering/security.md`
- Validate mọi input tại system boundary
- Không log sensitive data

## Git

- Commit nhỏ, thường xuyên — một logical change một commit
- Conventional commits format bắt buộc
- Không commit: `.env`, `node_modules`, build artifacts, `*.log`

## Documentation

- Code tự giải thích là tốt nhất
- Comment giải thích WHY, không phải WHAT
- TODO phải có ticket: `// TODO [PROJ-123]:`
- Public APIs phải có JSDoc / docstring

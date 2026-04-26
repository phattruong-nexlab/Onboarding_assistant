# Rules: Backend

> Áp dụng khi Claude làm việc trong `/backend` hoặc task có `scope: BE`.
> Đọc thêm: `backend/CLAUDE.md` cho project-specific BE rules.

---

## API Design

- Tuân thủ `steering/api-standards.md` — không có exception
- Mọi endpoint phải có validation (Pydantic / Zod / class-validator)
- Response format nhất quán — xem `docs/API_CONTRACTS.md`
- Không expose internal errors cho client — log server-side, trả generic message

## Architecture

- Controller/Route: chỉ handle HTTP (parse request, call service, return response)
- Service: business logic — không biết về HTTP
- Repository: data access — không biết về business logic
- Dependency injection — không hardcode dependencies

## Database

- KHÔNG thay đổi schema mà không có migration file
- Migration có cả `up` và `down`
- Index foreign keys và fields thường query
- Không để N+1 queries — eager load khi cần
- Transactions cho operations liên quan nhiều tables

## Error Handling

- Custom exception classes với error codes rõ ràng
- Catch errors ở service layer — không để bubble up thành 500
- Log errors với đủ context: user id, request id, input data (bỏ sensitive fields)

## Security

- Auth middleware trên mọi protected route
- Rate limiting trên auth endpoints
- Parameterized queries — không bao giờ string concat SQL
- Sanitize input trước khi lưu DB

## Testing

- Unit test services với mocked repository
- Integration test API endpoints với test database
- Seed data cho tests — không dùng production data

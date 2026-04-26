# Instinct: Always Check API Contract

## Trigger (Tự động kích hoạt)

Khi Claude chuẩn bị tạo hoặc sửa bất kỳ file nào liên quan đến:
- API calls (fetch, axios, HTTP client)
- API endpoint definitions (routes, controllers)
- Request/Response types hoặc interfaces
- API_CONTRACTS.md

## Hành động bắt buộc

**TRƯỚC KHI viết bất kỳ API-related code:**

1. Đọc `docs/API_CONTRACTS.md`
2. Đọc `steering/api-standards.md`
3. Nếu đang implement spec → đọc `specs/[feature]/design.md` phần API Contracts
4. Verify: code sắp viết có khớp với contracts không?

**Nếu phát hiện mismatch:**
- STOP — không implement theo kiểu "tôi nghĩ đúng hơn"
- Báo human: "Contract trong design.md nói X, nhưng tôi thấy existing code đang dùng Y"
- Chờ clarification

**Nếu contract chưa có:**
- STOP — không tự define contract
- Báo human: "Endpoint này chưa có trong API_CONTRACTS.md, cần define trước"

## Lý do

FE và BE implement cùng một contract. Nếu một bên drift thì integration fail.
Việc kiểm tra contract mất 30 giây. Việc fix integration bug mất nhiều giờ.

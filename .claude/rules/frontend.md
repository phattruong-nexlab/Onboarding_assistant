# Rules: Frontend

> Áp dụng khi Claude làm việc trong `/frontend` hoặc task có `scope: FE`.
> Đọc thêm: `frontend/CLAUDE.md` cho project-specific FE rules.

---

## Component Design

- Một component làm đúng 1 việc — tách nếu quá 150 dòng
- Props phải typed đầy đủ — không dùng prop spreading vô tội vạ
- Tránh prop drilling quá 2 levels — dùng context hoặc state management
- Extract custom hooks khi logic phức tạp hoặc reusable

## State Management

- Phân biệt rõ: server state vs UI state vs global state
- Không lưu derived data vào state — tính toán trong render
- Reset state khi component unmount nếu cần

## API Integration (QUAN TRỌNG)

- Tất cả API calls qua service layer — không fetch trực tiếp từ component
- Đọc `docs/API_CONTRACTS.md` trước khi implement bất kỳ API call nào
- Handle 3 states bắt buộc: loading, success, error
- Handle network error và timeout

## UI/UX Rules

- Mọi action có response tức thì (optimistic UI hoặc loading indicator)
- Empty states phải có UI — không để blank screen
- Error states phải actionable — không chỉ hiện "Có lỗi xảy ra"
- Form validation: inline errors, không phải alert
- Accessible: semantic HTML, alt text, keyboard navigation

## Performance

- Lazy load routes và heavy components
- Không để memory leak (cleanup useEffect)
- Images phải có width/height để tránh layout shift

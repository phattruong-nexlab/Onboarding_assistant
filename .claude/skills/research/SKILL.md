# Skill: research

## Trigger
`/research [chủ đề]` hoặc khi cần thông tin kỹ thuật trước khi quyết định.

## Mục đích
Research nhanh và có cấu trúc — không mất thời gian vào rabbit holes.

## Các bước thực hiện

### 1. Define câu hỏi cụ thể

Trước khi research, xác định:
- Câu hỏi chính cần trả lời là gì?
- Kết quả research sẽ ảnh hưởng đến quyết định gì?
- Cần bao nhiêu depth? (quick scan vs deep dive)

### 2. Spawn @researcher agent

```
@researcher [câu hỏi research cụ thể]

Context:
- Project đang dùng: [tech stack từ steering/tech-stack.md]
- Vấn đề cụ thể: [mô tả ngắn]
- Cần quyết định: [quyết định gì dựa trên research]
```

### 3. Đánh giá kết quả

Sau khi researcher trả về, kiểm tra:
- Recommendation có rõ ràng không?
- Evidence đủ không?
- Có phù hợp với constraints của project không?

### 4. Lưu kết quả (nếu quan trọng)

Nếu research dẫn đến quyết định kỹ thuật quan trọng → thêm vào `docs/DECISIONS.md`.

```markdown
## ADR-XXX: [Tiêu đề từ research]
**Date:** [today]
**Context:** Research về [chủ đề]
**Decision:** [Kết luận]
**Rationale:** [Lý do từ research findings]
```

## Ví dụ use cases

```
/research "So sánh Zustand vs Jotai cho state management trong Next.js 14"
/research "Best practice cho refresh token rotation với httpOnly cookies"
/research "Cách handle optimistic updates khi API fail"
```

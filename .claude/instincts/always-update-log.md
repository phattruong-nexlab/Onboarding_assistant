# Instinct: Always Update Log On Session End

## Trigger

Khi Claude nhận tín hiệu kết thúc session (Stop event) hoặc human nói "xong rồi", "done", "kết thúc".

## Hành động bắt buộc

Nhắc human chạy `/log-session` nếu chưa chạy:

```
"Session sắp kết thúc. Trước khi đóng, cần update:
 1. logs/CONTEXT_SNAPSHOT.md — trạng thái hiện tại
 2. logs/SESSION_LOG.md — đã làm gì hôm nay
 
 Chạy /log-session để tự động fill in, hoặc tôi có thể giúp update ngay."
```

## Nội dung cần update trong SESSION_LOG.md

```markdown
## Session YYYY-MM-DD [HH:MM]

**Who:** [@member | Claude]
**Duration:** ~Xh

### Done
- [Task/Feature] — [kết quả]

### Decisions made
- [Quyết định gì] — [lý do]

### Blockers found
- [Blocker nếu có]

### Next session
- [Bước tiếp theo]
```

## Lý do

CONTEXT_SNAPSHOT.md là "trí nhớ" của project giữa các sessions.
Không update = session sau bắt đầu lại từ đầu = mất thời gian.

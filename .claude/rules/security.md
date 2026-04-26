# Rules: Security

> Override mọi rule khác. Apply mọi lúc, mọi nơi trong project.
> Đây là bản rút gọn để Claude đọc nhanh — chi tiết xem `steering/security.md`.

---

## Instant STOP conditions

Dừng ngay và báo human nếu:
- Sắp hardcode secret / credential / API key
- Phát hiện SQL string concatenation với user input
- Thấy token/password trong log statement
- Thấy stack trace trả về trong API response cho client

---

## Checklist trước mỗi commit

```
[ ] Không có secret nào trong code
[ ] Input được validate tại API boundary
[ ] Auth middleware đúng chỗ
[ ] Error messages không expose internals
```

---

## Quick reference

```python
# ✅ Đúng
secret = os.getenv("SECRET_KEY")
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))

# ❌ Sai — STOP ngay
secret = "sk-1234abcd"
cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
```

---

## Nếu phát hiện security issue trong code đang review

```
1. STOP — không tiếp tục
2. Báo human: "Phát hiện security issue tại [file:line]"
3. Mô tả: risk là gì, impact như thế nào
4. Suggest fix nhưng không tự apply nếu đây là production code
```

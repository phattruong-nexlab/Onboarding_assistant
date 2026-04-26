# Rules: API Design

> Áp dụng khi Claude tạo hoặc sửa bất kỳ file liên quan đến API.
> Đây là chuẩn bắt buộc cho cả FE (service layer) và BE (routes/controllers).

---

## Trước khi implement bất kỳ API call nào

```
1. Đọc docs/API_CONTRACTS.md
2. Đọc steering/api-standards.md
3. Nếu contract chưa có → STOP, báo human
4. Nếu contract mâu thuẫn với existing code → báo human, không tự quyết
```

## FE — Service Layer Rules

```typescript
// ✅ Đúng — tất cả calls qua service
// frontend/src/services/user.service.ts
export const getUser = async (id: string): Promise<User> => {
  const response = await api.get(`/users/${id}`)
  return response.data.data
}

// ❌ Sai — fetch trực tiếp từ component
const MyComponent = () => {
  useEffect(() => {
    fetch('/api/v1/users/me') // KHÔNG
  }, [])
}
```

```typescript
// ✅ Đúng — handle 3 states
const { data, isLoading, error } = useQuery(...)

if (isLoading) return <Skeleton />
if (error) return <ErrorState message={error.message} />
return <UserCard data={data} />

// ❌ Sai — chỉ handle success
const data = await getUser(id)
return <UserCard data={data} />
```

## BE — Controller Rules

```typescript
// ✅ Đúng — controller chỉ handle HTTP
router.post('/users', validate(createUserSchema), async (req, res) => {
  const user = await userService.create(req.body)  // delegate to service
  res.status(201).json({ success: true, data: user })
})

// ❌ Sai — business logic trong controller
router.post('/users', async (req, res) => {
  const hashedPassword = await bcrypt.hash(req.body.password, 10)  // KHÔNG
  const user = await db.users.create({ ...req.body, password: hashedPassword })
  res.json(user)
})
```

## Response Format (bắt buộc theo api-standards.md)

```typescript
// ✅ Đúng
res.json({ success: true, data: user })
res.status(400).json({ success: false, error: { code: 'VALIDATION_ERROR', message: '...' } })

// ❌ Sai
res.json(user)  // thiếu wrapper
res.json({ error: 'Something went wrong' })  // không có success flag và error code
```

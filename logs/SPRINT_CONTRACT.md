# Sprint Contract

> Output của Planner agent — điền trước khi bắt đầu implement.
> FE và BE đều phải đồng ý với contract này trước khi code.

---

## Sprint [Name/Number]

**Created:** YYYY-MM-DD bởi @planner agent
**Period:** YYYY-MM-DD → YYYY-MM-DD
**Features in sprint:** [feature-1], [feature-2]

---

## Scope Agreement

### FE Scope
```
Tasks FE sẽ implement:
- TASK-001: [Tên] (est: Xh)
- TASK-003: [Tên] (est: Xh)

FE sẽ KHÔNG làm:
- [Những gì nằm ngoài FE scope]

FE phụ thuộc vào BE:
- TASK-002 phải done trước TASK-003 có thể bắt đầu
```

### BE Scope
```
Tasks BE sẽ implement:
- TASK-002: [Tên] (est: Xh)
- TASK-004: [Tên] (est: Xh)

BE sẽ KHÔNG làm:
- [Những gì nằm ngoài BE scope]
```

---

## Interface Agreement (FE ↔ BE)

> Đây là phần quan trọng nhất — FE và BE cùng verify trước khi sign-off.

### Endpoints được implement trong sprint này

| Endpoint | Status | FE needs by | BE delivers by |
|----------|--------|-------------|----------------|
| POST /api/v1/[resource] | Mới | YYYY-MM-DD | YYYY-MM-DD |
| GET /api/v1/[resource] | Mới | YYYY-MM-DD | YYYY-MM-DD |

Contracts chi tiết: `docs/API_CONTRACTS.md`

---

## Risks & Dependencies

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| [Risk 1] | Low/Med/High | Low/Med/High | [Plan B] |

---

## Sign-off

- [ ] FE Lead đồng ý với scope và contracts: @____
- [ ] BE Lead đồng ý với scope và contracts: @____
- [ ] PM đồng ý với timeline: @____

**Status:** ☐ Draft → ☐ Agreed → ☐ In Progress → ☐ Completed

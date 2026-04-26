# PRD: Onboarding Assistant
**Product Requirements Document**
**Phiên bản:** 1.0 | **Ngày:** Tháng 4, 2026 | **Trạng thái:** Draft

---

## 1. Tổng Quan Sản Phẩm

### 1.1 Mục Tiêu

Onboarding Assistant là một hệ thống AI-powered giúp tự động hóa việc tạo, kiểm tra và cập nhật tài liệu kỹ thuật từ source code. Sản phẩm giải quyết vấn đề tài liệu bị lỗi thời, không đồng bộ với code, khiến quá trình onboarding nhân sự mới kéo dài và tốn kém nguồn lực senior.

### 1.2 Tuyên Bố Vấn Đề

Hiện tại, các nhóm kỹ thuật đang đối mặt với các vấn đề nghiêm trọng:

- **Tài liệu lỗi thời:** Documentation trong repo thường không được cập nhật khi code thay đổi, dẫn đến sai lệch nghiêm trọng giữa mô tả và thực tế.
- **Không có owner:** Không có cá nhân hoặc quy trình rõ ràng chịu trách nhiệm duy trì tài liệu.
- **Onboarding chậm:** Nhân sự mới mất 1–2 tuần chỉ để hiểu được flow hệ thống, phải đọc code thủ công và hỏi senior liên tục.
- **Chi phí support cao:** Senior engineer bị gián đoạn công việc thường xuyên để hỗ trợ người mới, giảm năng suất toàn team.
- **Rủi ro hiểu sai:** QA, BA dễ có hiểu biết sai về logic hệ thống, dẫn đến bug và yêu cầu sai.

### 1.3 Mục Tiêu Kinh Doanh

| Mục tiêu | Chỉ số đo lường | Target |
|-----------|-----------------|--------|
| Giảm thời gian onboarding | Thời gian để nhân sự mới tự làm việc độc lập | ≤ 3 ngày (từ 1–2 tuần) |
| Giảm thời gian support của senior | Giờ/tuần senior dành cho support onboarding | Giảm 60% |
| Tăng tỷ lệ docs đồng bộ với code | % tài liệu chính xác so với codebase | ≥ 90% |
| Giảm bug do hiểu sai tài liệu | Số bug liên quan đến tài liệu sai | Giảm 50% |

---

## 2. Người Dùng & Personas

### 2.1 Nhóm Người Dùng Mục Tiêu

#### Persona 1: Nhân Sự Mới (Primary User)
- **Đối tượng:** Developer, Data Engineer, Backend Engineer mới vào team
- **Nỗi đau:** Mất nhiều giờ đọc code để hiểu flow, ngại hỏi senior vì sợ làm phiền
- **Nhu cầu:** Tài liệu rõ ràng, chính xác, có thể tự tra cứu
- **Mục tiêu sử dụng:** Xem tài liệu module, API, service flow một cách nhanh chóng

#### Persona 2: Tech Lead / Senior Engineer
- **Đối tượng:** Senior engineer, tech lead chịu trách nhiệm kỹ thuật của team
- **Nỗi đau:** Liên tục bị hỏi những câu hỏi lặp lại, mất focus vào task chính
- **Nhu cầu:** Tự động hóa việc giải thích codebase, giảm thời gian support
- **Mục tiêu sử dụng:** Review và approve tài liệu được AI generate, đảm bảo chất lượng

#### Persona 3: QA / Business Analyst
- **Đối tượng:** QA Engineer, BA cần hiểu hệ thống để viết test case hoặc spec
- **Nỗi đau:** Tài liệu kỹ thuật thường quá sơ sài hoặc sai, khó test đúng logic
- **Nhu cầu:** Mô tả API, data flow và business logic dưới dạng dễ hiểu
- **Mục tiêu sử dụng:** Xem API spec, module description để viết test case và requirement

#### Persona 4: Engineering Manager
- **Đối tượng:** Manager quản lý team kỹ thuật
- **Nỗi đau:** Onboarding tốn nhiều chi phí, khó theo dõi tiến độ nhân sự mới
- **Nhu cầu:** Dashboard tổng quan về trạng thái documentation và onboarding
- **Mục tiêu sử dụng:** Theo dõi coverage của tài liệu, phê duyệt quy trình

---

## 3. Phạm Vi MVP

### 3.1 Trong Phạm Vi (In Scope)

- Scan và phân tích Python/FastAPI codebase
- Kiểm tra tính nhất quán giữa docs và code
- Tự động generate và update tài liệu
- Giao diện Streamlit cho phép review và approve
- Xuất ra Markdown / README

### 3.2 Ngoài Phạm Vi (Out of Scope - Phase 2+)

- Hỗ trợ đa ngôn ngữ lập trình ngoài Python (Java, Go, Node.js)
- Tích hợp trực tiếp vào IDE
- CI/CD pipeline integration (auto-trigger khi merge PR)
- Multi-repo management dashboard
- Role-based access control (RBAC) nâng cao
- Analytics và reporting dashboard

---

## 4. Tính Năng Chi Tiết (Feature Specifications)

### Feature 1: Doc Consistency Checker

**Mô tả:** Tự động quét toàn bộ repo và so sánh với tài liệu hiện tại để phát hiện các điểm không nhất quán.

**User Stories:**
- *Là một Tech Lead,* tôi muốn hệ thống tự động phát hiện các function/API đã bị xóa nhưng vẫn còn được mô tả trong docs, để tôi có thể clean up tài liệu.
- *Là một Developer mới,* tôi muốn biết phần nào của tài liệu đã lỗi thời để không đọc nhầm và làm sai.
- *Là một QA,* tôi muốn hệ thống báo cho tôi biết những module mới chưa có tài liệu, để tôi có thể yêu cầu bổ sung.

**Acceptance Criteria:**
- Hệ thống phát hiện được function/API tồn tại trong docs nhưng đã bị xóa hoặc rename trong code
- Phát hiện được endpoint mô tả sai (sai params, sai response format, sai HTTP method)
- Liệt kê được các module/class mới chưa có tài liệu
- Báo cáo kết quả dưới dạng danh sách có phân loại: Missing / Outdated / Incorrect
- Thời gian scan: ≤ 5 phút cho repo ≤ 10,000 dòng code

**Độ ưu tiên:** P0 – Critical

---

### Feature 2: Auto Update Documentation (Core MVP)

**Mô tả:** Parse source code để hiểu cấu trúc hệ thống, so sánh với tài liệu hiện tại và tự động cập nhật những phần sai hoặc thiếu.

**User Stories:**
- *Là một Senior Engineer,* tôi muốn hệ thống tự động draft nội dung cập nhật cho tài liệu khi code thay đổi, để tôi chỉ cần review và approve thay vì viết từ đầu.
- *Là một Dev mới,* tôi muốn tài liệu luôn phản ánh đúng trạng thái hiện tại của hệ thống để tôi có thể tin tưởng và sử dụng.

**Quy Trình Xử Lý:**
1. Parse source code → extract API endpoints, functions, classes, data models
2. So sánh cấu trúc extracted với nội dung docs hiện tại
3. LLM (Gemini API) phân tích sự khác biệt và generate nội dung mới
4. Trình bày diff (cũ vs. mới) cho user review
5. User accept/reject từng thay đổi
6. Ghi đè file tài liệu sau khi được approve

**Acceptance Criteria:**
- Parse được FastAPI routes (endpoint, method, params, response model)
- Parse được Python functions và docstrings
- Parse được class definitions và relationships
- Generate tài liệu mới/cập nhật đúng format Markdown
- Cho phép partial accept (accept một số thay đổi, reject một số khác)
- Lưu lịch sử thay đổi (versioning đơn giản)

**Độ ưu tiên:** P0 – Critical

---

### Feature 3: Code → Doc Generator

**Mô tả:** Tạo tài liệu từ đầu cho các module/service chưa có tài liệu.

**User Stories:**
- *Là một Developer,* khi tôi viết một module mới, tôi muốn hệ thống tự động generate tài liệu ban đầu để tôi không phải viết tay từ đầu.
- *Là một BA,* tôi muốn có thể xem API spec được generate tự động để tôi hiểu hệ thống nhanh hơn.

**Output Types:**
- **API Spec:** Endpoint URL, HTTP method, request params, request body, response format, error codes
- **Module Description:** Mục đích của module, dependencies, public interface
- **Service Flow Diagram:** Mô tả dạng text/markdown về luồng xử lý dữ liệu qua các service
- **README Template:** Cấu trúc README chuẩn với nội dung được điền tự động

**Acceptance Criteria:**
- Generate API spec đầy đủ từ FastAPI route decorator và type hints
- Generate module description dựa trên class docstring, function names, và imports
- Output đúng chuẩn Markdown, có thể commit thẳng vào repo
- Độ chính xác tối thiểu 80% (đánh giá bởi Senior Engineer review)

**Độ ưu tiên:** P1 – High

---

### Feature 4: Onboarding Assistant UI

**Mô tả:** Giao diện web dựa trên Streamlit cho phép user tương tác với toàn bộ hệ thống một cách trực quan.

**User Stories:**
- *Là một Tech Lead,* tôi muốn có một UI để xem toàn bộ trạng thái tài liệu của repo và duyệt từng thay đổi được AI đề xuất.
- *Là một Dev mới,* tôi muốn có thể chọn module và xem tài liệu tương ứng ngay trên web, không cần phải vào repo đọc code.

**Màn Hình Chính:**

**4.1 Dashboard (Trang chủ)**
- Tổng quan: Số module có docs / chưa có docs / docs lỗi thời
- Danh sách cảnh báo ưu tiên cao
- Nút "Run Scan" để khởi chạy quét mới

**4.2 Consistency Report**
- Danh sách toàn bộ vấn đề phát hiện, phân loại theo severity
- Cho phép filter theo module, loại vấn đề
- Link trực tiếp đến file docs và file code liên quan

**4.3 Doc Review & Approval**
- Hiển thị side-by-side: Doc hiện tại (trái) vs. Doc đề xuất (phải)
- Highlight các đoạn thay đổi (xanh = thêm mới, đỏ = xóa, vàng = sửa)
- Nút Accept All / Reject All / Accept từng đoạn
- Preview kết quả trước khi lưu

**4.4 Doc Browser**
- Tìm kiếm và xem tài liệu theo module/service
- Tab chuyển đổi giữa: API Spec / Module Description / Service Flow

**Acceptance Criteria:**
- UI load time ≤ 3 giây
- Responsive trên màn hình 1280px+
- Hỗ trợ dark mode
- Không yêu cầu login (MVP) – xác thực bằng API key trong config

**Độ ưu tiên:** P1 – High

---

## 5. Kiến Trúc Kỹ Thuật

### 5.1 Tech Stack

| Layer | Công nghệ | Lý do chọn |
|-------|-----------|------------|
| Frontend UI | Streamlit | Rapid development, Python-native, phù hợp MVP |
| Backend API | FastAPI (Python) | Async support, auto API docs, type hints |
| LLM | Gemini API (Google) | Chi phí thấp, context window lớn, tốt cho code |
| Code Parser | AST (Python built-in) + tree-sitter | Phân tích chính xác cấu trúc code |
| Doc Storage | File system (Git-based) | Không cần DB, dễ track thay đổi |
| Caching | Redis (optional) | Cache kết quả parse để tăng tốc |

### 5.2 Kiến Trúc Hệ Thống

```
┌─────────────────────────────────────────────────────────┐
│                  Streamlit UI (Frontend)                 │
│   Dashboard | Consistency Report | Doc Review | Browser  │
└───────────────────────┬─────────────────────────────────┘
                        │ HTTP/REST
┌───────────────────────▼─────────────────────────────────┐
│                 FastAPI Backend                          │
│  /scan   /check   /generate   /approve   /docs          │
└──────┬───────────────┬──────────────────┬───────────────┘
       │               │                  │
┌──────▼──────┐ ┌──────▼──────┐ ┌────────▼───────┐
│ Code Parser │ │Doc Comparator│ │  Gemini API    │
│  (AST/TS)  │ │   Engine     │ │  LLM Service   │
└──────┬──────┘ └──────┬──────┘ └────────┬───────┘
       │               │                  │
┌──────▼───────────────▼──────────────────▼───────┐
│              Repository File System               │
│         Source Code          Documentation        │
└──────────────────────────────────────────────────┘
```

### 5.3 Data Flow

1. User chọn repo path và nhấn "Scan"
2. Code Parser quét tất cả `.py` files, extract entities (routes, functions, classes)
3. Doc Comparator đọc tài liệu hiện tại và so sánh với entities vừa extract
4. Danh sách inconsistencies được gửi đến Gemini API cùng context code
5. Gemini generate nội dung tài liệu mới/cập nhật
6. Kết quả hiển thị trên UI, chờ user approve
7. Sau khi approve, file docs được ghi đè trên disk

### 5.4 Gemini API Prompt Strategy

- **System Prompt:** Định nghĩa vai trò (senior technical writer), format output (Markdown), ngôn ngữ (Tiếng Anh cho docs kỹ thuật)
- **Context Injection:** Đưa toàn bộ source code của module vào context
- **Few-shot Examples:** Cung cấp ví dụ về tài liệu tốt để guide output format
- **Temperature:** 0.3 (thấp để đảm bảo tính nhất quán và chính xác)

---

## 6. Yêu Cầu Phi Chức Năng (Non-Functional Requirements)

### 6.1 Hiệu Năng

| Chỉ số | Yêu cầu |
|--------|---------|
| Thời gian scan repo 10K LOC | ≤ 5 phút |
| Thời gian generate doc cho 1 module | ≤ 30 giây |
| UI response time | ≤ 3 giây |
| Concurrent users | Tối thiểu 10 users đồng thời |

### 6.2 Độ Tin Cậy

- Uptime: ≥ 99% trong giờ làm việc (8h–20h)
- Graceful error handling: Nếu Gemini API fail, hiển thị thông báo rõ ràng, không crash UI
- Data integrity: Không overwrite docs nếu chưa được user approve

### 6.3 Bảo Mật

- Gemini API key lưu trong environment variables, không hardcode
- Không gửi source code ra ngoài ngoài Gemini API (đã đánh giá rủi ro)
- Audit log cho mọi thay đổi tài liệu (ai approve, khi nào)

### 6.4 Khả Năng Mở Rộng

- Thiết kế module hóa để dễ thêm parser cho ngôn ngữ khác (Java, TypeScript)
- API backend có thể tích hợp với GitHub Actions về sau
- Config-driven: các quy tắc kiểm tra docs có thể customize qua file config

---

## 7. Kế Hoạch Phát Triển

### 7.1 Lộ Trình (Roadmap)

#### Phase 1 – MVP (Sprint 1–3, ~6 tuần)

| Sprint | Deliverables |
|--------|-------------|
| Sprint 1 (tuần 1–2) | Code Parser (Python AST), Doc Reader, Basic Consistency Checker |
| Sprint 2 (tuần 3–4) | Gemini API Integration, Doc Generator cho single module |
| Sprint 3 (tuần 5–6) | Streamlit UI (Dashboard + Doc Review), End-to-end flow |

#### Phase 2 – Enhancement (Sprint 4–6, ~6 tuần)

- CI/CD integration (auto-scan khi PR được merge)
- Hỗ trợ thêm ngôn ngữ: TypeScript/Node.js
- Email/Slack notification khi có inconsistency mới
- Analytics dashboard (tracking docs health over time)

#### Phase 3 – Scale (Sprint 7+)

- Multi-repo support
- Team collaboration features (comments, assignments)
- Integration với Confluence, Notion
- Custom doc templates

### 7.2 Ưu Tiên Tính Năng (MoSCoW)

| Must Have | Should Have | Could Have | Won't Have (MVP) |
|-----------|-------------|------------|-----------------|
| Doc Consistency Checker | Code → Doc Generator | Dark mode UI | Multi-repo dashboard |
| Auto Update Documentation | Version history | Slack notification | RBAC |
| Streamlit UI (Review/Approve) | Batch approve | Export PDF | CI/CD integration |
| FastAPI Backend | Config file | Keyword search | IDE plugin |

---

## 8. Điều Kiện Thành Công & KPIs

### 8.1 KPIs Chính

| KPI | Baseline (Hiện tại) | Target (Sau 3 tháng) |
|-----|---------------------|----------------------|
| Thời gian onboarding trung bình | 7–10 ngày | ≤ 3 ngày |
| Giờ support/tuần của senior | ~8 giờ/tuần | ≤ 3 giờ/tuần |
| % docs chính xác với codebase | ~40% (ước tính) | ≥ 85% |
| Số bug do hiểu sai docs | Cần baseline đo | Giảm 50% |
| Tỷ lệ hài lòng của nhân sự mới | Cần baseline khảo sát | ≥ 4/5 |

### 8.2 Điều Kiện Launch MVP

- [ ] Tất cả tính năng P0 hoạt động ổn định trên môi trường staging
- [ ] Đã test với ≥ 2 repo nội bộ thực tế
- [ ] Senior engineer review và confirm độ chính xác ≥ 80%
- [ ] UI test với ≥ 3 user mới (onboarding scenario)
- [ ] Không có critical bug còn mở

---

## 9. Rủi Ro & Biện Pháp Giảm Thiểu

| Rủi ro | Mức độ | Khả năng xảy ra | Biện pháp |
|--------|--------|-----------------|-----------|
| Gemini API generate sai thông tin kỹ thuật | Cao | Trung bình | Bắt buộc có human review trước khi apply |
| Chi phí Gemini API vượt ngân sách | Trung bình | Thấp | Caching, limit context size, batch requests |
| Senior không chịu review/approve | Cao | Trung bình | Thiết kế UX tối giản, tích hợp vào workflow sẵn có |
| Codebase phức tạp, parser không đọc được | Trung bình | Trung bình | Fallback sang regex-based parsing, manual override |
| Nhân sự mới vẫn prefer hỏi trực tiếp | Thấp | Cao | UX tốt, gamification nhẹ, quảng bá nội bộ |

---

## 10. Phụ Lục

### 10.1 Thuật Ngữ

| Thuật ngữ | Định nghĩa |
|-----------|-----------|
| Consistency Check | Quá trình so sánh docs với code để tìm sự không khớp |
| Doc Coverage | Tỷ lệ modules/APIs đã có tài liệu so với tổng số |
| Entity Extraction | Quá trình parse code để lấy ra thông tin cấu trúc (routes, functions, classes) |
| Human-in-the-loop | Quy trình yêu cầu con người approve trước khi AI thực hiện thay đổi |
| LOC | Lines of Code – số dòng code |

### 10.2 Tài Liệu Tham Khảo

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Google Gemini API](https://ai.google.dev/docs)
- [Python AST Module](https://docs.python.org/3/library/ast.html)

### 10.3 Lịch Sử Phiên Bản PRD

| Phiên bản | Ngày | Tác giả | Thay đổi |
|-----------|------|---------|---------|
| 0.1 | Tháng 4, 2026 | Product Team | Bản nháp đầu tiên |
| 1.0 | Tháng 4, 2026 | Product Team | Hoàn thiện MVP scope, thêm KPIs |

---

*Tài liệu này được soạn thảo bởi Product Management Team. Mọi thay đổi cần được approve bởi Product Owner và Tech Lead trước khi cập nhật.*

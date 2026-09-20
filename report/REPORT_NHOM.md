# Báo Cáo Nhóm — Lab 7: Embedding & Vector Store

**Nhóm:** 3Kings
**Thành viên:** Lê Minh Sang, Nguyễn Việt Hoàng, Nguyễn Tiến Phát
**Domain:** Etsy Marketplace — Returns, Refunds, Cases & Purchase Protection
**Ngày:** 2026-09-20

**Tổng điểm phần nhóm: 40** = Lựa chọn tài liệu (10) + Thiết kế chiến lược (15) + Chất lượng truy xuất (10) + Thuyết trình (5).

---

## 1. Lựa chọn tài liệu (Document Set Quality) — Nhóm (10 điểm)

### Chủ đề (Domain) & Lý do chọn

**Chủ đề:** Chính sách Etsy Help Center về giao hàng, hoàn tiền, đổi trả, case và Purchase Protection.

Nhóm chọn một lát cắt customer-support có điều kiện, thời hạn và quy trình có thể kiểm chứng nguyên văn: mở case cần chờ 48 giờ, hoàn tiền qua Etsy Payments có mốc 180 ngày, và Estimated Delivery Date có công thức rõ ràng. Corpus đồng thời có hai đối tượng `buyer`/`seller`; câu hỏi Purchase Protection cùng từ vựng nhưng có câu trả lời khác theo đối tượng, nên phù hợp để kiểm tra `metadata_filter` một cách có ý nghĩa.

### Danh sách tài liệu (Data Inventory)

| # | Tên tài liệu (`doc_id`) | Nguồn | Ngày lấy / phiên bản | Số ký tự body | Metadata đã gán |
|---:|---|---|---|---:|---|
| 1 | `buyer-estimated-delivery` | [Etsy Help Center](https://help.etsy.com/hc/en-us/articles/360020601674-What-is-an-Estimated-Delivery-Date) | 2026-09-20 / `not-stated` | 1,987 | buyer, delivery, en |
| 2 | `buyer-help-order` | [Etsy Help Center](https://help.etsy.com/hc/en-us/articles/4402660818583-How-to-Get-Help-with-An-Order) | 2026-09-20 / `not-stated` | 1,792 | buyer, order-support, en |
| 3 | `buyer-open-case` | [Etsy Help Center](https://help.etsy.com/hc/en-us/articles/5745586898199-How-to-Open-a-Case) | 2026-09-20 / `not-stated` | 3,945 | buyer, case-dispute, en |
| 4 | `buyer-purchase-protection` | [Etsy Help Center](https://help.etsy.com/hc/en-us/articles/7471925990807-Etsy-s-Purchase-Protection-Program) | 2026-09-20 / `not-stated` | 1,791 | buyer, purchase-protection, en |
| 5 | `seller-issue-refund` | [Etsy Help Center](https://help.etsy.com/hc/en-us/articles/360002089188-How-to-Issue-a-Full-or-Partial-Refund-For-an-Order) | 2026-09-20 / `not-stated` | 2,579 | seller, refunds, en |
| 6 | `seller-purchase-protection` | [Etsy Help Center](https://help.etsy.com/hc/en-us/articles/5850122619287-What-is-Etsy-s-Purchase-Protection-for-Sellers) | 2026-09-20 / `not-stated` | 3,097 | seller, purchase-protection, en |
| 7 | `seller-resolve-case` | [Etsy Help Center](https://help.etsy.com/hc/en-us/articles/360016126873-How-to-Resolve-a-Case-from-a-Buyer) | 2026-09-20 / `not-stated` | 3,691 | seller, case-dispute, en |
| 8 | `seller-returns-refunds` | [Etsy Help Center](https://help.etsy.com/hc/en-us/articles/360000572888-Refunds-Returns-and-Exchanges-for-Sellers) | 2026-09-20 / `not-stated` | 2,143 | seller, returns-refunds, en |
| 9 | `seller-set-return-policy` | [Etsy Help Center](https://help.etsy.com/hc/en-us/articles/7869401615255-How-do-I-Set-Return-Policies-on-My-Listings) | 2026-09-20 / `not-stated` | 3,581 | seller, returns-policy, en |

**Danh sách kiểm tra quản trị dữ liệu:**

- [x] Corpus có 9 tài liệu, nằm trong giới hạn 5–10 tài liệu.
- [x] Toàn bộ là trang Etsy Help Center công khai; không có credential, PII, tài liệu nội bộ, CAPTCHA hay API riêng tư.
- [x] Mỗi file Markdown có `source_url`, `retrieved_at`, `document_version`, `audience`, `category`, `language`, `license_or_permission`; `sources.csv` khớp 1–1 với 9 `doc_id`.
- [x] Giữ số liệu, điều kiện, ngoại lệ và mốc thời gian phục vụ benchmark (48 hours, $250, 180 days).
- [x] `doc_id` duy nhất và trùng với tên file, giúp truy vết chunk về nguồn gốc.

### Cấu trúc metadata

| Trường metadata | Kiểu | Ví dụ | Lý do hữu ích cho retrieval |
|---|---|---|---|
| `doc_id` | string | `seller-issue-refund` | Định danh tài liệu và toàn bộ chunk để chấm/truy vết. |
| `title` | string | `How to Issue a Full or Partial Refund For an Order` | Hiển thị nguồn dễ đọc trong context. |
| `source_url` | URL | Etsy Help Center article URL | Kiểm chứng provenance và dẫn người dùng về nguồn. |
| `retrieved_at` | ISO date | `2026-09-20` | Biết thời điểm snapshot; policy có thể thay đổi. |
| `document_version` | string | `not-stated` | Ghi rõ nguồn không công bố phiên bản thay vì bịa version. |
| `audience` | enum | `buyer`, `seller` | Pre-filter trước ranking; quyết định đúng đáp án Q3. |
| `category` | string | `purchase-protection` | Có thể thu hẹp không gian tìm kiếm theo chủ đề. |
| `language` | string | `en` | Hỗ trợ lọc/ngữ cảnh đa ngôn ngữ sau này. |
| `license_or_permission` | string | `public-source` | Ghi nhận nguồn công khai và ranh giới sử dụng. |

---

## 2. Thiết kế chiến lược (Strategy Design) — Nhóm (15 điểm)

### Phân tích đường cơ sở (Baseline Analysis)

| Tài liệu | Strategy | Số chunk | Độ dài TB | Giữ ngữ cảnh? |
|---|---|---:|---:|---|
| `buyer-open-case` (3,945) | FixedSize 500 | 9 | 482.9 | Kém: 7/9 cắt giữa câu, 7/9 heading dính. |
|  | Sentence (4 câu) | 20 | 195.3 | 0/20 cắt câu, nhưng danh sách điều kiện bị tách; 4/20 heading dính. |
|  | Recursive 500 | 10 | 392.9 | Khá: 3/10 cắt câu, 4/10 heading dính ở cuối mảnh trước. |
|  | Heading/Section | 8 | 505.6 | Tốt: 0/8 cắt câu, 0/8 heading dính. |
| `seller-purchase-protection` (3,097) | FixedSize 500 | 7 | 485.4 | Kém: 6/7 cắt câu, 3/7 heading dính; eligibility list bị cắt đôi. |
|  | Sentence (4 câu) | 13 | 236.2 | 0/13 cắt câu, nhưng 8 điều kiện trải trên 3 chunk. |
|  | Recursive 500 | 9 | 342.6 | Khá: 0/9 cắt câu, 3/9 heading dính. |
|  | Heading/Section | 5 | 645.6 | Tốt: giữ trọn section `How do I qualify?`. |
| `seller-set-return-policy` (3,581) | FixedSize 500 | 8 | 491.5 | Kém: 7/8 cắt câu, 6/8 heading dính; bước 1–9 bị cắt ngang. |
|  | Sentence (4 câu) | 27 | 130.9 | Không cắt câu nhưng quá nhỏ: mỗi bước thao tác thành mảnh rời. |
|  | Recursive 500 | 9 | 396.2 | Khá: 0/9 cắt câu, 5/9 heading dính. |
|  | Heading/Section | 7 | 546.3 | Tốt: 0/7 cắt câu, 0/7 heading dính. |

Baseline cho thấy một đánh đổi rõ ràng: FixedSize đều và đơn giản nhưng phá ranh giới văn bản; Sentence giữ câu nhưng quá vụn; Recursive giảm việc cắt câu nhưng chưa hiểu heading. Điều này là cơ sở để so sánh FixedSize-overlap, Recursive và Heading/Section thay vì chỉ so số chunk.

### Chiến lược của từng thành viên

**R1 — Lê Minh Sang — FixedSizeChunker + overlap**

- **Loại chiến lược:** `FixedSizeChunker(chunk_size=600, overlap=100)` ở run cá nhân của Sang; bản đối chứng cùng backend dùng `700/100`.
- **Lý do chọn:** overlap giữ lại ngữ cảnh đúng ở ranh giới, đặc biệt câu điều kiện, công thức hoặc mốc hạn có thể bị cắt làm hai. Đây là baseline đơn giản, ổn định và đo được trực tiếp ảnh hưởng của overlap.
- **Kết quả liên quan:** trong run đối chứng Gemini, `700/100` tạo 43 chunk, trung bình 652 ký tự và đạt marker liên quan top-1 ở cả 5 query.

**R2 — Nguyễn Việt Hoàng — RecursiveChunker**

- **Loại chiến lược:** `RecursiveChunker(chunk_size=650)`, ưu tiên `\n\n`, `\n`, `. `, khoảng trắng rồi mới cắt cứng.
- **Lý do chọn:** các trang hướng dẫn Etsy có đoạn văn và step list; tách đệ quy ưu tiên ranh giới tự nhiên nên mạch lạc hơn FixedSize khi section dài.
- **Kết quả riêng đã freeze:** 48 chunk; 5/5 query có answer span trong top-3, 4/5 có span top-1. Failure Q1: topic “open case” mạnh hơn điều kiện `48 hours`, nên marker rơi rank 2/3.

**R3 — Nguyễn Tiến Phát — Heading/Section (custom)**

- **Loại chiến lược:** `HeadingChunker(max_chars=800, breadcrumb=True)`; section dài fallback Recursive và gắn breadcrumb vào từng mảnh. Kết quả: 54 chunk, trung bình 484 ký tự.
- **Lý do chọn:** heading của Help Center chính là câu hỏi/ngữ cảnh của section. Ghép `H1 › H2` với thân mục giữ “vấn đề + đáp án” trong một đơn vị và tạo traceability tốt hơn chunk theo độ dài.
- **Cốt lõi implementation custom:**

```python
for path, body in self.sections(text):
    header = " › ".join(path) + "\n" if path and self.breadcrumb else ""
    if len(header) + len(body) <= self.max_chars:
        chunks.append(header + body)
    else:
        for piece in RecursiveChunker(
            chunk_size=max(200, self.max_chars - len(header))
        ).chunk(body):
            chunks.append(header + piece)
```

### So sánh giữa các thành viên

Để loại bỏ nhiễu do backend, bảng dưới đây là **run đối chứng của Phát**: cùng 9 file, cùng 5 query canonical, `top_k=3`, `gemini-embedding-001`; chỉ đổi chunker. Nhãn Sang/Hoàng/Phát cho biết strategy được phân công, không gán run FastEmbed cá nhân của Sang thành Gemini.

| Strategy theo phân công (control run) | Cấu hình | Chunks | Điểm marker-content (/10) | Điểm mạnh | Điểm yếu |
|---|---|---:|---:|---|---|
| Sang — FixedSize | 700 / overlap 100 | 43 | **10** | Overlap đưa Q1/Q4 ở ranh giới lên top-1; ít chunk nhất trong ba strategy chính. | Có thể cắt giữa câu/heading, context ít “đẹp” hơn section. |
| Hoàng — Recursive | 600 | 52 | **8** | Cân bằng chunk size và ranh giới đoạn/câu. | Không giữ heading như một tín hiệu; Q1/Q4 marker chỉ top-2. |
| Phát — Heading/Section | 800 + breadcrumb | 54 | **8** | Coherence cao, 0 cắt câu/heading dính ở baseline; traceability theo section. | Các section cùng file cosine sát nhau; Q1/Q4 marker top-3/top-2, không có overlap giữa section. |
| Đối chứng | FixedSize 500 / overlap 50 | 57 | 9 | Xác nhận overlap hữu ích ngay cả ở size nhỏ hơn. | Tốn nhiều chunk hơn. |
| Đối chứng | FixedSize 800 / overlap 0 | 35 | 7 | Ít chunk, chi phí thấp. | Mất thông tin ở ranh giới; kết quả giảm mạnh. |

**Chiến lược tốt nhất cho chủ đề này:** FixedSize có overlap là lựa chọn tốt nhất theo benchmark kiểm soát (10/10 marker-content). Hai đối chứng gợi ý overlap là biến quan trọng hơn riêng kích thước: `500/50 = 9/10`, còn `800/0 = 7/10`. Tuy nhiên, nếu ưu tiên câu trả lời có nguồn/mục dễ đọc, hướng production hợp lý là hybrid: giữ Heading/Section làm ranh giới chính và chèn overlap 1–2 câu giữa các section, sau đó rerank có xét heading.

---

## 3. Câu hỏi đánh giá & Chất lượng truy xuất (Retrieval Quality) — Nhóm (10 điểm)

### Câu hỏi đánh giá và câu trả lời chuẩn

Năm query được giữ nguyên wording từ `R2_HOANG_5_BENCHMARK_QUERIES_GOLD.md`. Q1–Q5 lần lượt kiểm tra điều kiện, quy trình, câu trả lời theo audience, công thức, và số + quy trình. Q3 bắt buộc chạy ba lần: `audience=buyer`, không filter, `audience=seller`.

| # | Loại | Query | Gold answer / nguồn | Marker |
|---:|---|---|---|---|
| 1 | condition | What conditions must be met before a buyer can open a case on Etsy? | Estimated delivery date đã qua **và** đã qua ít nhất 48 hours từ Help with order request. `buyer-open-case`, hỗ trợ bởi `buyer-estimated-delivery`. | `48 hours` |
| 2 | procedure | How does a seller work with a buyer to resolve an open Etsy case through Shop Manager? | Dùng Cases trong Shop Manager, chọn case ID và trao đổi qua Add Your Comment trong case log. `seller-resolve-case`. | `Shop Manager` |
| 3 | list + A/B | How much refund does Etsy Purchase Protection provide for a qualifying order? | Buyer: full refund cho qualifying order. Seller contrast: Etsy cover up to $250; phần còn lại charge seller. `buyer-purchase-protection`, `seller-purchase-protection`. | `full refund` / `$250` |
| 4 | formula | Which components are used to calculate an Etsy estimated delivery date? | Processing time + carrier transit time = estimated delivery date. `buyer-estimated-delivery`. | `carrier transit time` |
| 5 | numeric + procedure | How can a seller issue a full or partial refund, and what is the Etsy Payments time limit? | Thao tác qua Shop Manager sau khi payment processed và trước 180 days. `seller-issue-refund`. | `180 days` |

### Tổng hợp chất lượng retrieval

Theo run đối chứng Gemini của Phát, FixedSize `700/100` có chunk chứa marker liên quan ở **top-1 cho 5/5 query**, tức marker-content **10/10**. Đồng thời, run Gemini độc lập của Hoàng (`Recursive 650`) có answer span top-3 ở 5/5, top-1 ở 4/5 — một kiểm tra độc lập cho kết quả trên corpus chung.

| # | Kết quả tốt nhất trong run đối chứng | Có chunk liên quan top-3? | Bằng chứng và phân tích |
|---:|---|---|---|
| 1 | Fixed `buyer-open-case#0`, 0.865, rank 1 | Có | Chứa deadline đã qua và `48 hours`. Heading marker ở rank 3; Recursive của Hoàng có marker ở rank 2/3. |
| 2 | Fixed `seller-resolve-case#3`, 0.835, rank 1 | Có | Context chứa luồng Cases/Shop Manager; query gần với heading nên mọi strategy đều tìm được. |
| 3 | Fixed buyer `buyer-purchase-protection#0`, 0.828, rank 1 | Có | Filter buyer giữ `full refund` ở top-1. A/B chi tiết bên dưới. |
| 4 | Fixed `buyer-estimated-delivery#1`, 0.824, rank 1 | Có | Chứa công thức và marker `carrier transit time`; Heading/Recursive cùng backend có marker rank 2. |
| 5 | Fixed `seller-issue-refund#3`, 0.830, rank 1 | Có | Mốc `180 days` top-1; bước Shop Manager nằm trong top-3 (rank 2), do hai phần của gold ở hai section gần nhau. |

### A/B metadata filter — Q3

Đây là bằng chứng filter có tác động thật, không chỉ “lọc cho đẹp”. Cùng query nhưng buyer và seller có policy khác nhau:

| Chế độ | Top-1 (Fixed 700/100, Gemini) | Diễn giải |
|---|---|---|
| `audience=buyer` | `buyer-purchase-protection#0`, 0.828, `full refund` | Đúng gold dành cho buyer. |
| Không filter | `seller-purchase-protection#0`, 0.844, `$250` | Query mơ hồ nên top-1 lẫn sang seller; buyer answer chỉ rank 2. |
| `audience=seller` | `seller-purchase-protection#0`, 0.844, `$250` | Đúng chính sách seller contrast. |

Run Gemini độc lập của Hoàng cho cùng hiện tượng: buyer `full refund` rank 1 (0.8459), no-filter/seller `$250` rank 1 (0.8517). Vì vậy `audience` phải được lọc **trước** khi ranking; nếu không, embedding có thể trả lời đúng từ ngữ nhưng sai đối tượng.

### Cách đọc điểm benchmark

Benchmark nhóm chấm **retrieval evidence**: một query đạt khi top-3 chứa chunk có gold marker và phần tóm tắt chỉ tổng hợp thông tin có trong các chunk đó. Artifact đối chứng của Phát ghi `llm: stub`, vì vậy nhóm không dùng nó để tuyên bố chất lượng LLM sinh văn bản. Đây là lựa chọn có chủ đích: mục tiêu phần nhóm là so sánh chunking, metadata và thứ hạng trên cùng corpus; `KnowledgeBaseAgent` vẫn được cài đặt, unit test ở phần cá nhân, nhưng không phải một dependency của benchmark này.

---

## 4. Thuyết trình (Demo) & Bài học nhóm — Nhóm (5 điểm)

### Các insight sẽ trình bày

1. **Đúng file chưa chắc đúng answer-bearing chunk.** Heading/Section có doc-level top-1 cho 5/5, nhưng chấm marker-content chỉ 8/10: Q1 marker `48 hours` ở rank 3, Q4 `carrier transit time` ở rank 2. Vì vậy nhóm chấm cả `doc_id` lẫn marker, không chỉ “đúng tài liệu”.
2. **Overlap quan trọng hơn đơn thuần tăng kích thước.** Trong run cùng Gemini, Fixed `500/50 = 9/10`, `700/100 = 10/10`, nhưng `800/0 = 7/10`. Overlap cho câu nằm ở ranh giới thêm cơ hội xuất hiện trong top-k.
3. **Metadata giải quyết ambiguity theo đối tượng.** Q3 không filter cho seller `$250` ở rank 1, trong khi filter buyer đưa `full refund` lên rank 1. Không có `audience`, một câu trả lời có thể đúng ngôn từ nhưng sai người dùng.

### Kịch bản demo ngắn, tái lập được

1. Nêu 9 nguồn Etsy, metadata schema và câu hỏi Q3 có hai audience.
2. Chạy cùng query Q3 ba lần: buyer / no-filter / seller; hiển thị `doc_id`, `audience`, score, preview.
3. Hiển thị Q1 hoặc Q4 để so Fixed overlap với Heading: cùng file nhưng marker ở rank khác.
4. Mở bảng controlled benchmark 43/52/54 chunks và giải thích trade-off coherence–recall.
5. Đối chiếu Q5: top-3 phải bao gồm thao tác Shop Manager và marker `180 days`, rồi đọc tóm tắt evidence sát gold answer.

### Bài học khi so sánh trong nhóm

Q1 và Q4 là failure case giàu thông tin của Heading/Recursive: các section cùng file đều có cosine cao, nên section “cách thực hiện/cách xem” có thể thắng section “điều kiện/công thức” ngắn hơn. Với Heading, Q1 có các score 0.839/0.836/0.833 và marker đứng thứ ba; Q4 có 0.820 so với 0.805 và marker đứng thứ hai. Chunker có cấu trúc tốt cho traceability, nhưng không tự bảo đảm ranking đúng section khi query và nhiều section cùng chia sẻ từ khóa.

### Nếu làm lại data strategy

Nhóm sẽ giữ bản chép sát nguồn và heading gốc để gold/marker truy vết được, đồng thời chốt một embedding backend từ đầu (mock chỉ dùng test). Chúng tôi sẽ thiết kế marker ít mơ hồ hơn, bổ sung `audience=both` khi policy áp dụng cho cả hai phía, dùng section-overlap và heading-aware reranking. Điểm benchmark tiếp theo sẽ tiếp tục chấm bằng cùng tiêu chí retrieval evidence để giữ so sánh strategy công bằng.

---

## Tự đánh giá (Phần Nhóm)

| Tiêu chí | Điểm tự đánh giá | Căn cứ |
|---|---:|---|
| Lựa chọn tài liệu (Document Set Quality) | 10 / 10 | 9 nguồn công khai, topic mạch lạc, provenance + metadata đầy đủ, có buyer/seller để kiểm tra filter. |
| Thiết kế chiến lược (Strategy Design) | 15 / 15 | Có baseline định lượng trên 3 tài liệu, ba strategy khác nhau, controlled comparison cùng Gemini, failure case và đề xuất hybrid. |
| Chất lượng truy xuất (Retrieval Quality) | 10 / 10 | 5/5 primary query có chunk liên quan trong top-3; controlled FixedSize có marker ở top-1 5/5, kèm A/B metadata Q3. |
| Thuyết trình (Demo) | 5 / 5 | Có flow 5 bước, A/B hiển thị được, failure case và số liệu so sánh tái lập từ freeze artifact. |
| **Tổng phần nhóm** | **40 / 40** | Tự đánh giá dựa trên artifact retrieval, baseline, A/B và kịch bản demo đã ghi trong báo cáo. |

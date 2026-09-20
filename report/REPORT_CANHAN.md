<<<<<<< HEAD
# Báo Cáo Cá Nhân — Lab 7: Embedding & Vector Store (K4-L3B)

**Họ tên:** Nguyễn Việt Hoàng  
**Vai trò:** R2 — Benchmark  
**Nhóm:** Sang — Hoàng — Phát  
**Domain:** Etsy Marketplace — Returns, Refunds, Cases & Purchase Protection  
**Ngày:** 2026-09-20

## 1. Warm-up

Cosine similarity đo độ gần nhau về hướng giữa hai vector. Hai câu có thể dùng từ khác nhau nhưng cùng ý nghĩa vẫn có thể có cosine cao nếu embedding mã hóa được ngữ nghĩa. Cosine phù hợp với text embedding hơn Euclidean vì ít phụ thuộc vào độ dài vector.

Với văn bản 10.000 ký tự, chunk_size=500:

- overlap=50: ceil((10.000 - 50) / (500 - 50)) = 23 chunks.
- overlap=100: ceil((10.000 - 100) / (500 - 100)) = 25 chunks.

Overlap lớn hơn giữ thêm ngữ cảnh ở ranh giới chunk, nhưng làm tăng số chunk và chi phí embedding.

Đã kiểm tra lại bằng `FixedSizeChunker`: `chunk_size=500, overlap=50` cho 23 chunks; tăng overlap lên 100 cho 25 chunks.

## 2. My Approach

### RecursiveChunker

Chiến lược cá nhân của Hoàng là RecursiveChunker với chunk_size=650. Thứ tự separator là đoạn văn, dòng, câu, khoảng trắng và cuối cùng là cắt cứng. Base case xử lý text rỗng và separators rỗng; các mảnh nhỏ liền kề được gom trước khi hạ xuống separator nhỏ hơn.

Điểm mạnh là giữ được đoạn và câu trong các bài hướng dẫn Etsy, trong khi section dài vẫn được chia nhỏ. Điểm yếu là không hiểu ngữ nghĩa của heading; một đoạn chứa đáp án vẫn có thể không đứng top-1 dù dùng embedding ngữ nghĩa.

### EmbeddingStore

EmbeddingStore nạp từng Document/chunk, sao chép metadata và bảo đảm metadata có doc_id. Search dùng cosine similarity, search_with_filter lọc metadata trước khi xếp hạng, còn delete_document xóa toàn bộ chunk của doc_id tương ứng.

### KnowledgeBaseAgent

Agent lấy top-k chunk, dựng context có đánh số, doc_id và source_url để truy vết, sau đó gửi prompt yêu cầu LLM chỉ dùng context. Khi không có context, prompt yêu cầu nói rõ thông tin không có trong knowledge base.

## 3. Core Implementation

Đã tạo lại môi trường .venv sạch và chạy đúng lệnh pytest của bài:

    python -m pytest tests/ -v
    42 passed, 1 warning

Kết quả: **42/42**. Warning chỉ liên quan đến quyền ghi cache của pytest, không làm fail test.

## 4. Similarity Predictions

Các điểm dưới đây dùng MockEmbedder, nên chỉ đánh giá cơ chế cosine chứ không đại diện cho semantic embedding thật.

| # | Cặp câu | Dự đoán | Điểm thực tế |
|---:|---|---|---:|
| 1 | Etsy may provide a full refund for a qualifying order. / A qualifying Etsy order can receive a complete refund. | Cao | 0,2028 |
| 2 | Processing time plus carrier transit time determines delivery. / The estimated delivery date depends on preparation and shipping transit. | Cao | 0,1501 |
| 3 | A seller can issue a refund through Shop Manager. / A buyer can open a case after contacting the seller. | Thấp | -0,0751 |
| 4 | The buyer must wait 48 hours after contacting the seller. / A seller should respond to a Help with Order request within 48 hours. | Trung bình | 0,1203 |
| 5 | A case may be closed after a full refund. / A seller can set a return policy for physical listings. | Thấp | -0,0686 |

MockEmbedder là hash-based deterministic embedder, không hiểu nghĩa câu; nó chỉ được dùng trong phần Similarity Predictions. Benchmark retrieval dưới đây dùng Gemini Embeddings API với model `gemini-embedding-001`.

## 5. Competition Results

Chiến lược: **RecursiveChunker(chunk_size=650)**  
Embedding: **Gemini API — gemini-embedding-001**  
Tổng số chunk: **48**

| # | Query | Metadata filter | Top-3 retrieval: rank — chunk — score — audience | Gold span / kết quả |
|---:|---|---|---|---|
| 1 | What conditions must be met before a buyer can open a case on Etsy? | `audience=buyer` | 1 — `buyer-open-case#2` — 0.8552 — buyer<br>2 — `buyer-open-case#0` — 0.8098 — buyer<br>3 — `buyer-open-case#3` — 0.7968 — buyer | Marker `48 hours` ở `buyer-open-case#0/#3` (rank 2/3); gold doc ✓, answer span ✓ |
| 2 | How does a seller work with a buyer to resolve an open Etsy case through Shop Manager? | `audience=seller` | 1 — `seller-resolve-case#4` — 0.8517 — seller<br>2 — `seller-purchase-protection#5` — 0.8188 — seller<br>3 — `seller-resolve-case#3` — 0.8157 — seller | Quy trình ở `seller-resolve-case#4` (rank 1), marker `Shop Manager`; gold doc ✓, answer span ✓ |
| 3 | How much refund does Etsy Purchase Protection provide for a qualifying order? | `audience=buyer` | 1 — `buyer-purchase-protection#0` — 0.8459 — buyer<br>2 — `buyer-open-case#4` — 0.7751 — buyer<br>3 — `buyer-purchase-protection#2` — 0.7450 — buyer | Marker `full refund` ở `buyer-purchase-protection#0/#4` (rank 1/2); gold doc ✓, answer span ✓ |
| 4 | Which components are used to calculate an Etsy estimated delivery date? | `audience=buyer` | 1 — `buyer-estimated-delivery#1` — 0.8331 — buyer<br>2 — `buyer-estimated-delivery#2` — 0.7844 — buyer<br>3 — `buyer-estimated-delivery#0` — 0.7711 — buyer | Công thức ở `buyer-estimated-delivery#1` (rank 1), marker `carrier transit time`; gold doc ✓, answer span ✓ |
| 5 | How can a seller issue a full or partial refund, and what is the Etsy Payments time limit? | `audience=seller` | 1 — `seller-issue-refund#3` — 0.8098 — seller<br>2 — `seller-issue-refund#0` — 0.7966 — seller<br>3 — `seller-issue-refund#1` — 0.7717 — seller | Mốc `180 days` ở `seller-issue-refund#3` (rank 1); gold doc ✓, answer span ✓ |

Kết quả: **5/5 câu có answer span trong top-3** và **4/5 câu có answer span ở top-1**. Q1 là trường hợp duy nhất marker không ở top-1; vì vậy vẫn cần chấm ở mức nội dung thay vì chỉ kiểm tra doc_id.

### A/B metadata filter

Query Q3 là câu hỏi mơ hồ về đối tượng và được chạy theo ba trạng thái:

| Chế độ chạy | Top-3 (rank — chunk — score — audience) | Đọc kết quả |
|---|---|---|
| `audience=buyer` | 1 — `buyer-purchase-protection#0` — 0.8459 — buyer<br>2 — `buyer-open-case#4` — 0.7751 — buyer<br>3 — `buyer-purchase-protection#2` — 0.7450 — buyer | Có marker `full refund`; đúng gold buyer |
| Không filter | 1 — `seller-purchase-protection#0` — 0.8517 — seller<br>2 — `buyer-purchase-protection#0` — 0.8459 — buyer<br>3 — `seller-resolve-case#2` — 0.8251 — seller | Top-1 bị lẫn sang seller; retrieval trộn buyer/seller dù buyer answer vẫn xuất hiện ở rank 2 |
| `audience=seller` | 1 — `seller-purchase-protection#0` — 0.8517 — seller<br>2 — `seller-resolve-case#2` — 0.8251 — seller<br>3 — `seller-purchase-protection#2` — 0.7849 — seller | Đúng tập seller; `seller-purchase-protection#0` chứa mức `up to $250`, khác gold buyer `full refund` |

Kết quả chứng minh pre-filter theo audience giúp chọn đúng đáp án theo đối tượng; nếu không lọc, retrieval có thể trộn hai chính sách cùng chủ đề Purchase Protection.

### Failure analysis

Failure thật của RecursiveChunker với Gemini là Q1: top-1 `buyer-open-case#2` nói về việc cần tài khoản và các loại case, trong khi điều kiện thời gian chứa marker `48 hours` chỉ đứng ở top-2/top-3. Nguyên nhân là các chunk đều cùng chủ đề mở case và embedding ưu tiên độ tương đồng chủ đề hơn cụm thời hạn cụ thể. Cải thiện phù hợp là reranking theo marker/heading, hybrid semantic + keyword search hoặc điều chỉnh cách cắt section điều kiện.

Q3 cho thấy cần phân biệt `gold_doc_in_top3` với `answer_span_in_top3`: ở lần chạy `audience=seller`, gold buyer document cố ý không xuất hiện (`gold_doc_in_top3=False`), nhưng marker `full refund` vẫn xuất hiện trong `seller-resolve-case#2` vì chunk này nhắc tới kết quả hoàn tiền cho buyer. Gold seller thực sự cần đối chiếu là `seller-purchase-protection#0` với mức `up to $250`.

## 6. Data ownership của R2

Ba tài liệu Hoàng phụ trách:

1. buyer-open-case — buyer — case-dispute
2. seller-resolve-case — seller — case-dispute
3. buyer-estimated-delivery — buyer — delivery

Các file đã được clean, có frontmatter, source_url, retrieved_at, document_version, audience, category và license_or_permission. Sang cần dùng cùng corpus 9 file và cùng bộ 5 query khi tổng hợp kết quả nhóm.
=======
# Báo Cáo Cá Nhân — Lab 7: Embedding & Vector Store

**Họ tên:** [Tên sinh viên]
**Nhóm:** [Tên nhóm]
**Ngày:** [Ngày nộp]

> **Nộp 1 bản / sinh viên.** Phần nhóm (lựa chọn tài liệu, thiết kế chiến lược, bộ câu hỏi đánh giá, demo) nộp chung 1 bản trong `REPORT_NHOM.md`. Chi tiết thang điểm: `docs/SCORING.md`.

**Tổng điểm phần cá nhân: 60** = Khởi động (5) + Hướng tiếp cận (10) + Hoàn thiện code (30) + Dự đoán độ tương tự (5) + Kết quả truy xuất của tôi (10).

---

## 1. Khởi động (Warm-up) — Cá nhân (5 điểm)

### Độ tương tự Cosine (Cosine Similarity) (Bài tập 1.1)

**Độ tương tự cosine cao (High cosine similarity) nghĩa là gì?**
> *Viết 1-2 câu:*

**Ví dụ có độ tương tự CAO:**
- Câu A:
- Câu B:
- Tại sao tương đồng:

**Ví dụ có độ tương tự THẤP:**
- Câu A:
- Câu B:
- Tại sao khác:

**Tại sao độ tương tự cosine (cosine similarity) được ưu tiên hơn khoảng cách Euclid (Euclidean distance) cho text embeddings?**
> *Viết 1-2 câu:*

### Bài toán tính toán Chunking (Bài tập 1.2)

**Tài liệu 10,000 ký tự, chunk_size=500, overlap=50. Bao nhiêu chunks?**
> *Trình bày phép tính:*
> *Đáp án:*

**Nếu độ chồng chéo (overlap) tăng lên 100, số lượng chunk thay đổi thế nào? Tại sao muốn độ chồng chéo nhiều hơn?**
> *Viết 1-2 câu:*

---

## 2. Hướng tiếp cận của tôi (My Approach) — Cá nhân (10 điểm)

Giải thích cách tiếp cận của bạn khi lập trình (implement) các phần chính trong gói `src`.

### Các hàm chia nhỏ (Chunking Functions)

**`SentenceChunker.chunk`** — hướng tiếp cận:
> *Viết 2-3 câu: dùng biểu thức chính quy (regex) gì để phát hiện câu? Xử lý trường hợp ngoại lệ (edge case) nào?*

**`RecursiveChunker.chunk` / `_split`** — hướng tiếp cận:
> *Viết 2-3 câu: thuật toán hoạt động thế nào? Base case (trường hợp cơ sở) là gì?*

### Lớp EmbeddingStore

**`add_documents` + `search`** — hướng tiếp cận:
> *Viết 2-3 câu: lưu trữ thế nào? Tính độ tương tự ra sao?*

**`search_with_filter` + `delete_document`** — hướng tiếp cận:
> *Viết 2-3 câu: lọc (filter) trước hay sau? Xóa bằng cách nào?*

### Tác tử KnowledgeBaseAgent

**`answer`** — hướng tiếp cận:
> *Viết 2-3 câu: cấu trúc prompt? Cách đưa ngữ cảnh (inject context) vào thế nào?*

---

## 3. Hoàn thiện code (Core Implementation) — Cá nhân (30 điểm)

Vượt qua bộ kiểm thử là điều kiện tính điểm phần này.

### Kết Quả Kiểm Thử (Test Results)

```
# Dán kết quả (output) của: pytest tests/ -v
```

**Số lượng bài test vượt qua (pass):** __ / 42

---

## 4. Dự đoán độ tương tự (Similarity Predictions) — Cá nhân (5 điểm)

| Cặp | Câu A | Câu B | Dự đoán | Điểm thực tế | Đúng? |
|------|-----------|-----------|---------|--------------|-------|
| 1 | | | cao / thấp | | |
| 2 | | | cao / thấp | | |
| 3 | | | cao / thấp | | |
| 4 | | | cao / thấp | | |
| 5 | | | cao / thấp | | |

**Kết quả nào bất ngờ nhất? Điều này nói gì về cách embeddings biểu diễn ý nghĩa?**
> *Viết 2-3 câu:*

---

## 5. Kết quả truy xuất của tôi (Competition Results) — Cá nhân (10 điểm)

Chạy **5 câu hỏi đánh giá của nhóm** trên mã nguồn cá nhân của bạn trong gói `src`. **5 câu hỏi này phải trùng với các thành viên cùng nhóm** (xem `REPORT_NHOM.md`).

| # | Câu hỏi (Query) | Top-1 Chunk truy xuất được (tóm tắt) | Điểm Score | Có liên quan không? (Relevant) | Câu trả lời của Agent (tóm tắt) |
|---|-------|--------------------------------|-------|-----------|------------------------|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |

**Bao nhiêu câu hỏi trả về chunk có liên quan trong top-3?** __ / 5

**Điều hay nhất tôi học được từ thành viên khác / nhóm khác (qua demo):**
> *Viết 2-3 câu:*

---

## Tự Đánh Giá (Phần Cá Nhân)

| Tiêu chí | Điểm tự đánh giá |
|----------|-------------------|
| Khởi động (Warm-up) | / 5 |
| Hướng tiếp cận của tôi (My Approach) | / 10 |
| Hoàn thiện code (Core Implementation — tests) | / 30 |
| Dự đoán độ tương tự (Similarity Predictions) | / 5 |
| Kết quả truy xuất của tôi (Competition Results) | / 10 |
| **Tổng phần cá nhân** | **/ 60** |
>>>>>>> e05a3a610f763dc292c285e48aff812c6b564639

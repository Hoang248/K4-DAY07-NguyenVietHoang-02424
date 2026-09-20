# Hoàng → Sang — Bàn giao dữ liệu trước khi freeze bài

**Vai trò:** R2 — Benchmark  
**Strategy:** `RecursiveChunker`  
**Corpus:** 9 file trong `data/etsy-policies/`  
**Bộ query:** đúng 5 query canonical trong `R2_HOANG_5_BENCHMARK_QUERIES_GOLD.md`

## 1. Các file Hoàng gửi Sang

| File | Mục đích | Trạng thái |
|---|---|---|
| `report/REPORT_CANHAN.md` | Báo cáo cá nhân của Hoàng, mục 5 đã có top-3 Gemini | Hoàn tất |
| `report/REPORT_NHOM.md` | Bản report nhóm hiện tại để Sang trích/đối chiếu; không tự ghi đè | Gửi kèm |
| `report/R2_HOANG_5_BENCHMARK_QUERIES_GOLD.md` | 5 query, gold answer, source, marker và yêu cầu A/B | Hoàn tất |
| `bench.py` | Code benchmark, có `--embedding gemini` và cache API | Hoàn tất |
| `ket_qua_benchmark.txt` | Output benchmark chính thức của Hoàng bằng Gemini | Hoàn tất |
| `ket_qua_pytest.txt` | Output `pytest tests/ -v` | 42/42 passed |
| `data/etsy-policies/*.md` + `sources.csv` | Corpus chung 9 file | Đã dùng đúng corpus |

## 2. Hoàng đã đáp ứng yêu cầu CP6

- `REPORT_CANHAN.md` đã có bảng top-3 cho cả 5 query.
- `bench.py` chạy trên đúng 9 file Markdown và đúng 5 query canonical.
- Backend đã dùng: `Gemini API — gemini-embedding-001`.
- `RecursiveChunker`: `chunk_size=650`.
- Separator priority giữ nguyên:

  ```text
  ["\n\n", "\n", ". ", " ", ""]
  ```

- Tổng số chunk: `48`.
- Answer span trong top-3: `5/5`.
- Answer span ở top-1: `4/5`.
- `pytest`: `42 passed, 1 warning`; warning chỉ là `PytestCacheWarning` do quyền ghi `.pytest_cache`.

## 3. Benchmark score của Hoàng

| Query | Top-1 | Gold marker | Answer span top-3 |
|---:|---|---|---|
| Q1 | `buyer-open-case#2`, `0.8552` | `48 hours` ở rank 2/3 | Có |
| Q2 | `seller-resolve-case#4`, `0.8517` | `Shop Manager` ở rank 1 | Có |
| Q3 | `buyer-purchase-protection#0`, `0.8459` | `full refund` ở rank 1/2 | Có |
| Q4 | `buyer-estimated-delivery#1`, `0.8331` | `carrier transit time` ở rank 1 | Có |
| Q5 | `seller-issue-refund#3`, `0.8098` | `180 days` ở rank 1 | Có |

Top-3 đầy đủ của cả 5 query nằm trong `ket_qua_benchmark.txt` và `report/REPORT_CANHAN.md`, gồm score, chunk ID, `doc_id`, audience và preview.

## 4. Q3 — A/B metadata filter

**Query:** `How much refund does Etsy Purchase Protection provide for a qualifying order?`  
**Buyer gold marker:** `full refund`  
**Seller contrast marker:** `$250`

| Lượt chạy | Rank | Score | Chunk ID | `doc_id` | Audience | Preview | Marker |
|---|---:|---:|---|---|---|---|---|
| `audience=buyer` | 1 | 0.8459 | `buyer-purchase-protection#0` | `buyer-purchase-protection` | buyer | Etsy’s Purchase Protection program provides a full refund for qualifying orders... | `full refund` ✓ |
| `audience=buyer` | 2 | 0.7751 | `buyer-open-case#4` | `buyer-open-case` | buyer | Explain why you are contacting the seller and your desired resolution... | `full refund` ✓ |
| `audience=buyer` | 3 | 0.7450 | `buyer-purchase-protection#2` | `buyer-purchase-protection` | buyer | Items that arrive late due to forces outside the seller’s control... | — |
| Không filter | 1 | 0.8517 | `seller-purchase-protection#0` | `seller-purchase-protection` | seller | Etsy covers up to $250 of a refund... | `$250` ✓ |
| Không filter | 2 | 0.8459 | `buyer-purchase-protection#0` | `buyer-purchase-protection` | buyer | Etsy’s Purchase Protection program provides a full refund... | `full refund` ✓ |
| Không filter | 3 | 0.8251 | `seller-resolve-case#2` | `seller-resolve-case` | seller | If the order is eligible for Purchase Protection, the buyer receives a full refund... | `full refund` ✓* |
| `audience=seller` | 1 | 0.8517 | `seller-purchase-protection#0` | `seller-purchase-protection` | seller | Etsy covers up to $250 of a refund... | `$250` ✓ |
| `audience=seller` | 2 | 0.8251 | `seller-resolve-case#2` | `seller-resolve-case` | seller | The buyer receives a full refund; Etsy covers up to $250... | `full refund` ✓* |
| `audience=seller` | 3 | 0.7849 | `seller-purchase-protection#2` | `seller-purchase-protection` | seller | Buyers are responsible for customs duties and import duties... | — |

`✓*` là marker xuất hiện trong một chunk seller có nhắc tới buyer full refund; gold seller cần đối chiếu theo nội dung seller, trong đó mức bảo vệ chính là `up to $250`.

**Kết luận A/B:** filter `buyer` đưa tài liệu buyer lên đúng top-1. Không filter đưa seller policy lên top-1 dù câu hỏi đang cần buyer answer. Filter `seller` đưa seller policy lên top-1 và cho thấy đáp án đối tượng seller khác với buyer.

## 5. RecursiveChunker — rationale và failure/observation

**Rationale:** RecursiveChunker ưu tiên cắt theo đoạn văn, dòng, câu, khoảng trắng rồi mới cắt cứng. Cách này giữ được các bước hướng dẫn và điều kiện liên quan trong cùng chunk, phù hợp với corpus chính sách Etsy.

**Failure case thật:** Q1 có top-1 là `buyer-open-case#2`, nói về yêu cầu tài khoản và các loại case. Điều kiện thời gian chứa marker `48 hours` chỉ nằm ở `buyer-open-case#0` và `buyer-open-case#3` tại top-2/top-3. Nguyên nhân là các chunk đều cùng chủ đề mở case; embedding ưu tiên tương đồng chủ đề hơn mốc thời hạn cụ thể.

**Cải thiện đề xuất:** reranking theo marker/heading, kết hợp semantic search với keyword search, hoặc điều chỉnh cách tách section điều kiện.

**Observation:** Q3 cho thấy phải chấm cả `gold_doc_in_top3` và `answer_span_in_top3`. Một chunk seller có thể chứa cụm `full refund` nhưng không phải gold buyer document; không được chỉ nhìn marker hoặc chỉ nhìn tên tài liệu.

## 6. Việc Sang cần lưu ý khi freeze

`REPORT_NHOM.md` hiện tại vẫn chứa bảng so sánh cũ bằng **TF-IDF lexical**, trong khi benchmark cá nhân mới của Hoàng dùng **Gemini**. Nhóm cần chốt một trong hai phương án:

1. Giữ lexical làm backend chung: Hoàng giữ riêng kết quả Gemini như thử nghiệm bổ sung và report nhóm dùng số liệu lexical thống nhất.
2. Chuyển cả nhóm sang Gemini: Sang và Phát phải chạy lại strategy của mình bằng cùng backend Gemini trước khi freeze bảng so sánh.

Không trộn score lexical của Sang/Phát với score Gemini của Hoàng trong cùng bảng so sánh chiến lược.

## Tin nhắn có thể gửi vào nhóm

> Hoàng gửi Sang các file: `REPORT_CANHAN.md`, bản `REPORT_NHOM.md` hiện tại để đối chiếu, `R2_HOANG_5_BENCHMARK_QUERIES_GOLD.md`, `bench.py`, `ket_qua_benchmark.txt` và `ket_qua_pytest.txt`. Phần R2 đã chạy RecursiveChunker `chunk_size=650` trên đúng 9 file/5 query, dùng Gemini `gemini-embedding-001`, đạt 5/5 answer span top-3, 4/5 top-1 và pytest 42/42. Q3 đã có đủ A/B buyer, unfiltered, seller. Lưu ý report nhóm hiện còn số liệu lexical; nhóm cần chốt backend chung trước khi freeze.

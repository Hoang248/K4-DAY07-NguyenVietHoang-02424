# R2 Hoàng — 5 Benchmark Query + Gold Answer

## Checkpoint 5 — bộ query canonical dùng chung cho cả nhóm

**Corpus:** 9 file Markdown đã clean trong `data/etsy-policies/`.

**Embedding khi benchmark hiện tại:** `lexical`.

## Chiến lược cá nhân của Hoàng theo đề bài

- **Role:** `R2 — Benchmark`.
- **Strategy bắt buộc:** `RecursiveChunker`.
- **Separator priority phải giữ nguyên:** `["\\n\\n", "\\n", ". ", " ", ""]`.
- **Tham số benchmark hiện tại:** `chunk_size=650` trong `bench.py`; đây là mức tune được phép của đề bài so với giá trị mặc định `500` của class.
- **Nguyên tắc:** ưu tiên cắt theo đoạn, sau đó đến dòng, câu, khoảng trắng và cuối cùng mới cắt theo ký tự; các chunk con được gom lại sát giới hạn `chunk_size`.
- **Lệnh chạy của Hoàng:** `python bench.py --strategy recursive --embedding lexical`.

**Quy ước:**

- Bộ canonical có **đúng 5 query**, không thêm hoặc bớt câu.
- Các query dùng tiếng Anh vì corpus chính thức đang là tiếng Anh.
- Mỗi gold answer chỉ dùng thông tin trích được hoặc tổng hợp trực tiếp từ 9 file trong corpus; không bổ sung kiến thức Etsy bên ngoài.
- `gold_marker` là cụm đặc trưng phải xuất hiện trong nội dung chunk liên quan, dùng để chấm retrieval ở mức nội dung.
- Chunk ID bên dưới là kết quả tham chiếu của `RecursiveChunker(chunk_size=650)` hiện tại. Khi đổi chiến lược hoặc `chunk_size`, phải chấm lại theo **source file + section + marker**, không cố định chunk ID.
- Q3 vẫn là **một query duy nhất**, nhưng bắt buộc chạy A/B: có filter `buyer`, không filter và filter `seller`.

## Q1 — Condition

- **Query:** `What conditions must be met before a buyer can open a case on Etsy?`
- **Question type:** `condition`
- **Primary metadata filter:** `{"audience": "buyer"}`
- **Gold answer:** `To open a case, the estimated delivery date for the order must have passed and at least 48 hours must have passed since the buyer sent the seller a Help with order request.`
- **Gold source files:**
  - `data/etsy-policies/buyer-open-case.md`
  - `data/etsy-policies/buyer-estimated-delivery.md`
- **Gold sections:** `When can I open a case?`; `Quick answer`
- **Gold marker:** `48 hours`
- **Reference chunks for R2 recursive:** `buyer-open-case#0`, `buyer-open-case#3`
- **Verbatim evidence from corpus:**

  > For physical items and digital items ready for immediate download:
  >
  > - The estimated delivery date provided at purchase has passed.
  > - At least 48 hours have passed since you sent the seller a Help with order request.

## Q2 — Procedure

- **Query:** `How does a seller work with a buyer to resolve an open Etsy case through Shop Manager?`
- **Question type:** `procedure`
- **Primary metadata filter:** `{"audience": "seller"}`
- **Gold answer:** `The seller uses Cases in Shop Manager, selects the applicable case, and communicates through Add Your Comment in the case log.`
- **Gold source file:** `data/etsy-policies/seller-resolve-case.md`
- **Gold section:** `How do I work with my buyer to resolve the case?`
- **Gold marker:** `Shop Manager`
- **Reference chunk for R2 recursive:** `seller-resolve-case#4`
- **Verbatim evidence from corpus:**

  > If the case is open, work with the buyer through Cases in Shop Manager.
  >
  > 1. Sign in to Etsy.com and go to Shop Manager.
  > 2. Go to Help and then Cases.
  > 3. Go to the Cases reported about your shop tab and select the applicable case ID.
  > 4. Use Add Your Comment to communicate while the case is active. Depending on the order, you may also issue a refund or update shipping information.

## Q3 — List + mandatory audience-filter A/B

- **Query:** `How much refund does Etsy Purchase Protection provide for a qualifying order?`
- **Question type:** `list + A/B metadata filter`
- **Primary metadata filter:** `{"audience": "buyer"}`
- **A/B contrast filter:** `{"audience": "seller"}`
- **Unfiltered run:** also run once with no `metadata_filter`.
- **Buyer gold answer:** `Etsy’s Purchase Protection program provides a full refund for qualifying orders when an item doesn’t arrive, arrives damaged, arrives 7+ days after the maximum estimated delivery date window provided at checkout, or differs significantly from the item description or photos.`
- **Buyer gold source file:** `data/etsy-policies/buyer-purchase-protection.md`
- **Buyer gold section:** `Qualifying order issues`
- **Buyer gold marker:** `full refund`
- **Buyer reference chunk for R2 recursive:** `buyer-purchase-protection#0`
- **Seller contrast gold answer:** `If an order is eligible for Etsy Purchase Protection, Etsy covers up to $250 of a refund, or the converted equivalent in the seller’s local currency. Any remaining amount is charged to the seller, and the seller does not need to issue the refund.`
- **Seller contrast source file:** `data/etsy-policies/seller-purchase-protection.md`
- **Seller contrast section:** `Purchase Protection for Sellers`
- **Seller contrast marker:** `$250`
- **Seller reference chunk for R2 recursive:** `seller-purchase-protection#0`
- **Why this query really needs the filter:** the query does not say buyer or seller, while the two audience-specific documents use the same topic but give different coverage: buyer receives a full refund for qualifying issues, whereas the seller policy describes Etsy covering up to `$250`. The three runs must be saved separately so the group can compare top-3 precision and answer content.
- **Verbatim buyer evidence from corpus:**

  > Etsy’s Purchase Protection program provides a full refund for qualifying orders when an item:
  >
  > - Doesn’t arrive.
  > - Arrives damaged.
  > - Arrives 7+ days after the maximum estimated delivery date window provided at checkout.
  > - Differs significantly from the item description or photos, such as the wrong material or color.

- **Verbatim seller evidence from corpus:**

  > If an order is eligible for Etsy Purchase Protection, Etsy covers up to $250 of a refund, or the converted equivalent in the seller’s local currency. Any remaining amount is charged to the seller, and the seller does not need to issue the refund.

## Q4 — Formula

- **Query:** `Which components are used to calculate an Etsy estimated delivery date?`
- **Question type:** `formula`
- **Primary metadata filter:** `{"audience": "buyer"}`
- **Gold answer:** `Processing time plus carrier transit time equals the estimated delivery date.`
- **Gold source file:** `data/etsy-policies/buyer-estimated-delivery.md`
- **Gold section:** `How is the estimated delivery date calculated?`
- **Gold marker:** `carrier transit time`
- **Reference chunk for R2 recursive:** `buyer-estimated-delivery#1`
- **Verbatim evidence from corpus:**

  > The estimated delivery date is based on the processing time for the items and the transit time for the shipping carrier.
  >
  > Processing time + carrier transit time = estimated delivery date.

## Q5 — Numeric + procedure

- **Query:** `How can a seller issue a full or partial refund, and what is the Etsy Payments time limit?`
- **Question type:** `numeric + procedure`
- **Primary metadata filter:** `{"audience": "seller"}`
- **Gold answer:** `The seller uses Shop Manager to issue the refund; Etsy Payments refunds can be issued after processing and before 180 days have passed.`
- **Gold source file:** `data/etsy-policies/seller-issue-refund.md`
- **Gold sections:** `To refund an order`; `When can I issue a refund?`
- **Gold marker:** `180 days`
- **Reference chunks for R2 recursive:** `seller-issue-refund#0`, `seller-issue-refund#3`
- **Verbatim procedure evidence from corpus:**

  > 1. On Etsy.com, open Shop Manager.
  > 2. Select Orders.
  > 3. Choose the three-dot icon next to the order you want to refund.
  > 4. Choose Refund.
  > 5. Select a reason for issuing a refund and add an optional message to the buyer.
  > 6. To refund the entire transaction, select the box by Issue a full refund. To partially refund the transaction, enter the amount to refund next to the item.
  > 7. Select Review refund.
  > 8. Select Submit.

- **Verbatim time-limit evidence from corpus:**

  > If you use Etsy Payments, you can issue a refund after the payment is processed and before 180 days after the payment is processed. After 180 days, you cannot refund an order through Etsy Payments.

## CP5 execution checklist

- [ ] Cả nhóm dùng đúng 5 query ở trên, không tự đổi wording khi benchmark.
- [ ] Mỗi chunk được tạo ngoài `EmbeddingStore` và có `metadata["doc_id"]` là tên file gốc.
- [ ] Q1, Q2, Q4, Q5 chạy với filter audience tương ứng.
- [ ] Q3 chạy đủ ba lần: `buyer`, không filter, `seller`.
- [ ] Mỗi lần lưu top-3 gồm `score`, `Document.id`, `metadata.doc_id`, `audience` và preview content.
- [ ] Chấm cả `gold_doc_in_top3` và `answer_span_in_top3`; không chỉ chấm tên tài liệu.
- [ ] Ghi kết quả vào `REPORT_NHOM.md` mục 3 và file benchmark cá nhân.

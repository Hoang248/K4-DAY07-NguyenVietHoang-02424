**K4-DAY07 - NỀN TẢNG DỮ LIỆU,  
EMBEDDING & VECTOR STORE**

Kế hoạch hoàn chỉnh từ Checkpoint 1 đến Checkpoint 7

**Nhóm 3 người: Sang (R1) - Hoàng (R2) - Phát (R3)**

*Domain chốt: Etsy Marketplace - Returns, Refunds, Cases & Purchase Protection*

Phiên bản hướng dẫn: 20/09/2026

Căn cứ: README.md, K4_VARIANT.md, day7-lab-data-foundations.md, exercises.md, docs/DATA_COLLECTION.md, docs/EVALUATION.md, docs/SCORING.md và hai mẫu báo cáo trong repo.

| **Nguyên tắc sử dụng:** Các mục “BẮT BUỘC” dưới đây bám theo tài liệu Lab. Các mục “ĐỀ XUẤT NHÓM” là quyết định triển khai cho nhóm Sang - Hoàng - Phát để hoàn thành bài nhất quán và dễ so sánh. |
|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

# MỤC LỤC NỘI DUNG

1.  1\. Bản chất bài Lab, deliverable và thang điểm

2.  2\. Phân vai chính thức R1/R2/R3 và nguyên tắc “ai cũng tự code”

3.  3\. Chốt 9 URL cuối cùng và phân 3 URL/người

4.  4\. Kế hoạch theo 7 Checkpoint

5.  5\. Setup môi trường và Checkpoint 1

6.  6\. Thu thập - làm sạch - metadata - Checkpoint 2

7.  7\. Warm-up và chunking.py - Checkpoint 3

8.  8\. store.py + agent.py - Checkpoint 4

9.  9\. Chiến lược riêng + 5 benchmark query - Checkpoint 5

10. 10\. Chạy benchmark, A/B filter, failure analysis - Checkpoint 6

11. 11\. REPORT_CANHAN.md - mỗi người phải tự hoàn thiện

12. 12\. REPORT_NHOM.md - Sang tổng hợp bản cuối

13. 13\. Demo, GitHub, nộp VLearn - Checkpoint 7

14. 14\. Ma trận công việc theo từng người

15. 15\. Lỗi thường gặp và cách xử lý

16. 16\. Phụ lục lệnh nhanh, validator và checklist cuối buổi

# 1. Bản chất bài Lab, deliverable và thang điểm

| **BẮT BUỘC:** Lab kéo dài 4 giờ, gồm phần cá nhân 60 điểm và phần nhóm 40 điểm. Mỗi sinh viên phải tự hoàn thiện toàn bộ TODO trong src/ và tự chạy benchmark; phần nhóm chỉ dùng chung corpus, 5 benchmark query/gold answer và REPORT_NHOM.md. |
|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

## 1.1 Mục tiêu kỹ thuật

- Giải thích cosine similarity và dự đoán độ tương đồng giữa hai đoạn text.

- Triển khai 3 chiến lược chunking và so sánh bằng số liệu.

- Xây EmbeddingStore có search, metadata filter và delete.

- Kết nối knowledge base với agent theo mô hình RAG.

- Thu thập corpus công khai đúng provenance/robots.txt và phân tích khi retrieval thành công hoặc thất bại.

## 1.2 Deliverable bắt buộc

| **\#** | **Deliverable**                                 | **Ai làm** | **Điểm/ý nghĩa**          |
|--------|-------------------------------------------------|------------|---------------------------|
| 1      | src/ hoàn thiện; pytest tests/ -v -\> 42 passed | Mỗi người  | 30 điểm cá nhân           |
| 2      | data/\<chu-de\>/ gồm 5-10 .md + sources.csv     | Nhóm       | 10 điểm nhóm              |
| 3      | bench.py + ket_qua_benchmark.txt                | Mỗi người  | Cơ sở chấm retrieval      |
| 4      | report/REPORT_CANHAN.md                         | Mỗi người  | Tổng phần cá nhân 60 điểm |
| 5      | report/REPORT_NHOM.md                           | Nhóm       | Tổng phần nhóm 40 điểm    |
| 6      | Repo GitHub K4-DAY07-HoVaTen-MSSV + link VLearn | Mỗi người  | Điều kiện chấm            |

## 1.3 Thang điểm

| **Phần** | **Hạng mục**                   | **Điểm** |
|----------|--------------------------------|----------|
| Cá nhân  | Core Implementation - 42 tests | 30       |
| Cá nhân  | My Approach                    | 10       |
| Cá nhân  | Competition Results - 5 query  | 10       |
| Cá nhân  | Warm-up                        | 5        |
| Cá nhân  | Similarity Predictions         | 5        |
| Nhóm     | Strategy Design                | 15       |
| Nhóm     | Document Set Quality           | 10       |
| Nhóm     | Retrieval Quality              | 10       |
| Nhóm     | Demo                           | 5        |

| **Điểm chiến lược:** Strategy Design (15 điểm) cao hơn Retrieval Quality (10 điểm). Vì vậy nhóm phải giải thích được tại sao chiến lược tốt/xấu, không chỉ đưa score. |
|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|

# 2. Phân vai R1/R2/R3 và nguyên tắc ai cũng tự code

| **QUY ƯỚC NHÓM:** Sang đảm nhiệm R1 Data và là người tổng hợp REPORT_NHOM.md cuối cùng. Đây là trách nhiệm điều phối cộng thêm; Sang vẫn phải làm toàn bộ bài cá nhân giống Hoàng và Phát. |
|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

| **Người** | **Role chính thức** | **Trách nhiệm điều phối**                                                                                                                                                                      | **Chiến lược retrieval riêng**                                         |
|-----------|---------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------|
| Sang      | R1 - Data           | Chốt domain; phân chia 9 URL; kiểm metadata; giữ sources.csv; nhận 6 file còn lại từ Hoàng/Phát; chuẩn hóa corpus chung; tổng hợp REPORT_NHOM.md; phát hành bản group report cuối cho cả nhóm. | FixedSizeChunker có overlap (đề xuất nhóm; tự benchmark).              |
| Hoàng     | R2 - Benchmark      | Chủ trì đúng 5 query + gold answer; kiểm gold answer trích được từ corpus; thiết kế ít nhất 1 query thực sự cần audience filter.                                                               | RecursiveChunker (đề xuất nhóm; tự benchmark).                         |
| Phát      | R3 - Strategy       | Bảo đảm không trùng chiến lược; chạy baseline comparator; sở hữu chunker theo heading/section bắt buộc.                                                                                        | Custom Heading/Section Chunker, section dài fallback RecursiveChunker. |

## 2.1 Những việc CẢ BA đều phải tự làm

- Tự setup repo/venv và tự đạt baseline CP1.

- Tự hoàn thiện mọi TODO trong src/chunking.py, src/store.py, src/agent.py; không chia code theo kiểu “mỗi người làm một file”.

- Tự làm Warm-up và Similarity Predictions trong REPORT_CANHAN.md.

- Tự tạo bench.py của mình, chỉ thay strategy/chunker để so sánh công bằng.

- Tự chạy 5 benchmark query trên strategy của mình, lưu ket_qua_benchmark.txt.

- Tự điền REPORT_CANHAN.md và tự có repo GitHub đúng tên để nộp.

- Đều phải nói phần chiến lược của mình trong demo 6-8 phút.

# 3. Chốt 9 URL cuối cùng và phân 3 URL/người

| **ĐÃ CHỐT:** Corpus cuối dùng 9 tài liệu Etsy Help Center: 4 buyer + 5 seller, nằm trong giới hạn 5-10 tài liệu. Các cặp buyer/seller cùng chủ đề “case” và “purchase protection” giúp tạo benchmark chứng minh metadata_filter theo audience. |
|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

## 3.1 Sang - R1 Data - 3 URL

**1. How to Get Help with An Order**  
doc_id: buyer-help-order \| audience: buyer \| category: order-support

> [<u>https://help.etsy.com/hc/en-us/articles/4402660818583-How-to-Get-Help-with-An-Order</u>](https://help.etsy.com/hc/en-us/articles/4402660818583-How-to-Get-Help-with-An-Order)

**2. Refunds Returns and Exchanges for Sellers**  
doc_id: seller-returns-refunds \| audience: seller \| category: returns-refunds

> [<u>https://help.etsy.com/hc/en-us/articles/360000572888-Refunds-Returns-and-Exchanges-for-Sellers</u>](https://help.etsy.com/hc/en-us/articles/360000572888-Refunds-Returns-and-Exchanges-for-Sellers)

**3. How to Issue a Full or Partial Refund For an Order**  
doc_id: seller-issue-refund \| audience: seller \| category: refunds

> [<u>https://help.etsy.com/hc/en-us/articles/360002089188-How-to-Issue-a-Full-or-Partial-Refund-For-an-Order</u>](https://help.etsy.com/hc/en-us/articles/360002089188-How-to-Issue-a-Full-or-Partial-Refund-For-an-Order)

## 3.2 Hoàng - R2 Benchmark - 3 URL

**1. How to Open a Case**  
doc_id: buyer-open-case \| audience: buyer \| category: case-dispute

> [<u>https://help.etsy.com/hc/en-us/articles/5745586898199-How-to-Open-a-Case</u>](https://help.etsy.com/hc/en-us/articles/5745586898199-How-to-Open-a-Case)

**2. How to Resolve a Case from a Buyer**  
doc_id: seller-resolve-case \| audience: seller \| category: case-dispute

> [<u>https://help.etsy.com/hc/en-us/articles/360016126873-How-to-Resolve-a-Case-from-a-Buyer</u>](https://help.etsy.com/hc/en-us/articles/360016126873-How-to-Resolve-a-Case-from-a-Buyer)

**3. What is an Estimated Delivery Date**  
doc_id: buyer-estimated-delivery \| audience: buyer \| category: delivery

> [<u>https://help.etsy.com/hc/en-us/articles/360020601674-What-is-an-Estimated-Delivery-Date</u>](https://help.etsy.com/hc/en-us/articles/360020601674-What-is-an-Estimated-Delivery-Date)

## 3.3 Phát - R3 Strategy - 3 URL

**1. Etsy Purchase Protection Program**  
doc_id: buyer-purchase-protection \| audience: buyer \| category: purchase-protection

> [<u>https://help.etsy.com/hc/en-us/articles/7471925990807-Etsy-s-Purchase-Protection-Program</u>](https://help.etsy.com/hc/en-us/articles/7471925990807-Etsy-s-Purchase-Protection-Program)

**2. Purchase Protection for Sellers**  
doc_id: seller-purchase-protection \| audience: seller \| category: purchase-protection

> [<u>https://help.etsy.com/hc/en-us/articles/5850122619287-What-is-Etsy-s-Purchase-Protection-for-Sellers</u>](https://help.etsy.com/hc/en-us/articles/5850122619287-What-is-Etsy-s-Purchase-Protection-for-Sellers)

**3. How do I Set Return Policies on My Listings**  
doc_id: seller-set-return-policy \| audience: seller \| category: returns-policy

> [<u>https://help.etsy.com/hc/en-us/articles/7869401615255-How-do-I-Set-Return-Policies-on-My-Listings</u>](https://help.etsy.com/hc/en-us/articles/7869401615255-How-do-I-Set-Return-Policies-on-My-Listings)

## 3.4 Bảng kiểm 9 tài liệu

| **\#** | **Owner** | **doc_id**                 | **audience** | **category**        |
|--------|-----------|----------------------------|--------------|---------------------|
| 1      | Sang      | buyer-help-order           | buyer        | order-support       |
| 2      | Sang      | seller-returns-refunds     | seller       | returns-refunds     |
| 3      | Sang      | seller-issue-refund        | seller       | refunds             |
| 4      | Hoàng     | buyer-open-case            | buyer        | case-dispute        |
| 5      | Hoàng     | seller-resolve-case        | seller       | case-dispute        |
| 6      | Hoàng     | buyer-estimated-delivery   | buyer        | delivery            |
| 7      | Phát      | buyer-purchase-protection  | buyer        | purchase-protection |
| 8      | Phát      | seller-purchase-protection | seller       | purchase-protection |
| 9      | Phát      | seller-set-return-policy   | seller       | returns-policy      |

| **Lý do loại 6 URL còn lại:** Không phải vì chúng sai. Nhóm chỉ cần 5-10 tài liệu; 9 URL trên đã đủ coverage và tạo được các cặp buyer/seller phục vụ filter. Giữ 6 URL còn lại làm nguồn dự phòng nếu crawler báo robots.txt, JavaScript body rỗng hoặc lỗi encoding. |
|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

# 4. Kế hoạch theo 7 Checkpoint

| **CP** | **Mốc** | **Cần đạt**                                                                     | **Chủ trì điều phối**                  |
|--------|---------|---------------------------------------------------------------------------------|----------------------------------------|
| CP1    | 0:20    | pytest: 11 passed, 31 failed; fail là NotImplementedError                       | Mỗi người                              |
| CP2    | 1:00    | 5-10 md; metadata đủ; sources.csv 1-1; \>=2 audience; REPORT_NHOM mục 1         | Sang R1                                |
| CP3    | 1:45    | pytest -k "Chunker or Similarity or Compare" -\> 23 passed                      | Mỗi người                              |
| CP4    | 2:30    | pytest full -\> 42 passed; main.py chạy từ đầu đến cuối                         | Mỗi người                              |
| CP5    | 3:00    | bench.py chạy 5 query/top-3; có 5 gold answer; 3 strategy khác nhau             | Hoàng R2 + Phát R3                     |
| CP6    | 3:25    | mỗi người có ket_qua_benchmark.txt; có A/B filter + failure case + bảng so sánh | Cả nhóm                                |
| CP7    | 4:00    | 2 report đầy đủ; repo sạch; push; nộp link VLearn; demo sẵn sàng                | Sang tổng hợp group + mỗi người tự nộp |

# 5. Setup môi trường và Checkpoint 1

## 5.1 Repo và Python

- Fork đúng starter repo L3B trước khi clone. Mỗi người cần remote GitHub thuộc tài khoản của mình.

- Tên repo nộp cuối: K4-DAY07-HoVaTen-MSSV, họ tên viết liền không dấu.

- Python chuẩn là 3.11; 3.10+ vẫn chạy test nhưng nên dùng 3.11 để khớp môi trường chấm.

- Không dùng .venv đã đóng gói trong ZIP từ máy khác; tạo lại venv trên máy mình.

## 5.2 Setup bằng uv - luồng khuyến nghị cho nhóm

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th># đứng tại thư mục repo<br />
rm -rf .venv<br />
uv venv --python 3.11<br />
source .venv/bin/activate # macOS/Linux<br />
# Windows PowerShell: .venv\Scripts\Activate.ps1<br />
<br />
uv pip install -r requirements.txt<br />
python --version<br />
python -m pytest tests/ -v</th>
</tr>
</thead>
<tbody>
</tbody>
</table>

| **CP1 expected:** 11 passed, 31 failed trên 42 test. Nếu là ModuleNotFoundError thì venv/package setup sai; nếu fail chủ yếu NotImplementedError thì baseline đúng. |
|---------------------------------------------------------------------------------------------------------------------------------------------------------------------|

## 5.3 Commit gợi ý sau CP1

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th>git status<br />
git add .<br />
git commit -m "chore: verify day07 starter baseline"</th>
</tr>
</thead>
<tbody>
</tbody>
</table>

Nếu không có file nào thay đổi, Git có thể báo nothing to commit; không phải lỗi.

# 6. Thu thập - làm sạch - metadata - Checkpoint 2

| **BẮT BUỘC K4-L3B:** Corpus phải là chính sách đổi trả/bảo hành hoặc quy định buyer/seller của thương mại điện tử. Mỗi document có audience (buyer/seller/both), source_url, retrieved_at, document_version và ít nhất một field lọc khác. Gold answer về sau phải lấy từ corpus, không suy đoán. |
|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

## 6.1 Metadata - xử lý an toàn để thỏa mọi tài liệu yêu cầu

K4_VARIANT.md yêu cầu audience + ít nhất một field hữu ích khác. exercises.md (generic) nói source_url/retrieved_at/document_version + ít nhất 2 field hữu ích. Để thỏa cả hai cách diễn đạt, nhóm dùng bộ field sau cho mọi file:

| **Field**             | **Bắt buộc/khuyến nghị** | **Ví dụ**                      |
|-----------------------|--------------------------|--------------------------------|
| doc_id                | Bắt buộc                 | buyer-open-case                |
| title                 | Bắt buộc                 | How to Open a Case             |
| source_url            | Bắt buộc                 | URL Etsy gốc                   |
| retrieved_at          | Bắt buộc                 | 2026-09-20                     |
| document_version      | Bắt buộc                 | not-stated nếu trang không nêu |
| audience              | Bắt buộc L3B             | buyer / seller                 |
| category              | Field lọc thêm           | case-dispute                   |
| language              | Field lọc thêm           | en                             |
| license_or_permission | Nên có trong CSV         | public-source                  |

## 6.2 Sang chuẩn bị file data/urls.csv từ CSV 9 URL

17. Sang lấy file day07_etsy_urls_final_9.csv và copy vào repo thành data/urls.csv.

18. Sang kiểm không trùng doc_id; title/audience/category đúng theo bảng phân công.

19. Sang gửi cùng một data/urls.csv cho Hoàng và Phát để cả ba corpus có provenance giống nhau.

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th>cp /duong-dan/day07_etsy_urls_final_9.csv data/urls.csv<br />
# hoặc copy bằng Finder/Explorer rồi kiểm:<br />
cat data/urls.csv</th>
</tr>
</thead>
<tbody>
</tbody>
</table>

## 6.3 Mỗi người crawl 3 URL của mình

Khuyến nghị tạo ba CSV tạm để từng người không đụng vào 6 URL của người khác. Sau khi clean xong, chuyển file .md cho Sang. Crawler chính thức kiểm robots.txt, chờ \>=1 giây và tự tạo sources.csv.

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th>python scripts/fetch_public_pages.py data/urls_sang.csv --output-dir data/etsy-policies<br />
# Hoàng/Phát thay CSV tương ứng trên repo của mình</th>
</tr>
</thead>
<tbody>
</tbody>
</table>

- robots.txt disallowed -\> bỏ URL, không tìm cách vượt.

- extracted content is too short -\> trang JS/body không dùng được, thay nguồn dự phòng.

- LookupError: unknown encoding -\> bỏ URL gây lỗi khỏi lượt chạy, xử lý riêng hoặc thay nguồn.

- Không đăng nhập, không vượt CAPTCHA, không gọi API riêng tư.

## 6.4 Làm sạch file - checklist cho từng người

- Mở từng .md sau crawl; xóa navigation, header/footer lặp, feedback widget, menu, banner, nội dung không phục vụ policy.

- Giữ nguyên heading H1/H2/H3 càng nhiều càng tốt - đặc biệt quan trọng với strategy của Phát.

- Giữ mọi con số, điều kiện, ngoại lệ và mốc thời gian có thể dùng làm gold answer.

- Không tự dịch hoặc tự thêm nội dung không có trong nguồn.

- Không bịa document_version; nếu nguồn không nêu thì dùng not-stated.

- Tên file nên đúng doc_id và không dấu; 1 file = 1 nguồn.

- Nếu một nguồn trộn buyer và seller với hai đáp án khác nhau, nên tách để audience filter có tác dụng thật.

## 6.5 Frontmatter mẫu

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th>---<br />
doc_id: buyer-open-case<br />
title: How to Open a Case<br />
source_url: https://help.etsy.com/...<br />
retrieved_at: 2026-09-20<br />
document_version: not-stated<br />
audience: buyer<br />
category: case-dispute<br />
language: en<br />
---<br />
<br />
# How to Open a Case<br />
<br />
&lt;nội dung đã clean&gt;</th>
</tr>
</thead>
<tbody>
</tbody>
</table>

## 6.6 Quy trình merge corpus do Sang điều phối

20. Hoàng gửi 3 file .md đã clean + 3 dòng provenance tương ứng cho Sang.

21. Phát gửi 3 file .md đã clean + 3 dòng provenance tương ứng cho Sang.

22. Sang clean 3 file của mình, gom đủ 9 file vào data/etsy-policies/.

23. Sang chuẩn hóa frontmatter và rebuild/kiểm sources.csv sao cho đúng 1 dòng cho mỗi file .md.

24. Sang gửi lại corpus 9 file đã chốt cho Hoàng và Phát. Từ đây cả ba phải benchmark trên đúng cùng corpus; không được tự sửa nội dung riêng làm mất tính công bằng.

## 6.7 Validator CP2

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th>python - &lt;&lt;'PY'<br />
import csv, re<br />
from pathlib import Path<br />
D = Path("data/etsy-policies")<br />
REQ = ["doc_id","title","source_url","retrieved_at","document_version","audience"]<br />
mds = sorted(D.glob("*.md"))<br />
rows = list(csv.DictReader(open(D/"sources.csv", encoding="utf-8")))<br />
ids, auds = [], {}<br />
for p in mds:<br />
text = p.read_text(encoding="utf-8")<br />
parts = text.split("---")<br />
fm = dict(re.findall(r"^(\w+):\s*(.+)$", parts[1], re.M))<br />
ids.append(fm.get("doc_id"))<br />
auds[fm.get("audience")] = auds.get(fm.get("audience"), 0) + 1<br />
ok = all(k in fm for k in REQ) and fm.get("doc_id") == p.stem<br />
print(f"{p.name:45} {'OK' if ok else 'THIEU METADATA'}")<br />
print("so file :", len(mds), "(can 5-10)")<br />
print("csv :", "khop" if sorted(r["doc_id"] for r in rows)==sorted(ids) else "LECH")<br />
print("audience:", auds)<br />
PY</th>
</tr>
</thead>
<tbody>
</tbody>
</table>

| **Lưu ý validator:** Trong codelab gốc, biểu thức regex hiển thị có ký tự \\ ở cuối mẫu. Nếu copy nguyên mà không match frontmatter, dùng mẫu kết thúc bằng \$ như đoạn validator ở trên. |
|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

| **CP2 PASS:** 9 file .md; mọi file OK; sources.csv khớp 1-1; audience có buyer và seller; REPORT_NHOM mục 1 đã điền. |
|----------------------------------------------------------------------------------------------------------------------|

# 7. Warm-up và chunking.py - Checkpoint 3

| **BẮT BUỘC:** Từ CP2 trở đi là code cá nhân. Sang, Hoàng và Phát đều tự hoàn thiện các TODO; role nhóm không thay thế nghĩa vụ cá nhân. |
|-----------------------------------------------------------------------------------------------------------------------------------------|

## 7.1 Warm-up REPORT_CANHAN mục 1

- Cosine similarity cao: vector text gần cùng hướng -\> ngữ nghĩa gần nhau; nên cho ví dụ khác từ vựng nhưng cùng nghĩa.

- Cosine thường hợp text embedding hơn Euclidean vì tập trung vào hướng/quan hệ hơn độ lớn vector.

- Chunking math: ceil((10000-50)/(500-50)) = 23 chunks.

- Overlap 100: ceil((10000-100)/(500-100)) = 25 chunks; overlap lớn hơn giữ ngữ cảnh biên tốt hơn nhưng tăng số chunk/chi phí.

## 7.2 TODO SentenceChunker

- Tách tại vị trí sau dấu câu . ! ? kết hợp whitespace/newline nhưng phải giữ dấu câu.

- Gom tối đa max_sentences_per_chunk câu thành mỗi chunk.

- Strip khoảng trắng; input rỗng trả \[\].

- Ghi rõ edge case chưa xử lý tốt như chữ viết tắt hoặc số thập phân.

## 7.3 TODO RecursiveChunker

- Thử separator ưu tiên: đoạn văn -\> dòng -\> câu -\> khoảng trắng -\> cắt cứng.

- Mảnh quá dài thì đệ quy xuống separator tiếp theo.

- Mảnh nhỏ liền kề phải được gom lên tới gần chunk_size để tránh hàng trăm chunk vụn.

- Phải có base case cho separators=\[\] và text rỗng.

## 7.4 compute_similarity và comparator

- compute_similarity dùng cosine; vector zero-norm trả 0.0, không để ZeroDivisionError.

- ChunkingStrategyComparator.compare phải trả đúng 3 key: fixed_size, by_sentences, recursive.

- Mỗi key có count, avg_length, chunks; text rỗng phải tránh chia 0.

| python -m pytest tests/ -k "Chunker or Similarity or Compare" -v |
|------------------------------------------------------------------|

| **CP3 PASS:** Kỳ vọng 23 passed. |
|----------------------------------|

# 8. store.py + agent.py - Checkpoint 4

## 8.1 EmbeddingStore

- Để ổn định bài chấm, dùng in-memory path; codelab cảnh báo nhánh Chroma có thể gây fail nếu \_use_chroma bật nhưng chưa triển khai.

- \_make_record: copy metadata; luôn bảo đảm metadata\["doc_id"\] tồn tại và trỏ về file gốc.

- \_search_records: dùng chung cho search và search_with_filter để logic ranking nhất quán; output không cần embedding vector.

- search_with_filter: lọc candidate theo metadata TRƯỚC rồi mới similarity search.

- delete_document: xóa mọi chunk có metadata\["doc_id"\] khớp và trả True/False.

- add_documents không tự chunk: 1 Document input = 1 record.

## 8.2 KnowledgeBaseAgent.answer

25. Retrieve top-k.

26. Dựng context; nên đánh số chunk \[1\], \[2\], \[3\] và kèm source/doc_id để trace.

27. Prompt ràng buộc model chỉ dùng context được cung cấp; không có dữ liệu thì nói không tìm thấy.

28. Gọi llm_fn; store rỗng thì trả thông báo thay vì crash.

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th>python -m pytest tests/ -v<br />
python main.py "Chunking là gì?"</th>
</tr>
</thead>
<tbody>
</tbody>
</table>

| **CP4 PASS:** 42 passed và main.py chạy end-to-end. Mỗi người chụp/copy output pytest thật vào REPORT_CANHAN mục 3. |
|---------------------------------------------------------------------------------------------------------------------|

# 9. Chiến lược riêng + benchmark - Checkpoint 5

## 9.1 Strategy chốt để không trùng nhau

| **Người** | **Strategy chốt**              | **Ghi chú**                                                                                                                                                   |
|-----------|--------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Sang      | FixedSizeChunker + overlap     | Đề xuất bắt đầu chunk_size 600-900, overlap 80-150 rồi ghi lại tham số thực tế. Đây là đề xuất tuning, không phải con số bắt buộc của Lab.                    |
| Hoàng     | RecursiveChunker               | Giữ separator ưu tiên; có thể tune chunk_size.                                                                                                                |
| Phát      | Heading/Section Chunker custom | Tách theo heading; section quá dài fallback Recursive; khi cắt section dài phải gắn lại heading vào mọi mảnh con. Đây là strategy bắt buộc của nhóm theo L3B. |

## 9.2 R2 Hoàng - đúng 5 benchmark query + gold answer

- Đúng 5 câu; đa dạng: số liệu, điều kiện, quy trình, liệt kê.

- Mỗi gold answer phải trích được từ 9 file đã clean; không lấy “kiến thức Etsy” ngoài corpus.

- Ít nhất 1 query phải thật sự cần metadata_filter={"audience":"buyer"} hoặc seller.

- Mỗi query phải chỉ ra chunk/file chứa gold info để chấm retrieval ở mức nội dung.

## 9.3 Bộ 5 query khởi tạo đề xuất cho Hoàng kiểm chứng lại

| **ĐỀ XUẤT - chưa phải gold cuối:** Hoàng phải đối chiếu nội dung file .md sau crawl/clean trước khi đóng băng gold answer. Không copy mù các câu dưới đây nếu corpus thực tế bị thay đổi. |
|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

| **\#** | **Query đề xuất**                                                                                                                                    | **Nguồn dự kiến**                                      |
|--------|------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------|
| 1      | Buyer phải đáp ứng những điều kiện thời gian nào trước khi có thể mở case?                                                                           | buyer-open-case / buyer-estimated-delivery             |
| 2      | Một seller xử lý một case đang mở với buyer qua Shop Manager như thế nào?                                                                            | seller-resolve-case                                    |
| 3      | “Purchase Protection áp dụng thế nào?” - chạy A/B với audience=buyer và audience=seller để chứng minh hai đối tượng có nội dung/điều kiện khác nhau. | buyer-purchase-protection + seller-purchase-protection |
| 4      | Estimated Delivery Date được tính từ những thành phần nào?                                                                                           | buyer-estimated-delivery                               |
| 5      | Seller có thể issue full/partial refund theo quy trình nào và giới hạn thời gian nào cần lưu ý?                                                      | seller-issue-refund                                    |

## 9.4 R3 Phát - baseline comparator

- Chạy ChunkingStrategyComparator().compare() trên 2-3 tài liệu.

- Bỏ YAML frontmatter trước khi compare để metrics chỉ phản ánh content.

- Ghi count và avg_length cho Fixed/Sentence/Recursive vào REPORT_NHOM mục 2.

- Đánh giá thêm coherence: có cắt giữa ý không, heading có bị mất không.

## 9.5 bench.py - cấu trúc bắt buộc cho từng người

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th># 1) đọc từng .md -&gt; parse YAML frontmatter thành metadata + body content<br />
# 2) chunk body bằng strategy của cá nhân<br />
# 3) mỗi chunk thành Document:<br />
# id=f"{path.stem}#{i}"<br />
# metadata={**frontmatter, "doc_id": path.stem}<br />
# 4) add_documents() vào EmbeddingStore<br />
# 5) chạy đúng 5 query chung; dùng search_with_filter() khi query yêu cầu<br />
# 6) in top-3: score, Document.id, metadata.doc_id, audience, preview content<br />
# 7) lưu output vào ket_qua_benchmark.txt</th>
</tr>
</thead>
<tbody>
</tbody>
</table>

- Metadata frontmatter phải được copy vào mọi chunk.

- Chunking phải xảy ra ngoài store.

- Ba người giữ ingest/query logic giống nhau; chỉ thay chunker để so sánh công bằng.

- Nếu dùng API embedding có chi phí, nên cache embedding theo hash nội dung.

| **CP5 PASS:** Mỗi bench.py chạy đủ 5 query/top-3; nhóm đã khóa 5 gold answer trong REPORT_NHOM mục 3; ba người dùng ba strategy khác nhau. |
|--------------------------------------------------------------------------------------------------------------------------------------------|

# 10. Chạy benchmark, A/B filter và failure analysis - Checkpoint 6

## 10.1 Chọn embedding backend

- MockEmbedder đủ cho pytest nhưng không mã hóa semantic; benchmark bằng mock có thể là nhiễu.

- Nếu có điều kiện, dùng local multilingual / OpenAI / Gemini embedder. Nếu bắt buộc dùng mock, ghi rõ hạn chế trong report và tập trung phân tích chunk count, avg_length, coherence.

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th># Local<br />
uv pip install -r requirements-local.txt<br />
# .env: EMBEDDING_PROVIDER=local<br />
<br />
# Hoặc OpenAI/Gemini theo README; tuyệt đối không commit .env hay API key.</th>
</tr>
</thead>
<tbody>
</tbody>
</table>

## 10.2 Chấm retrieval ở mức nội dung

- Không chỉ kiểm doc_id gold có ở top-3; phải xem chunk top-3 có thật sự chứa thông tin trả lời hay không.

- Rubric: 2 điểm nếu top-3 có chunk liên quan và agent trả lời đúng; 1 điểm nếu có liên quan nhưng thiếu/không ở top-1; 0 nếu không có chunk trả lời được.

- Nên ghi marker/phrase đặc trưng của gold answer để kiểm chunk content một cách nhất quán.

## 10.3 A/B metadata filter bắt buộc

29. Chọn query \#3 Purchase Protection (hoặc query khác Hoàng chốt) là query filter.

30. Mỗi người chạy cùng query một lần không filter.

31. Chạy lại với metadata_filter buyer hoặc seller đúng đối tượng.

32. Lưu top-3 của cả hai lần; so sánh precision/recall và agent answer.

33. Nếu hai lần giống hệt nhau và không chứng minh được lợi ích thì query/corpus chưa thực sự cần filter - phải sửa trước khi nộp.

## 10.4 Failure analysis

- Phải có ít nhất 1 failure case thật: query nào hỏng, vì sao, sửa thế nào.

- Ví dụ nguyên nhân: chunk đúng chủ đề nhưng thiếu số liệu; top-3 đúng doc nhưng sai section; overlap quá ít; filter quá cứng làm mất recall; query mơ hồ.

- Đừng “chữa” failure bằng cách giấu kết quả; failure analysis là phần thể hiện hiểu retrieval.

| **CP6 PASS:** Mỗi người có ket_qua_benchmark.txt riêng + REPORT_CANHAN mục 5; nhóm có bảng comparison và ít nhất 1 failure case trong REPORT_NHOM mục 2/4. |
|------------------------------------------------------------------------------------------------------------------------------------------------------------|

# 11. REPORT_CANHAN.md - mỗi người tự hoàn thiện

| **Mục**                  | **Nội dung phải có**                                                                             | **Ai**                       |
|--------------------------|--------------------------------------------------------------------------------------------------|------------------------------|
| 1 Warm-up                | Cosine similarity + ví dụ high/low; Euclidean vs cosine; chunking math 23/25                     | Mỗi người tự viết            |
| 2 My Approach            | SentenceChunker, RecursiveChunker, EmbeddingStore, search_with_filter/delete, KnowledgeBaseAgent | Mỗi người tự mô tả code mình |
| 3 Core Implementation    | Output pytest thật; số pass /42                                                                  | Mỗi người                    |
| 4 Similarity Predictions | 5 cặp câu; dự đoán cao/thấp trước khi chạy; điểm thực tế; reflection                             | Mỗi người                    |
| 5 Competition Results    | Đúng 5 query chung; top-1 summary/score/relevance/agent answer; top-3 relevant count             | Mỗi người                    |

| **Không copy nguyên báo cáo cá nhân:** Ba người có thể dùng chung query/corpus, nhưng phần approach, test output, similarity prediction và benchmark result phải phản ánh repo/strategy của từng người. |
|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

# 12. REPORT_NHOM.md - Sang tổng hợp bản cuối

| **Vai Sang:** Sang là người giữ “single source of truth” cho REPORT_NHOM.md. Hoàng và Phát cung cấp dữ liệu theo deadline; Sang tổng hợp, chuẩn hóa wording và phát hành bản cuối để cả ba repo dùng cùng một nội dung group report. |
|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

## 12.1 Mục 1 - Document Set Quality (Sang chủ trì từ CP2)

- Chủ đề: Etsy Marketplace - Returns, Refunds, Cases & Purchase Protection.

- 2-3 câu lý do: corpus tách buyer/seller; có cấu trúc heading; phù hợp A/B metadata filter và so sánh chunking.

- Data Inventory đủ 9 tài liệu: title, source URL, retrieved_at/version, số ký tự sau clean, metadata.

- Governance checklist: nguồn public/được phép, không credential/PII, đủ provenance.

- Metadata schema: audience, category, language, source_url, retrieved_at, document_version.

## 12.2 Mục 2 - Strategy Design

- Phát gửi baseline count/avg_length/coherence trên 2-3 docs.

- Sang ghi strategy FixedSize + tham số thực tế và rationale.

- Hoàng ghi Recursive + tham số thực tế và rationale.

- Phát ghi custom Heading/Section + code snippet ngắn và fallback recursive.

- Sang tổng hợp bảng score/strength/weakness và kết luận strategy nào tốt nhất, không chỉ dựa vào điểm mà dựa cả coherence/filter behavior.

## 12.3 Mục 3 - Benchmark & Retrieval Quality

- Hoàng gửi đúng 5 query + gold answer + file/chunk chứa thông tin.

- Cả ba gửi top-3/score của mình cho Sang.

- Sang điền strategy tốt nhất cho từng query, có relevant chunk top-3 hay không và ghi chú.

- Phải trả lời rõ metadata filtering giúp ở query nào; kèm A/B evidence.

## 12.4 Mục 4 - Demo & Lessons

- 2-3 insight đáng trình bày.

- Bài học từ cùng corpus nhưng khác chunking.

- Ít nhất 1 failure case thật + nguyên nhân + cải thiện.

- Nếu làm lại sẽ đổi gì trong data strategy.

## 12.5 Quy trình bàn giao REPORT_NHOM

| **Mốc**   | **Hoàng gửi Sang**               | **Phát gửi Sang**                        | **Sang làm**                                    |
|-----------|----------------------------------|------------------------------------------|-------------------------------------------------|
| Sau CP2   | 3 file clean + xác nhận metadata | 3 file clean + xác nhận heading          | Merge 9 files, sources.csv, Report mục 1        |
| Trước CP5 | 5 query + gold answer draft      | Baseline + heading chunker rationale     | Review query/corpus; cập nhật mục 2/3           |
| Sau CP6   | ket_qua + score + observation    | ket_qua + score + failure/coherence note | Gom cả 3, so sánh, viết kết luận                |
| Trước CP7 | Review group report              | Review group report                      | Freeze REPORT_NHOM.md; gửi bản cuối cho cả nhóm |

# 13. Demo, GitHub và nộp VLearn - Checkpoint 7

## 13.1 Demo 6-8 phút

| **Khoảng** | **Nội dung**                                         | **Người nói chính**        |
|------------|------------------------------------------------------|----------------------------|
| ~1 phút    | Domain + 9 tài liệu + metadata schema                | Sang                       |
| ~2 phút    | Mỗi người tóm tắt strategy riêng                     | Sang + Hoàng + Phát        |
| ~2-3 phút  | So sánh score/coherence; tại sao strategy thắng/thua | Cả nhóm; Phát dẫn strategy |
| ~1-2 phút  | Live 1-2 query; một query A/B filter                 | Hoàng dẫn benchmark        |
| Còn lại    | Q&A                                                  | Cả ba                      |

| **Demo discipline:** Mở sẵn terminal với bench.py đã chạy được. Không đợi lên demo mới debug. |
|-----------------------------------------------------------------------------------------------|

## 13.2 Nộp bài - mỗi người một repo

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th>python -m pytest tests/ -v # 42 passed<br />
git status # không có .venv/ hoặc .env<br />
<br />
git add .<br />
git commit -m "Nop bai Lab 07"<br />
git branch -M main<br />
git push -u origin main</th>
</tr>
</thead>
<tbody>
</tbody>
</table>

- Mỗi người có repo riêng đúng quy ước K4-DAY07-HoVaTen-MSSV.

- Hoàng và Phát copy chính xác REPORT_NHOM.md bản Sang freeze vào repo của mình.

- Cả ba dùng cùng corpus 9 file cuối + sources.csv để so sánh công bằng.

- Mỗi repo có REPORT_CANHAN riêng, bench.py riêng, ket_qua_benchmark.txt riêng.

- Nộp link repo GitHub trên VLearn, không nộp ZIP.

## 13.3 Checkpoint 7 - checklist tuyệt đối

**☐** pytest tests/ -v -\> 42 passed; không còn raise NotImplementedError

**☐** data/etsy-policies/ có 9 .md đủ metadata; sources.csv khớp 1-1

**☐** có buyer và seller; ít nhất 1 query dùng audience filter

**☐** Phát có heading/section chunker

**☐** REPORT_CANHAN + REPORT_NHOM điền đủ, pytest output là thật

**☐** bench.py + ket_qua_benchmark.txt đã commit

**☐** repo không chứa .venv/.env/API key; đã push; link đã nộp VLearn

# 14. Ma trận công việc theo từng người

## 14.1 Sang

- CP1: setup + baseline 11/31.

- CP2: crawl/clean đúng 3 URL được giao, giữ provenance và heading.

- CP3: tự code chunking/similarity/comparator -\> 23 passed.

- CP4: tự code store/agent -\> 42 passed; tự điền test output.

- CP5: tự build bench.py và chạy đúng 5 query chung.

- CP6: lưu ket_qua_benchmark.txt, điền personal result, tìm observation/failure.

- CP7: hoàn thiện REPORT_CANHAN, repo, push và demo phần strategy.

| **Việc cộng thêm R1 + Report:** Phân 9 URL; merge 9 file; sources.csv; kiểm metadata; điền REPORT_NHOM mục 1; thu kết quả Hoàng/Phát; tổng hợp toàn REPORT_NHOM; phát hành bản cuối. |
|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

## 14.2 Hoàng

- CP1: setup + baseline 11/31.

- CP2: crawl/clean đúng 3 URL được giao, giữ provenance và heading.

- CP3: tự code chunking/similarity/comparator -\> 23 passed.

- CP4: tự code store/agent -\> 42 passed; tự điền test output.

- CP5: tự build bench.py và chạy đúng 5 query chung.

- CP6: lưu ket_qua_benchmark.txt, điền personal result, tìm observation/failure.

- CP7: hoàn thiện REPORT_CANHAN, repo, push và demo phần strategy.

| **Việc cộng thêm R2:** Soạn đúng 5 query/gold; kiểm gold từ corpus; thiết kế query A/B filter; gửi bảng benchmark/gold cho Sang. |
|----------------------------------------------------------------------------------------------------------------------------------|

## 14.3 Phát

- CP1: setup + baseline 11/31.

- CP2: crawl/clean đúng 3 URL được giao, giữ provenance và heading.

- CP3: tự code chunking/similarity/comparator -\> 23 passed.

- CP4: tự code store/agent -\> 42 passed; tự điền test output.

- CP5: tự build bench.py và chạy đúng 5 query chung.

- CP6: lưu ket_qua_benchmark.txt, điền personal result, tìm observation/failure.

- CP7: hoàn thiện REPORT_CANHAN, repo, push và demo phần strategy.

| **Việc cộng thêm R3:** Chạy comparator baseline; giữ 3 strategy không trùng; triển khai heading/section chunker; gửi baseline + rationale + failure/coherence note cho Sang. |
|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

# 15. Lỗi thường gặp và cách xử lý

| **Triệu chứng**                     | **Nguyên nhân**                                    | **Cách xử lý**                                    |
|-------------------------------------|----------------------------------------------------|---------------------------------------------------|
| Crawler disallowed by robots.txt    | Nguồn cấm auto crawl                               | Đổi nguồn; không vượt robots.                     |
| Crawler extracted content too short | Trang JS/body rỗng                                 | Đổi URL.                                          |
| LookupError encoding                | Charset server lỗi                                 | Bỏ URL đó khỏi batch; dùng dự phòng.              |
| Corpus top-k toàn menu/footer       | Chưa clean crawl output                            | Clean thủ công trước chunk.                       |
| Filter không đổi kết quả            | Chỉ có 1 audience hoặc buyer/seller chung file     | Tách corpus/audience; sửa query A/B.              |
| search_with_filter trả rỗng         | Metadata không truyền vào chunk hoặc lọc sau top-k | Copy frontmatter vào mọi chunk; lọc trước search. |
| delete_document False               | Thiếu metadata doc_id                              | Set doc_id file gốc trong \_make_record.          |
| Recursive chunk vụn                 | Không merge mảnh nhỏ                               | Thêm bước gom lên.                                |
| Comparator ZeroDivision             | Text rỗng count=0                                  | Guard avg_length.                                 |
| Benchmark vô nghĩa/score âm         | Dùng MockEmbedder                                  | Bật embedder thật hoặc ghi rõ hạn chế.            |
| Top-3 đúng doc nhưng agent sai      | Chunk top-3 không chứa answer                      | Chấm ở mức content; điều chỉnh chunking/overlap.  |
| Git lộ key/venv                     | Commit .env/.venv                                  | Kiểm .gitignore và git status trước push.         |

# 16. Phụ lục lệnh nhanh, commit plan và checklist cuối buổi

## 16.1 Command sequence từ đầu đến cuối

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th># CP1<br />
uv venv --python 3.11<br />
source .venv/bin/activate<br />
uv pip install -r requirements.txt<br />
python -m pytest tests/ -v<br />
<br />
# CP2<br />
python scripts/fetch_public_pages.py data/urls.csv --output-dir data/etsy-policies<br />
# clean + validate + update REPORT_NHOM mục 1<br />
<br />
# CP3<br />
python -m pytest tests/ -k "Chunker or Similarity or Compare" -v<br />
<br />
# CP4<br />
python -m pytest tests/ -v<br />
python main.py "Chunking là gì?"<br />
<br />
# CP5/CP6<br />
python bench.py | tee ket_qua_benchmark.txt<br />
<br />
# CP7<br />
python -m pytest tests/ -v<br />
git status<br />
git add .<br />
git commit -m "Nop bai Lab 07"<br />
git push</th>
</tr>
</thead>
<tbody>
</tbody>
</table>

## 16.2 Commit plan khuyến nghị

| **Mốc** | **Commit message gợi ý**                            |
|---------|-----------------------------------------------------|
| CP1     | chore: verify day07 starter baseline                |
| CP2     | data: add cleaned Etsy policy corpus and metadata   |
| CP3     | feat: implement chunking and cosine similarity      |
| CP4     | feat: implement embedding store and rag agent       |
| CP5     | feat: add personal retrieval benchmark strategy     |
| CP6     | docs: record benchmark results and failure analysis |
| CP7     | docs: finalize individual and group reports         |

## 16.3 Cấu trúc repo cuối

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th>K4-DAY07-HoVaTen-MSSV/<br />
├── src/ # mọi TODO hoàn thiện<br />
├── data/<br />
│ └── etsy-policies/<br />
│ ├── 9 file .md<br />
│ └── sources.csv<br />
├── report/<br />
│ ├── REPORT_CANHAN.md # riêng từng người<br />
│ └── REPORT_NHOM.md # chung, Sang freeze bản cuối<br />
├── bench.py # riêng từng người<br />
├── ket_qua_benchmark.txt # riêng từng người<br />
├── tests/<br />
├── main.py<br />
└── ...</th>
</tr>
</thead>
<tbody>
</tbody>
</table>

## 16.4 “Definition of Done” của nhóm

**☐** 9 URL chốt, 3 URL/người, 4 buyer + 5 seller.

**☐** Corpus clean giống nhau trên cả 3 repo.

**☐** Ba strategy khác nhau: Fixed / Recursive / Heading custom.

**☐** 5 query chung + 5 gold answer kiểm chứng từ corpus.

**☐** Có A/B filter thật sự làm thay đổi/chất lượng kết quả.

**☐** Mỗi người 42/42 tests, bench riêng, personal report riêng.

**☐** Sang đã tổng hợp và freeze group report; Hoàng/Phát đã đồng bộ đúng bản.

**☐** Demo rehearsal ít nhất 1 lần; terminal chuẩn bị sẵn.

**☐** Mỗi repo sạch key/venv và đã push/nộp link.

# PHỤ LỤC A - Nguồn yêu cầu dùng để biên soạn hướng dẫn

- README.md - mục tiêu, hai phase, deliverable, scoring summary.

- K4_VARIANT.md - ràng buộc riêng L3B về audience, metadata filter, heading chunker và gold answer.

- day7-lab-data-foundations.md - timeline 7 checkpoint, role R1/R2/R3, coding guidance, benchmark, demo/submission.

- exercises.md - warm-up, TODO checklist, strategy/benchmark/failure analysis.

- docs/DATA_COLLECTION.md - provenance, robots.txt, format frontmatter, sources.csv và checklist corpus.

- docs/EVALUATION.md - precision, chunk coherence, metadata utility, grounding, data strategy impact.

- docs/SCORING.md - rubric 60 cá nhân + 40 nhóm.

- report/REPORT_CANHAN.md và report/REPORT_NHOM.md - cấu trúc báo cáo phải điền.

# PHỤ LỤC B - 9 URL cuối cùng (copy-ready)

**1. \[Sang\] buyer-help-order - How to Get Help with An Order**

> [<u>https://help.etsy.com/hc/en-us/articles/4402660818583-How-to-Get-Help-with-An-Order</u>](https://help.etsy.com/hc/en-us/articles/4402660818583-How-to-Get-Help-with-An-Order)

**2. \[Sang\] seller-returns-refunds - Refunds Returns and Exchanges for Sellers**

> [<u>https://help.etsy.com/hc/en-us/articles/360000572888-Refunds-Returns-and-Exchanges-for-Sellers</u>](https://help.etsy.com/hc/en-us/articles/360000572888-Refunds-Returns-and-Exchanges-for-Sellers)

**3. \[Sang\] seller-issue-refund - How to Issue a Full or Partial Refund For an Order**

> [<u>https://help.etsy.com/hc/en-us/articles/360002089188-How-to-Issue-a-Full-or-Partial-Refund-For-an-Order</u>](https://help.etsy.com/hc/en-us/articles/360002089188-How-to-Issue-a-Full-or-Partial-Refund-For-an-Order)

**4. \[Hoàng\] buyer-open-case - How to Open a Case**

> [<u>https://help.etsy.com/hc/en-us/articles/5745586898199-How-to-Open-a-Case</u>](https://help.etsy.com/hc/en-us/articles/5745586898199-How-to-Open-a-Case)

**5. \[Hoàng\] seller-resolve-case - How to Resolve a Case from a Buyer**

> [<u>https://help.etsy.com/hc/en-us/articles/360016126873-How-to-Resolve-a-Case-from-a-Buyer</u>](https://help.etsy.com/hc/en-us/articles/360016126873-How-to-Resolve-a-Case-from-a-Buyer)

**6. \[Hoàng\] buyer-estimated-delivery - What is an Estimated Delivery Date**

> [<u>https://help.etsy.com/hc/en-us/articles/360020601674-What-is-an-Estimated-Delivery-Date</u>](https://help.etsy.com/hc/en-us/articles/360020601674-What-is-an-Estimated-Delivery-Date)

**7. \[Phát\] buyer-purchase-protection - Etsy Purchase Protection Program**

> [<u>https://help.etsy.com/hc/en-us/articles/7471925990807-Etsy-s-Purchase-Protection-Program</u>](https://help.etsy.com/hc/en-us/articles/7471925990807-Etsy-s-Purchase-Protection-Program)

**8. \[Phát\] seller-purchase-protection - Purchase Protection for Sellers**

> [<u>https://help.etsy.com/hc/en-us/articles/5850122619287-What-is-Etsy-s-Purchase-Protection-for-Sellers</u>](https://help.etsy.com/hc/en-us/articles/5850122619287-What-is-Etsy-s-Purchase-Protection-for-Sellers)

**9. \[Phát\] seller-set-return-policy - How do I Set Return Policies on My Listings**

> [<u>https://help.etsy.com/hc/en-us/articles/7869401615255-How-do-I-Set-Return-Policies-on-My-Listings</u>](https://help.etsy.com/hc/en-us/articles/7869401615255-How-do-I-Set-Return-Policies-on-My-Listings)

**HẾT - dùng checklist CP7 trước khi push bài**

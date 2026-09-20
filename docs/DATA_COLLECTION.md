# Hướng Dẫn Thu Thập (Crawl) và Chuẩn Hóa Dữ Liệu — K4-L3B

Mỗi nhóm thu thập dữ liệu về chủ đề bắt buộc của lớp **L3B: chính sách đổi trả/bảo hành thương mại điện tử**. Mục tiêu là có một bộ tài liệu nhỏ, đáng tin cậy để so sánh retrieval — không phải crawl càng nhiều càng tốt. Xem ràng buộc riêng của L3B tại [`K4_VARIANT.md`](../K4_VARIANT.md).

## 1. Phạm vi dữ liệu cần nộp

- Chủ đề: **chính sách đổi trả, bảo hành, hoặc quy định người bán/người mua** trên nền tảng thương mại điện tử (chọn một sàn/cửa hàng cụ thể, không cần phủ hết).
- Thu thập **5–10 tài liệu công khai** liên quan trực tiếp đến chủ đề; ưu tiên trang chính sách chính thức của sàn/cửa hàng, có cấu trúc và ngày cập nhật.
- Mỗi tài liệu là một file `.md` trong `data/<ten-chu-de>/`; ghi nguồn trong `data/<ten-chu-de>/sources.csv`.
- Không dùng dữ liệu cá nhân, thông tin đăng nhập, tài liệu nội bộ/không được phép chia sẻ, nội dung sau đăng nhập (ví dụ trang quản trị người bán riêng tư), hoặc nội dung có quyền sử dụng không rõ ràng.

## 2. Cách crawl/thu thập

1. Lập trước danh sách 5–10 URL và kiểm tra mỗi trang thực sự thuộc chủ đề đã chọn.
2. Đọc điều khoản sử dụng và `robots.txt`. Nếu website không cho crawl tự động, đổi nguồn hoặc chỉ chép tay phần công khai được phép dùng — **trang mở công khai với người đọc không đồng nghĩa cho phép truy cập tự động**.
3. Chỉ lấy nội dung công khai cần thiết; không đăng nhập, vượt CAPTCHA, né giới hạn truy cập, hay gọi API riêng tư.
4. Nếu dùng script: crawl chậm (ít nhất 1 giây giữa các request), đặt `User-Agent`, và không crawl toàn website. Với quy mô lab, 5–10 trang là đủ.
5. Lưu URL gốc, ngày lấy dữ liệu và ngày hiệu lực/phiên bản (nếu nguồn có nêu). **Làm sạch trước khi lưu**: loại bỏ menu, banner khuyến mãi, danh sách sản phẩm không liên quan, footer lặp lại — giữ lại đúng điều khoản, con số và mốc thời gian.
6. Đọc lại nội dung đã làm sạch; không tự thêm hoặc suy đoán thông tin không có trong nguồn, và cảnh giác việc công cụ fetch có thể tự dịch nội dung sang tiếng Anh.

> Không bắt buộc nộp scraper. Chỉ nộp script nếu không làm lộ API key hay dữ liệu không được phép chia sẻ.

### Dùng crawler mẫu (khuyến nghị)

Repo có sẵn `scripts/fetch_public_pages.py`. Sao chép `scripts/urls.example.csv`, điền các URL được phép dùng, rồi chạy:

```bash
cp scripts/urls.example.csv data/urls.csv
python scripts/fetch_public_pages.py data/urls.csv --output-dir data/<ten-chu-de>
```

Cột bắt buộc trong `data/urls.csv` là `url`. Các cột `doc_id`, `title`, `audience`, `category`, `language`, `document_version`, `license_or_permission` sẽ được đưa thẳng vào frontmatter của file `.md` sinh ra.

Script chỉ lấy trang HTML/text công khai, kiểm tra `robots.txt`, chờ tối thiểu 1 giây giữa các request và tự sinh `.md` cùng `sources.csv`. Không dùng nó cho nội dung cần đăng nhập, CAPTCHA, trang render bằng JavaScript hoặc PDF; khi đó hãy chọn nguồn khác hoặc chuyển/clean thủ công.

**Lỗi đã biết:** nếu server trả `charset` không hợp lệ (ví dụ `charset=utf-8,gbk`), script crash với `LookupError: unknown encoding: ...` — lỗi này không nằm trong danh sách bắt lỗi của script nên một URL hỏng làm sập cả lượt chạy. Bỏ URL đó khỏi CSV, chạy tiếp, xử lý riêng nó sau.

## 3. Cấu trúc thư mục

```text
data/
└── <ten-chu-de>/
    ├── <tai-lieu-01>.md
    ├── <tai-lieu-02>.md
    └── sources.csv
```

Dùng tên file chữ thường, không dấu, nối bằng dấu gạch ngang; một file chỉ chứa một văn bản nguồn. Dùng UTF-8 và ưu tiên Markdown để giữ tiêu đề, danh sách, bảng. Không đưa PDF/HTML thô vào `data/`.

## 4. Format từng tài liệu `.md`

Mỗi file bắt đầu bằng YAML front matter, sau đó là nội dung đã làm sạch. Với K4, `doc_id`, `title`, `source_url`, `retrieved_at`, `document_version`, `audience` là bắt buộc.

```md
---
doc_id: return-refund-deadline
title: Thời hạn đổi trả và hoàn tiền
source_url: https://example.com/policy/returns
retrieved_at: 2026-09-18
document_version: "not-stated" # dùng "not-stated" nếu nguồn không nêu
audience: buyer                 # buyer | seller | both
category: returns-policy
language: vi
---

# Thời hạn đổi trả và hoàn tiền

Nội dung đã làm sạch từ nguồn. Giữ lại các điều kiện, ngoại lệ và thời hạn
cần thiết để trả lời benchmark query.
```

- `doc_id` duy nhất, ổn định, không dấu; nên trùng tên file.
- `source_url` là URL trang/văn bản gốc, không phải link tìm kiếm.
- `retrieved_at` dùng định dạng `YYYY-MM-DD`; `document_version` là phiên bản/ngày hiệu lực, hoặc `not-stated` — **không bịa số hiệu**.
- Ngoài `audience`, thêm ít nhất một trường hữu ích cho lọc như `category`, `language`, `product_type`.
- Nếu một trang gộp thông tin cho cả `buyer` và `seller` (ví dụ điều khoản đổi trả áp dụng khác nhau cho hai bên trên cùng một trang), tách thành nhiều file — mỗi file một `audience` — để `search_with_filter()` có việc thật để lọc.
- Khi nạp vào `Document`, parse front matter vào `metadata` và chỉ dùng phần bên dưới làm `content`.

## 5. File kiểm kê `sources.csv`

Mỗi file có đúng một dòng, dùng header sau:

```csv
doc_id,file_path,title,source_url,retrieved_at,document_version,license_or_permission
return-refund-deadline,data/chinh-sach-doi-tra/thoi-han-hoan-tien.md,Thời hạn đổi trả và hoàn tiền,https://example.com/policy/returns,2026-09-18,not-stated,public-source
```

`license_or_permission` ghi căn cứ sử dụng, ví dụ `public-source`, `CC-BY-4.0`, hoặc `team-owned`.

## 6. Checklist trước benchmark

- [ ] Có 5–10 file cùng một chủ đề, `doc_id` không trùng.
- [ ] Mỗi file có đủ metadata bắt buộc (`doc_id`, `title`, `source_url`, `retrieved_at`, `document_version`, `audience`); `sources.csv` khớp một-một với file.
- [ ] `audience` có ít nhất 2 giá trị khác nhau trong bộ tài liệu (`buyer`/`seller`) — nếu chỉ một giá trị thì `metadata_filter` không có gì để lọc.
- [ ] URL là nguồn gốc, truy cập được, và dữ liệu không nhạy cảm.
- [ ] Cả 5 benchmark query đều kiểm chứng được từ corpus, và ít nhất một câu cần `metadata_filter={"audience": "buyer"}` (hoặc `"seller"`) mới trả lời đúng.

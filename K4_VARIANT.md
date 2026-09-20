# Biến thể K4-L3B — Truy xuất Chính sách Thương mại Điện tử

L3B dùng chung cam kết mã nguồn cốt lõi (core coding contract) với L3A, nhưng Giai đoạn 2 (Phase 2) phải xây dựng cơ sở tri thức (knowledge base) về **chính sách đổi trả, bảo hành, hoặc quy định người bán/người mua** trên nền tảng thương mại điện tử.

> Lớp song song L3A cùng bài học này crawl chủ đề **dịch vụ/quy định đại học** thay vì thương mại điện tử — hai lớp thu thập dữ liệu khác nhau nhưng cùng ràng buộc kỹ thuật và cùng rubric chấm điểm bên dưới.

## Quy tắc riêng của L3B

- Mỗi tài liệu (document) phải có metadata `audience` (`buyer` / `seller` / `both`) và ít nhất một trường (field) hữu ích khác (`category`, `language`...).
- Ngoài `audience`, mỗi tài liệu phải có `source_url`, `retrieved_at` và `document_version`; chỉ dùng chính sách công khai hoặc được phép chia sẻ.
- Trong 5 câu hỏi đánh giá (benchmark query), có ít nhất một câu hỏi cần `metadata_filter={"audience": "buyer"}` (hoặc `"seller"`) để tránh lấy tài liệu dành cho đối tượng khác.
- Ít nhất một thành viên thử chia nhỏ (chunking) theo tiêu đề/mục (heading/section) của điều khoản/chính sách gốc.
- Câu trả lời chuẩn (Gold answer) phải trích được từ tài liệu nhóm thu thập, không suy đoán chính sách của nền tảng.

Thư mục `data/ecommerce/` có dữ liệu khởi động nhỏ; nhóm vẫn cần bổ sung tập tài liệu (corpus) 5–10 tài liệu theo yêu cầu Lab.

# Ghi chú về Vector Store

Vector store là một cơ sở dữ liệu hoặc lớp lưu trữ được thiết kế để giữ các embeddings và truy xuất các mục tương tự nhất với vector câu hỏi (query vector). Trong các hệ thống AI thực tế, vector store thường được dùng để hỗ trợ tìm kiếm ngữ nghĩa, gợi ý, quy trình phân cụm (clustering), và hệ thống tạo văn bản tăng cường truy xuất (RAG).

## Quy trình làm việc Tiêu biểu

Một đường ống tìm kiếm vector phổ biến có 4 giai đoạn:

1. **Chia nhỏ tài liệu (Chunk documents)** thành các đơn vị nhỏ hơn để bảo toàn ý nghĩa.
2. **Nhúng từng đoạn (Embed each chunk)** thành một vector số học dày đặc (dense numerical vector).
3. **Lưu trữ vector và metadata** để các bản ghi có thể được tìm kiếm và lọc.
4. **Nhúng câu hỏi (Embed the query)** và xếp hạng các vector được lưu trữ theo độ tương tự.

Chất lượng của hệ thống truy xuất phụ thuộc rất lớn vào chất lượng của các đoạn (chunks). Nếu các đoạn quá nhỏ, chúng có thể mất đi ngữ cảnh và tạo ra các kết quả khớp không hoàn chỉnh. Nếu các đoạn quá lớn, chúng có thể chứa quá nhiều ý tưởng không liên quan và làm loãng đi độ liên quan ngữ nghĩa.

## Tầm quan trọng của Metadata

Metadata thường quan trọng không kém bản thân vector. Các nhóm thường lưu các trường như nguồn tài liệu, ngôn ngữ, tác giả, khu vực sản phẩm, ngày xuất bản, và mức độ kiểm soát truy cập. Khi một người dùng hỏi một câu hỏi về một lĩnh vực cụ thể, các bộ lọc metadata có thể thu narrow không gian tìm kiếm và cải thiện độ chính xác (precision).

Ví dụ, một trợ lý hỗ trợ có thể giới hạn truy xuất chỉ trong các hướng dẫn khắc phục sự cố công khai, trong khi một công cụ phân tích nội bộ có thể tìm kiếm các báo cáo kỹ thuật sau sự cố (postmortems) và tài liệu về sự cố. Bước lọc này làm giảm nhiễu và có thể ngăn ứng dụng hiển thị văn bản từ phòng ban sai hoặc tài liệu lỗi thời.

## Rủi ro Phổ biến

Vector store rất mạnh mẽ, nhưng việc truy xuất không tự nhiên mà chính xác. Chia nhỏ (chunking) kém, embeddings chất lượng thấp, thiếu metadata, và thực hành đánh giá yếu đều có thể gây ra kết quả sai lệch. Một hệ thống có thể truy xuất những đoạn văn gần nhau về ngữ nghĩa nhưng không thực sự hữu ích cho tác vụ của người dùng.

Đó là lý do các nhóm nên kiểm thử chất lượng truy xuất bằng các câu hỏi thực tế, so sánh tìm kiếm có lọc so với không lọc, và kiểm tra các đoạn văn bản (chunks) thực sự được hệ thống trả về. Việc truy xuất tốt là kết quả của khâu chuẩn bị dữ liệu cẩn thận, chứ không chỉ là việc chọn cơ sở dữ liệu.

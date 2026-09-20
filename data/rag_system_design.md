# Thiết kế Hệ thống RAG cho Trợ lý Tri thức Nội bộ

## Bối cảnh

Một nhóm sản phẩm muốn một trợ lý có thể trả lời các câu hỏi về việc giới thiệu (onboarding), quy trình triển khai, sở hữu dịch vụ, và các bước khắc phục sự cố. Công ty đã có sẵn tài liệu rải rác trên các sổ tay markdown, sổ tay kỹ thuật (runbooks), và ghi chú hỗ trợ, nhưng nhân viên lãng phí thời gian tìm kiếm trên các thư mục không liên kết với nhau.

## Mục tiêu

Xây dựng một hệ thống tạo văn bản tăng cường truy xuất (retrieval-augmented generation - RAG) để tìm các tài liệu nội bộ có liên quan trước khi đưa ra câu trả lời. Trợ lý nên giảm thiểu sự ảo giác (hallucinations) bằng cách căn cứ phản hồi của nó trên văn bản truy xuất được và nên phân biệt rõ ràng giữa ngữ cảnh được truy xuất và phần tổng hợp tự tạo.

## Kiến trúc Đề xuất

Đường ống thu thập (ingestion pipeline) đọc các file markdown và text từ các thư mục đáng tin cậy, chia nhỏ chúng thành các đoạn (segments) mạch lạc về ngữ nghĩa, và lưu trữ các đoạn đó cùng với metadata. Mỗi bản ghi được lưu trữ bao gồm đường dẫn nguồn, mã định danh tài liệu, loại tài liệu, và phòng ban. Lớp truy xuất sẽ embed các câu hỏi của người dùng, thực hiện tìm kiếm tương tự (similarity search), và tùy chọn áp dụng các bộ lọc metadata khi câu hỏi được thu hẹp trong phạm vi một nhóm cụ thể.

Lớp ứng dụng lấy các đoạn (chunks) truy xuất được tốt nhất và xây dựng một lời nhắc (prompt) hướng dẫn mô hình ngôn ngữ chỉ trả lời từ các bằng chứng được cung cấp. Nếu kết quả truy xuất yếu hoặc mâu thuẫn, trợ lý nên nói rõ điều đó thay vì giả vờ rằng câu trả lời đã hoàn chỉnh.

## Kế hoạch Đánh giá

Nhóm nên đo lường chất lượng truy xuất bằng các câu hỏi thực tế của nhân viên như "Làm thế nào để triển khai billing API?" hoặc "Ai sở hữu dịch vụ checkout?" Thành công không chỉ là việc câu trả lời nghe trôi chảy hay không, mà là liệu bằng chứng được truy xuất có liên quan, có thể truy vết, và cập nhật hay không.

Một kế hoạch kiểm thử hữu ích bao gồm so sánh các chiến lược chia nhỏ (chunking), kiểm tra xem các bộ lọc metadata có cải thiện độ liên quan không, và ghi chép lại các trường hợp thất bại. Ví dụ về các trường hợp thất bại có thể bao gồm tài liệu lỗi thời được xếp hạng cao hơn sổ tay hiện tại, các đoạn nhỏ làm mất các lưu ý quan trọng, hoặc nội dung đa ngôn ngữ làm rối mô hình embedding.

## Lưu ý Vận hành

Khi tập tài liệu tăng lên, nhóm nên theo dõi hành vi index lại, việc xóa tài liệu, và độ mới của nguồn. Hệ thống cũng nên ghi log lại các đoạn nào đã được truy xuất để người đánh giá có thể xem xét tại sao một câu trả lời nhất định được tạo ra. Vòng lặp phản hồi đó là thiết yếu để cải thiện cả dữ liệu và chiến lược đưa ra câu lệnh (prompting strategy).

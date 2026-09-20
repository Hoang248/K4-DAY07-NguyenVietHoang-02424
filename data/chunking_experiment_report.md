# Báo cáo Thử nghiệm Chia nhỏ văn bản (Chunking Experiment Report)

## Mục đích

Báo cáo này tóm tắt một thử nghiệm nhỏ so sánh chia nhỏ theo kích thước cố định (fixed-size chunking), chia nhỏ theo câu (sentence-based chunking), và chia nhỏ đệ quy (recursive chunking) trên tài liệu nội bộ. Mục tiêu là để hiểu ranh giới chia nhỏ (chunk boundaries) ảnh hưởng thế nào đến chất lượng truy xuất, khả năng bảo toàn ngữ cảnh, và tính hữu ích của các đoạn văn bản được trả về.

## Chia nhỏ kích thước cố định (Fixed-Size Chunking)

Chia nhỏ theo kích thước cố định rất dễ lập trình và tạo ra số lượng chunk có thể dự đoán được. Nó hoạt động khá tốt cho các tài liệu kỹ thuật dài vì mỗi chunk đều nằm dưới một kích thước mục tiêu. Tuy nhiên, một số chunk lại cắt ngang các phần giải thích ở những chỗ bất hợp lý, đặc biệt là khi một quy trình kéo dài qua nhiều câu. Trong những trường hợp đó, kết quả tìm kiếm đôi khi trả về một đoạn có chứa từ khóa nhưng lại thiếu mất hướng dẫn thực tế.

## Chia nhỏ theo câu (Sentence-Based Chunking)

Chia nhỏ theo câu cải thiện khả năng đọc vì mỗi chunk khớp với ranh giới ngôn ngữ tự nhiên. Điều này giúp việc kiểm tra thủ công dễ dàng hơn và thường tạo ra kết quả truy xuất mạch lạc hơn cho các tài liệu chính sách ngắn và FAQ (Câu hỏi thường gặp). Nhược điểm là kích thước các chunk trở nên kém nhất quán hơn, và một số phần nội dung dày đặc vẫn vượt quá độ dài embedding lý tưởng khi quá nhiều câu dài được gộp lại với nhau.

## Chia nhỏ đệ quy (Recursive Chunking)

Chia nhỏ đệ quy mang lại sự cân bằng tốt nhất trong thử nghiệm. Đầu tiên nó cố gắng cắt ở các ranh giới cấu trúc lớn hơn như đoạn văn, sau đó mới dùng đến các dấu phân cách nhỏ hơn khi cần thiết. Kết quả là, hầu hết các chunk giữ được ngữ cảnh trong khi vẫn nằm trong khoảng kích thước mục tiêu. Đối với dữ liệu được thử nghiệm, chia nhỏ đệ quy tạo ra các đoạn văn bản hữu ích nhất quán nhất cho việc trả lời câu hỏi ở bước sau.

## Kết luận

Thử nghiệm cho thấy không có một chiến lược chung nào là tốt nhất, nhưng chia nhỏ đệ quy là một lựa chọn mặc định tốt cho tài liệu kỹ thuật hỗn hợp. Các nhóm vẫn nên xác thực giả định này bằng các câu hỏi thực tế của riêng họ, bởi vì chất lượng truy xuất phụ thuộc vào cả văn phong tài liệu và loại câu hỏi mà người dùng thực sự đặt ra.

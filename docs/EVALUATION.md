# Tiêu chí Đánh giá (Evaluation Metrics) cho Lab 7: Embedding & Vector Store

Trong lab này, chúng ta không chỉ hỏi "Nó chạy không?" mà hỏi **"Chất lượng truy xuất (Retrieval quality) tốt đến đâu?"**.

> Xem `docs/SCORING.md` để biết thang điểm (rubric) chấm điểm chính thức.

## Các Tiêu chí (Metric) Quan Trọng

### 1. Độ chính xác của Truy xuất (Retrieval Precision)

- **Độ liên quan Top-k (Top-k Relevance)**: Trong k kết quả trả về, bao nhiêu kết quả thực sự liên quan đến câu hỏi?
- **Phân bố Điểm (Score Distribution)**: Điểm tương tự (similarity score) có phân biệt rõ giữa kết quả tốt và kết quả nhiễu không?
- **Điểm Đánh giá (Benchmark Score)**: Mỗi câu hỏi 2 điểm — top-3 kết quả liên quan (relevant) + câu trả lời chính xác = 2, thiếu = 1/0.
- **Mục tiêu**: Top-3 kết quả (results) nên có ít nhất 2 kết quả liên quan trực tiếp.

### 2. Độ mạch lạc của Đoạn văn bản (Chunk Coherence)

- **Độ hoàn chỉnh ngữ nghĩa (Semantic Completeness)**: Đoạn văn bản (chunk) có giữ nguyên ý hoàn chỉnh hay bị cắt giữa câu/giữa ý?
- **Bảo toàn Ngữ cảnh (Context Preservation)**: Độ chồng chéo (overlap) có giúp giữ liên kết giữa các đoạn (chunks) không?
- **Đo lường**: So sánh số lượng đoạn (chunk count) và độ dài trung bình (avg_length) giữa 3 chiến lược, đánh giá chủ quan mức độ mạch lạc (coherent).

### 3. Tiện ích của Metadata (Metadata Utility)

- **Hiệu quả Lọc (Filter Effectiveness)**: Khi lọc theo metadata (danh mục, ngôn ngữ, ngày tháng), kết quả có chính xác hơn không?
- **Sự Đánh đổi Độ thu hồi (Recall Trade-off)**: Lọc (filter) quá chặt có làm mất kết quả tốt không?
- **Đo lường**: So sánh top-3 kết quả giữa `search()` và `search_with_filter()` trên cùng câu hỏi (query).

### 4. Chất lượng Căn cứ Dữ liệu (Grounding Quality)

- **Độ chính xác thực tế (Factual Accuracy)**: Câu trả lời của KnowledgeBaseAgent có dựa trên ngữ cảnh được truy xuất (retrieved context) hay tự bịa?
- **Khả năng Truy vết Nguồn (Source Traceability)**: Có thể chỉ ra đoạn (chunk) nào đã được dùng để trả lời không?
- **Đo lường**: Xác minh (verify) câu trả lời của tác tử (agent answer) với câu trả lời chuẩn (gold answer) trong đánh giá (benchmark).

### 5. Tác động của Chiến lược Dữ liệu (Data Strategy Impact)

- **Lựa chọn Tài liệu (Document Selection)**: Tài liệu có chủ đề rõ ràng, đủ nội dung để truy xuất (retrieval) có ý nghĩa?
- **Thiết kế Metadata (Metadata Design)**: Cấu trúc (schema) metadata có giúp lọc kết quả tốt hơn?
- **Cơ sở Chia nhỏ (Chunking Rationale)**: Chiến lược chia nhỏ (chunking strategy) có khai thác cấu trúc chủ đề (domain) không?
- **Đo lường**: So sánh điểm truy xuất (retrieval score) giữa các thành viên trong nhóm — cùng tài liệu, khác chiến lược.

## Cách Sử Dụng Tiêu chí (Metrics)

Các tiêu chí trên không yêu cầu tính toán phức tạp. Sinh viên nên:

1. **Quan sát có hệ thống**: Chạy cùng câu hỏi (query) với các cấu hình khác nhau, ghi lại kết quả
2. **So sánh A/B**: có lọc (filtered) so với không lọc (unfiltered), chiến lược A so với chiến lược B, tập dữ liệu X so với tập dữ liệu Y
3. **Giải thích tại sao**: Không chỉ ghi kết quả, mà giải thích nguyên nhân

Kết quả đánh giá nên được ghi trong báo cáo cá nhân (individual report) và báo cáo nhóm (group report).

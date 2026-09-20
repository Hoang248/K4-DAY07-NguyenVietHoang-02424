# Thang Điểm (Scoring Rubric) Lab 7: Embedding & Vector Store

Nhóm nộp **1 báo cáo nhóm** (`report/REPORT_NHOM.md` — phần nhóm, 40 điểm) và **mỗi sinh viên nộp 1 báo cáo cá nhân** (`report/REPORT_CANHAN.md` — phần cá nhân, 60 điểm).

> Tham khảo thêm `docs/EVALUATION.md` để xem các tiêu chí (metric) và góc nhìn đánh giá chất lượng truy xuất (retrieval quality).

---

## Điểm Cá Nhân (60 Điểm)

| Hạng mục | Mô tả | Điểm |
| :--- | :--- | :--- |
| **Hoàn thiện Code (Core Implementation)** | Vượt qua tất cả các bài kiểm thử (`pytest tests/ -v`) | 30 |
| **Hướng tiếp cận (My Approach)** | Giải thích cách lập trình từng phần trong gói `src` | 10 |
| **Kết quả Truy xuất (Competition Results)** | 5 câu hỏi đánh giá chạy trên mã nguồn cá nhân, cùng bộ câu hỏi với nhóm | 10 |
| **Khởi động (Warm-up)** | Giải thích độ tương tự cosine (cosine similarity) + bài toán chia nhỏ (chunking math) | 5 |
| **Dự đoán độ tương tự (Similarity Predictions)** | 5 cặp câu, dự đoán so với thực tế, phản ngẫm (reflection) | 5 |

---

## Điểm Nhóm (40 Điểm)

| Hạng mục | Mô tả | Điểm |
| :--- | :--- | :--- |
| **Thiết kế Chiến lược (Strategy Design)** | Giải thích chiến lược cá nhân + cơ sở (rationale) + so sánh với đường cơ sở (baseline) và với thành viên khác | 15 |
| **Chất lượng Bộ Tài liệu (Document Set Quality)** | 5-10 tài liệu có chủ đề rõ ràng, metadata hữu ích, nguồn minh bạch | 10 |
| **Chất lượng Truy xuất (Retrieval Quality)** | Độ chính xác trên 5 câu hỏi đánh giá (top-3 có chứa đoạn văn bản (chunk) liên quan) | 10 |
| **Thuyết trình (Demo)** | Trình bày chiến lược, so sánh trong nhóm, bài học rút ra | 5 |

### Cách Tính Điểm Chất lượng Truy xuất (Retrieval Quality) (10 điểm)

Nhóm thống nhất **5 câu hỏi đánh giá (benchmark queries)** kèm **câu trả lời chuẩn (gold answers)**. Mỗi thành viên chạy câu hỏi trên chiến lược riêng.

**Chấm mỗi câu hỏi (2 điểm/câu):**
- 2 điểm: Top-3 chứa đoạn (chunk) liên quan + câu trả lời của tác tử (agent answer) chính xác
- 1 điểm: Top-3 có đoạn liên quan nhưng câu trả lời thiếu chi tiết hoặc đoạn liên quan không ở top-1
- 0 điểm: Không truy xuất (retrieve) được đoạn liên quan trong top-3

---

## Tính Điểm Tổng

**Tổng = Cá Nhân (60) + Nhóm (40) = 100 Điểm Tối Đa**

> [!IMPORTANT]
> **Hai báo cáo, hai góc nhìn**: Báo cáo nhóm (`REPORT_NHOM.md`: lựa chọn tài liệu, chiến lược, câu hỏi đánh giá, demo) nộp chung 1 bản/nhóm. Báo cáo cá nhân (`REPORT_CANHAN.md`: hướng tiếp cận, kết quả, phản ngẫm) mỗi người nộp riêng vì mỗi người lập trình khác nhau.

> [!IMPORTANT]
> **Chiến lược (Strategy) > Hiệu suất (Performance)**: 15 điểm cho thiết kế chiến lược so với 10 điểm cho chất lượng truy xuất. Chúng tôi đánh giá cao khả năng **suy nghĩ và giải thích** hơn là điểm số thuần tuý.

> [!IMPORTANT]
> **Học từ nhau**: Mỗi thành viên thử chiến lược riêng trên cùng bộ tài liệu và cùng câu hỏi. So sánh kết quả trong nhóm giúp hiểu tại sao chiến lược A tốt hơn chiến lược B. Phần thuyết trình (demo) là cơ hội thảo luận với các nhóm khác về lựa chọn tài liệu, chiến lược và kết quả.

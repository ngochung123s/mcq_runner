# MedMCQ Pro Runner - Trình Thi Trắc Nghiệm Y Khoa & Quản Lý Ngân Hàng Đề

Ứng dụng Single-file HTML hiện đại, trực quan, chạy trực tiếp trên mọi trình duyệt web (Chrome, Edge, Firefox, Cốc Cốc, Safari điện thoại) mà không cần cài đặt Web Server, Node.js hay cơ sở dữ liệu.

## Giao diện mới và định dạng đề mở rộng

- **Giao diện mới:** CSS tự viết trong chính `index.html` (không còn Tailwind CDN), chạy đủ chức năng khi mở trực tiếp bằng `file://` và không cần mạng. Font Be Vietnam Pro tải khi có mạng, offline tự dùng Segoe UI / system-ui.
- **Sáng / tối:** nút ở góc phải thanh trên cùng; lựa chọn lưu ở khóa `medmcq_theme_v1`, lần đầu theo cài đặt hệ thống (`prefers-color-scheme`).
- **Bảng câu hỏi trên điện thoại:** hiện dạng ngăn kéo từ dưới lên, mở bằng nút "Bảng câu" ở thanh làm bài.
- **Giải thích từng đáp án:** nếu câu hỏi có `option_explanations` (mảng, mỗi phần tử ứng với một phương án), chế độ Tutor và trang Kết quả hiện lời giải ngay dưới từng phương án (đáp án đúng màu xanh, phương án sai bạn chọn màu đỏ, còn lại màu xám), kèm `explanation` tổng quát. Bộ đề cũ không có trường này vẫn chạy như trước.
- **Trường tùy chọn mới của câu hỏi:** `type` (`vignette` = Ca lâm sàng, `concept` = Khái niệm), `topic`, `difficulty` (1 Dễ, 2 Vừa, 3 Khó), `bloom`, `source`. Trang Kết quả có thêm bảng kết quả theo `topic`. Dấu xuống dòng `\n` trong `text` được giữ nguyên; dòng cuối được in đậm làm câu hỏi chính, các dòng trên là ca lâm sàng.
- **4 đến 6 phương án (A–F):** phím `1`–`6` hoặc `A`–`F` để chọn. Với câu 6 phương án, phím `F` chọn phương án F và gắn cờ chuyển thành `Shift`+`F`.
- **Bộ đề đi kèm:** file `data/bundled_banks.js` định nghĩa `window.MCQ_BUNDLED_BANKS = [bank, ...]`. Mỗi lần mở app, bộ đề chưa có (theo `id`) được thêm vào thư viện; bộ đề đã có sẽ được thay `title`, `description`, `questions`, `updated` khi bản đi kèm có `updated` mới hơn. Lịch sử làm bài không bị đụng tới. Thiếu file này app vẫn chạy bình thường.
- **Xuất TXT:** mỗi bộ đề có thêm nút xuất `.txt` theo mẫu `Câu N:` / `A.` / `Đáp án:` / `Giải thích:` (TXT không chứa giải thích từng đáp án, topic, độ khó; dùng JSON để giữ đủ). Nhập file JSON một bộ đề có trường mới sẽ giữ nguyên các trường đó khi lưu.

## 🌟 Tính Năng Nổi Bật

1. **Smart Auto-Parser (Nhập liệu tự nhiên bằng AI / Word):**
   - Không cần form nhập thủ công từng ô. Chỉ cần copy-paste văn bản câu hỏi dạng:
     ```text
     Câu 1: Bệnh Addison do tổn thương lớp nào của vỏ thượng thận?
     A. Lớp cầu
     B. Lớp bó
     C. Toàn bộ vỏ thượng thận
     D. Tủy thượng thận
     Đáp án: C
     Giải thích: Bệnh Addison là suy vỏ thượng thận nguyên phát...
     ```
   - Trình parser tự động nhận diện câu hỏi, các lựa chọn A, B, C, D, đáp án đúng và giải thích chi tiết.
   - Hỗ trợ xem trước (Preview) cấu trúc trước khi lưu.

2. **Hai Chế Độ Làm Bài Chuyên Nghiệp:**
   - **Luyện tập (Tutor Mode - phong cách UWorld/Amboss):** Chọn đáp án xong lập tức hiển thị Đúng/Sai kèm hộp giải thích lâm sàng chuyên sâu.
   - **Thi thử (Exam Mode):** Đồng hồ đếm thời gian thực, ẩn kết quả đến khi bấm "Nộp bài" để tính điểm chính xác và xếp loại.

3. **Công Cụ Hỗ Trợ Làm Bài:**
   - **Loại trừ đáp án (Strike-through):** Bấm biểu tượng `✕` bên cạnh đáp án để gạch ngang các phương án chắc chắn sai.
   - **Gắn cờ xem lại (Flag for review 🚩):** Đánh dấu câu còn phân vân để kiểm tra lại trước khi nộp.
   - **Question Matrix (Lưới điều hướng):** Trực quan hóa tiến độ làm bài, câu nào đã làm, câu nào gắn cờ, bấm vào ô để nhảy ngay đến câu đó.
   - **Phím tắt Pro:**
     - Phím `1, 2, 3, 4` hoặc `A, B, C, D`: Chọn đáp án.
     - Phím `→` (hoặc `N`): Sang câu tiếp theo.
     - Phím `←` (hoặc `P`): Về câu trước.
     - Phím `F`: Bật/tắt gắn cờ xem lại.

4. **Lưu Trữ & Quản Lý Dữ Liệu:**
   - Tự động lưu toàn bộ ngân hàng câu hỏi và lịch sử các lần thi vào `LocalStorage` của trình duyệt.
   - Hỗ trợ **Export JSON** (sao lưu 1 bộ đề hoặc toàn bộ ngân hàng câu hỏi).
   - Hỗ trợ **Import JSON / TXT** trực tiếp từ máy tính.
3. **Đồng Bộ Dữ Liệu Trực Tiếp Vào File Ổ Cứng (Direct File System Sync):**
   - Sử dụng công nghệ **File System Access API** hiện đại trên Chrome / Edge.
   - Cho phép chọn hoặc tạo một file `.json` duy nhất (ví dụ `medmcq_synced_database.json`) để làm database.
   - **Ghi đè 1 click / Tự động đồng bộ**: Mỗi khi bạn tạo thêm bộ câu hỏi mới, xóa đề hoặc hoàn thành bài thi, dữ liệu sẽ tự động ghi thẳng vào file trên ổ cứng mà không cần tải file lặp đi lặp lại.
   - Lưu file này vào thư mục OneDrive / Google Drive sẽ tự động đồng bộ sang các máy tính khác.

4. **Công Cụ Hỗ Trợ Làm Bài:**
   - **Loại trừ đáp án (Strike-through):** Bấm biểu tượng `✕` bên cạnh đáp án để gạch ngang phương án loại trừ.
   - **Gắn cờ xem lại (Flag for review 🚩):** Đánh dấu câu còn phân vân để kiểm tra lại trước khi nộp.
   - **Question Matrix (Lưới điều hướng):** Trực quan hóa tiến độ làm bài, câu nào đã làm, câu nào gắn cờ, bấm vào ô để nhảy ngay đến câu đó.
   - **Phím tắt Pro:**
     - Phím `1, 2, 3, 4` hoặc `A, B, C, D`: Chọn đáp án.
     - Phím `→` (hoặc `N`): Sang câu tiếp theo.
     - Phím `←` (hoặc `P`): Về câu trước.
     - Phím `F`: Bật/tắt gắn cờ xem lại.

5. **Lưu Trữ & Quản Lý Dữ Liệu:**
├── README.md                   # Tài liệu hướng dẫn sử dụng
└── data/
    ├── addison_sample.json     # Bộ đề mẫu JSON chuyên đề Bệnh Addison (8 câu)
    └── cushing_sample.txt      # File văn bản thô chuyên đề Hội chứng Cushing (4 câu)
```

## 🚀 Cách Mở & Sử Dụng

1. Nhấp đúp chuột vào file `index.html` trong thư mục `open_deep_research/mcq_runner/` để mở trên trình duyệt.
2. Hoặc kéo file `index.html` thả vào trình duyệt Chrome/Edge.
3. Ứng dụng đã được nạp sẵn bộ đề mẫu **Bệnh Addison & Tuyến Thượng Thận**. Bấm **"Làm bài"** để trải nghiệm ngay!

# MedMCQ Pro Runner - Trình Thi Trắc Nghiệm Y Khoa & Quản Lý Ngân Hàng Đề

Ứng dụng Single-file HTML hiện đại, trực quan, chạy trực tiếp trên mọi trình duyệt web (Chrome, Edge, Firefox, Cốc Cốc, Safari điện thoại) mà không cần cài đặt Web Server, Node.js hay cơ sở dữ liệu.

## Giao diện mới và định dạng đề mở rộng

- **Giao diện mới:** CSS tự viết trong chính `index.html` (không còn Tailwind CDN), chạy đủ chức năng khi mở trực tiếp bằng `file://` và không cần mạng. Font Be Vietnam Pro tải khi có mạng, offline tự dùng Segoe UI / system-ui.
- **Sáng / tối:** nút ở góc phải thanh trên cùng; lựa chọn lưu ở khóa `medmcq_theme_v1`, lần đầu theo cài đặt hệ thống (`prefers-color-scheme`).
- **Bảng câu hỏi trên điện thoại:** hiện dạng ngăn kéo từ dưới lên, mở bằng nút "Bảng câu" ở thanh làm bài.
- **Giải thích từng đáp án:** nếu câu hỏi có `option_explanations` (mảng, mỗi phần tử ứng với một phương án), chế độ Tutor và trang Kết quả hiện lời giải ngay dưới từng phương án (đáp án đúng màu xanh, phương án sai bạn chọn màu đỏ, còn lại màu xám), kèm `explanation` tổng quát. Bộ đề cũ không có trường này vẫn chạy như trước.
- **Trường tùy chọn mới của câu hỏi:** `type` (`vignette` = Ca lâm sàng, `concept` = Khái niệm), `topic`, `difficulty` (1 Dễ, 2 Vừa, 3 Khó), `bloom`, `source`. Trang Kết quả có thêm bảng kết quả theo `topic`. Dấu xuống dòng `\n` trong `text` được giữ nguyên; dòng cuối được in đậm làm câu hỏi chính, các dòng trên là ca lâm sàng.
- **4 đến 6 phương án (A–F):** phím `1`–`6` hoặc `A`–`F` để chọn. Với câu 6 phương án, phím `F` chọn phương án F và gắn cờ chuyển thành `Shift`+`F`.
- **Thư viện đề:** xem mục "Thư viện đề & quy trình nhập nhanh" bên dưới.
- **Xuất / nhập từng bộ đề:** nút tải xuống trên mỗi thẻ bộ đề xuất ra file `<id>.json` theo khuôn `medmcq-bank` (xem mục "Khuôn file bộ đề"), giữ đủ mọi trường. File này nhập lại vào app (kéo thả, hoặc nút "Tải từ file" ở tab Tạo / Nhập đề, chọn được nhiều file) hay thả thẳng vào `data/` đều được. TXT chỉ còn dùng để **nhập/dán** câu hỏi, không còn nút xuất TXT.

## Thư viện đề & quy trình nhập nhanh

**Thêm đề mới (không cần mở app):**
1. Thả file bộ đề `<id>.json` (khuôn `medmcq-bank`) vào thư mục `data/`. Mỗi file là đúng một bộ đề, tên file trùng `id`.
2. Nhấp đúp `CAP_NHAT.bat`: nó chạy `tools/build_library.py` để kiểm tra từng file và dựng lại `data/library.js`, rồi sao lưu (git commit + push) lên GitHub. File nào sai khuôn thì script liệt kê lỗi từng câu và dừng, thư viện cũ giữ nguyên.
3. Mở `index.html`: bộ đề mới tự xuất hiện. Thư viện nằm trong bộ nhớ, chỉ đọc, **không** sao chép vào LocalStorage nên không tốn dung lượng. Thiếu `data/library.js` app vẫn chạy (chỉ còn đề tự nhập).

**Trong app:**
- **Ngân hàng đề theo chuyên khoa:** các bộ đề gom thành mục có thể thu gọn (Nhi khoa, Nội khoa, Sản phụ khoa, Ngoại khoa, Khác, Đề tự nhập), sắp theo mã bài (IM-7b < IM-12 < IM-53b). Mỗi thẻ hiện mã bài, số câu, điểm và ngày lần làm gần nhất. Tìm kiếm có phím tắt `/`; bộ lọc: Tất cả / Chưa làm / Đang làm dở / Có câu sai.
- **Làm ngay 1 cú bấm:** nút **Luyện** (tutor) và **Thi** (exam) bắt đầu liền theo tùy chọn đã nhớ (`medmcq_prefs_v1`: xáo câu, xáo đáp án, số câu). Biểu tượng bánh răng mở bảng tùy chọn, có thêm mục **Số câu** (Tất cả / 10 / 20 / 40 / tự nhập).
- **Tiếp tục bài đang làm dở:** mỗi thao tác (chọn đáp án, gạch đáp án, gắn cờ, chuyển câu) tự lưu vào `medmcq_session_v1` (chỉ lưu mã câu + thứ tự đáp án + câu trả lời, vài KB). Mở lại app sẽ có thanh "Đang làm dở: … — câu x/y" với **Tiếp tục** / **Bỏ**; đồng hồ chạy tiếp từ thời gian đã làm. Nộp bài hoặc bấm nút thoát trong bài thì xóa phiên đã lưu. Nếu đề đã đổi và không còn câu nào đó, phiên bị bỏ kèm thông báo.
- **Ôn câu sai:** với mỗi câu, kết quả lần làm gần nhất (kể cả trong bài ôn/trộn) quyết định có "cần ôn" không (sai hoặc bỏ trống). Thẻ bộ đề hiện **Ôn n câu sai**; đầu trang có **Ôn tất cả câu sai (N)** gom câu của mọi bộ. Làm đúng thì câu rời khỏi danh sách ôn.
- **Trộn đề:** mỗi mục chuyên khoa có nút **Trộn 20 câu** (thi thử 20 câu ngẫu nhiên của nhóm). Nút **Chọn nhiều để trộn** cho tick nhiều bộ rồi bấm "Trộn n bộ — X câu" để chọn số câu và chế độ. Lịch sử hiện các bài này với tên "Trộn …" / "Ôn câu sai", và **Làm lại** chạy đúng bộ câu đó.
- **Nhập đề không cần bấm gì:** kéo thả file bộ đề `.json` (khuôn `medmcq-bank`) hoặc `.txt` theo mẫu `Câu N:` vào cửa sổ, hoặc dán (`Ctrl+V`) nội dung câu hỏi khi đang ở tab Ngân hàng đề, rồi đặt tên và lưu. Có thông báo "Đã nhập n bộ (m câu)" kèm **Hoàn tác**. JSON kiểu khác (file gộp nhiều bộ, file sao lưu cũ) bị từ chối kèm lý do. Bộ nhập có `id` trùng với đề thư viện sẽ được cấp `id` mới. Tab "Tạo / Nhập đề" vẫn dùng để soạn tay.
- **Xóa = ẩn với đề thư viện:** biểu tượng mắt gạch trên thẻ thư viện ẩn bộ đề khỏi danh sách; nút **Đã ẩn (n)** để hiện lại. Bộ ẩn chỉ tự hiện lại khi thư viện có bản `updated` mới hơn. Đề tự nhập thì xóa hẳn như trước.
- **Sao lưu / đồng bộ file** chỉ ghi đề tự nhập + lịch sử (đề thư viện đã nằm trong `data/` và Git). Khi một bộ vừa có trong thư viện vừa có bản tự nhập, app hiện bản có `updated` mới hơn (bằng nhau thì ưu tiên thư viện); bản lưu cũ trùng mã tự bị dọn khỏi LocalStorage ở lần mở đầu tiên.
- **Lưu ý dung lượng:** mỗi lần nộp bài, lịch sử lưu nguyên các câu hỏi của lần đó (bộ 60 câu có giải thích từng đáp án ≈ 90 KB). LocalStorage giới hạn ~5 MB, khi đầy app báo lỗi và không ghi được lịch sử mới; hãy xuất rồi xóa bớt lịch sử cũ.

## Khuôn file bộ đề (`medmcq-bank` v1)

Một file = một bộ đề, tên file `<id>.json`, mã hóa UTF-8. Luật kiểm tra nằm ở `tools/bank_format.py` (lúc build) và `BankFormat` trong `index.html` (lúc nhập/xuất); hai nơi phải giống nhau.

```json
{
  "format": "medmcq-bank",
  "version": 1,
  "id": "bank_ped40_hoi_chung_than_hu",
  "lesson": "PED-40",
  "group": "Nhi khoa",
  "title": "PED-40: Hội chứng thận hư nguyên phát ở trẻ em (40 câu ca lâm sàng)",
  "description": "Định nghĩa, sinh lý bệnh, chẩn đoán…",
  "updated": "2026-10-27T15:03:40Z",
  "questions": [
    {
      "id": "PED40-A01",
      "type": "vignette",
      "topic": "Chẩn đoán & sinh thiết",
      "subtopic": "…",
      "bloom": "phân tích",
      "difficulty": 3,
      "source": "PED-40 §0.2",
      "text": "Ca lâm sàng…\nCâu hỏi chính?",
      "options": ["…", "…", "…", "…"],
      "correct": 0,
      "explanation": "…",
      "option_explanations": ["…", "…", "…", "…"]
    }
  ]
}
```

- **Bắt buộc ở bộ đề:** `format`, `version`, `id`, `lesson` (có thể `""`), `group` (`Nhi khoa`, `Nội khoa`, `Sản phụ khoa`, `Ngoại khoa`, `Khác`), `title`, `description` (có thể `""`), `updated` (ISO, vd `2026-10-29T08:00:00Z`; tăng mỗi lần sửa để app nhận bản mới), `questions`.
- **Bắt buộc ở câu hỏi:** `id` (duy nhất trong bộ; lịch sử làm bài bám theo id này, đừng đổi), `text`, `options` (2–6 chuỗi), `correct` (chỉ số đáp án đúng, đếm từ 0), `explanation`.
- **Tùy chọn:** `option_explanations` (đúng bằng số phương án), `type` (`vignette`, `concept`, `calc`), `topic`, `subtopic`, `bloom`, `difficulty` (1, 2, 3), `source`.
- Trường lạ ở bất kỳ cấp nào đều bị báo lỗi, để mọi file luôn cùng một khuôn.

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
   - **Xuất từng bộ đề** ra file `medmcq-bank` và **nhập** lại file đó hoặc file `.txt` / nội dung dán.
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

5. **Cấu trúc thư mục:**
```text
mcq_runner/
├── index.html                  # Toàn bộ app (HTML + CSS + JS)
├── CAP_NHAT.bat                # Kiểm tra + dựng thư viện, sao lưu lên GitHub
├── BUILD_APK.bat               # Build bản Android MedMCQ.apk
├── tools/
│   ├── bank_format.py          # Khuôn medmcq-bank v1 + luật kiểm tra
│   └── build_library.py        # data/<id>.json → data/library.js
├── android/                    # Project Android (WebView bọc index.html)
└── data/
    ├── <id>.json               # Mỗi bộ đề một file, khuôn medmcq-bank
    └── library.js              # Sinh tự động, đừng sửa tay
```

## 🚀 Cách Mở & Sử Dụng

1. Nhấp đúp chuột vào file `index.html` để mở trên trình duyệt.
2. Hoặc kéo file `index.html` thả vào trình duyệt Chrome/Edge.
3. Bộ đề mẫu **Bệnh Addison & Tuyến Thượng Thận** (nhóm "Khác") có sẵn trong thư viện. Bấm **"Luyện"** để làm ngay!

## 📱 Bản Android (APK)

- Nhấp đúp `BUILD_APK.bat`: dựng lại thư viện rồi build `MedMCQ.apk` (cùng thư mục). Chép sang điện thoại và mở để cài; cài đè giữ nguyên lịch sử làm bài.
- Không cần Android Studio: JDK 17, Android SDK và Gradle nằm trong `%LOCALAPPDATA%\Android`.
- APK chứa sẵn `index.html` + `data/library.js` lúc build, nên có đề mới thì build lại APK. Xuất bộ đề trên điện thoại sẽ mở hộp thoại "Lưu vào…"; đồng bộ file ổ cứng chỉ có trên Chrome/Edge máy tính.

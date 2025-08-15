Run websocket: 
`uvicorn main:app --reload`


---

### *KỊCH BẢN CHI TIẾT CHĂM SÓC KHÁCH HÀNG - XỬ LÝ LỖI GIAO DỊCH CHUYỂN TIỀN*

*Vai trò:* Nhân viên Chăm sóc Khách hàng (CSKH)
*Tình huống:* Khách hàng (KH) gọi đến thông báo giao dịch chuyển tiền không thành công.

---

#### *Phần 1: Chào hỏi và Tiếp nhận thông tin ban đầu*

*Mục tiêu:* Tạo sự tin tưởng, thể hiện sự đồng cảm và nắm bắt vấn đề chính của khách hàng.

*Nhân viên CSKH:*
"Dạ, Ngân hàng [Tên Ngân hàng] xin nghe. Em là [Tên nhân viên], em có thể hỗ trợ gì cho anh/chị ạ?"

*Khách hàng:*
"Chào em, anh/chị vừa thực hiện một giao dịch chuyển tiền nhưng bị lỗi/không thành công..."

*Nhân viên CSKH:*
"Dạ, em rất tiếc về sự cố anh/chị đang gặp phải. Để đảm bảo an toàn tài khoản và hỗ trợ kiểm tra thông tin chính xác nhất, anh/chị vui lòng cho em xin thông tin để xác minh chủ tài khoản ạ."

---

#### *Phần 2: Xác minh thông tin khách hàng*

*Mục tiêu:* Bảo mật thông tin và xác định đúng khách hàng đang yêu cầu hỗ trợ.

*Nhân viên CSKH:*
"Anh/chị vui lòng cung cấp giúp em:
1.  Họ và tên đầy đủ của chủ tài khoản.
2.  Số Chứng minh nhân dân/Căn cước công dân (CCCD) mà mình đã đăng ký với ngân hàng ạ."

(Sau khi khách hàng cung cấp, nhân viên đối chiếu nhanh trên hệ thống)

*Nhân viên CSKH:*
"Dạ, em đã xác nhận thông tin chính xác. Cảm ơn anh/chị. Bây giờ, em sẽ bắt đầu kiểm tra giao dịch bị lỗi cho mình ạ."

---

#### *Phần 3: Khai thác thông tin chi tiết về giao dịch lỗi*

*Mục tiêu:* Thu thập đầy đủ các dữ kiện cần thiết để khoanh vùng và xác định chính xác giao dịch cần tra soát. Hãy hỏi một cách tuần tự và rõ ràng.

*Nhân viên CSKH:*
"Để tìm đúng giao dịch và nguyên nhân lỗi, anh/chị vui lòng cung cấp thêm cho em một vài thông tin chi tiết sau ạ:"

| Thông tin cần hỏi | Lời thoại gợi ý |
|:---|:---|
| *Thời gian giao dịch* | "Anh/chị có thể cho em biết ngày và khoảng thời gian (giờ) mình thực hiện giao dịch được không ạ?" |
| *Số tiền giao dịch* | "Dạ, số tiền chính xác của giao dịch bị lỗi là bao nhiêu ạ?" |
| *Thông tin người nhận* | "Anh/chị chuyển tiền đến số tài khoản và ngân hàng nào ạ? Tên người nhận hiển thị là gì ạ?" |
| *Kênh giao dịch* | "Anh/chị thực hiện giao dịch này qua ứng dụng Mobile Banking, Internet Banking trên website hay tại quầy/ATM ạ?" |
| *Nội dung thông báo lỗi* | "Khi giao dịch không thành công, hệ thống có hiển thị thông báo lỗi cụ thể nào không ạ? Nếu có, anh/chị có thể đọc giúp em nội dung đó được không?" |
| *Tình trạng tài khoản* | "Anh/chị đã kiểm tra lại số dư tài khoản của mình chưa ạ? Hệ thống đã trừ tiền trong tài khoản của mình chưa ạ?" |

---

#### *Phần 4: Tổng kết và xác nhận lại thông tin*

*Mục tiêu:* Đảm bảo tất cả thông tin ghi nhận là chính xác trước khi tiến hành tra soát.

*Nhân viên CSKH:*
"Dạ, cảm ơn anh/chị đã cung cấp thông tin. Em xin phép được xác nhận lại các thông tin về giao dịch của mình như sau:"
*   *Tên người gửi:* [Họ tên khách hàng]
*   *Thời gian thực hiện:* Khoảng [Giờ] ngày [Ngày]
*   *Số tiền:* [Số tiền] VNĐ
*   *Người nhận:* [Tên người nhận], số tài khoản [Số tài khoản nhận], tại ngân hàng [Tên ngân hàng nhận].
*   *Tình trạng:* Giao dịch báo lỗi và tài khoản [đã bị trừ tiền/chưa bị trừ tiền].

"Các thông tin trên đã chính xác chưa ạ?"

(Chờ khách hàng xác nhận)

---

#### *Phần 5: Giải thích quy trình và hẹn thời gian xử lý*

*Mục tiêu:* Cung cấp cho khách hàng hướng xử lý tiếp theo và thời gian dự kiến để họ yên tâm chờ đợi.

*Nhân viên CSKH:*
"Dạ, cảm ơn anh/chị đã xác nhận. Hiện tại, em sẽ tiến hành lập yêu cầu tra soát giao dịch này cho mình. Theo quy định của ngân hàng, thời gian xử lý tra soát liên ngân hàng sẽ trong khoảng [ví dụ: 3-5 ngày làm việc]. Trong thời gian này, bộ phận xử lý của ngân hàng sẽ làm việc với ngân hàng đối tác để xác định tình trạng giao dịch."

*Tùy vào tình huống, có thể tư vấn thêm:*
*   *Nếu tiền chưa trừ:* "Trường hợp này tiền vẫn còn trong tài khoản của anh/chị. Anh/chị có thể thử thực hiện lại giao dịch. Tuy nhiên, em vẫn sẽ ghi nhận yêu cầu để kiểm tra nguyên nhân lỗi ạ."
*   *Nếu tiền đã trừ:* "Anh/chị hoàn toàn yên tâm, Ngân hàng sẽ xử lý để đảm bảo quyền lợi cho mình. Sau khi có kết quả, tiền sẽ được hoàn lại vào tài khoản của anh/chị hoặc chuyển thành công đến người nhận. Em sẽ gửi thông báo kết quả đến anh/chị qua tin nhắn SMS/email."

*Nhân viên CSKH:*
"Em đã ghi nhận yêu cầu của mình với mã số là [Cung cấp mã số tra soát]. Anh/chị vui lòng lưu lại mã này để tiện theo dõi ạ. Anh/chị còn cần em hỗ trợ thêm vấn đề nào khác không ạ?"

---

#### *Phần 6: Kết thúc cuộc gọi*

*Mục tiêu:* Kết thúc cuộc trò chuyện một cách chuyên nghiệp.

*Nhân viên CSKH:*
"Dạ, một lần nữa em rất xin lỗi về sự bất tiện này. Cảm ơn anh/chị đã liên hệ đến Ngân hàng [Tên Ngân hàng]. Em chào anh/chị ạ."

---

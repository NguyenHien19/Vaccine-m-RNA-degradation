Cài đặt: 
- Yêu cầu đã cài đặt Git. Mở Terminal, truy cập đến thư mục dự định để chứa source code, thực hiện lệnh:
  git clone //link github
- Nếu chưa cài đặt Git, truy cập vào đường link Github ở trên, chọn Code, chọn Download ZIP. Sau khi file Zip đã tải xong thì giải nén
- Cài đặt framework django và các thư viện cần thiết để website hoạt động
  pip install -r requirements.txt
- Kích hoạt Django để sử dụng website. Thực hiện lần lượt các lệnh sau:
	py manage.py migrate
	py manage.py runserver
- Mở trình duyệt web, truy cập đường dẫn: http://127.0.0.1:8000/predict  
Cách sử dụng :
- Link video demo sản phẩm: https://youtu.be/0nMfAfMXvTQ 
- Trang chủ của trang web sẽ có 3 trường để nhập nội dung là Sequence, Structure và Loop type và 2 trường mặc định là Sequence length và Length to score. Người dùng nhập nội dung tương ứng, sau đó chọn “Predict” để dự đoán.
- Sau đó, web sẽ hiển thị kết quả dự đoán, bao gồm 107 bản ghi tương ứng với 107 bazơ nitơ trong chuỗi. Mỗi bản ghi bao gồm 5 giá trị dự đoán. Ngoài ra, còn có biểu đồ biểu diễn phân phối số lượng bazơ nitơ trong chuỗi và phân phối các giá trị dự đoán dọc theo chuỗi
- Để quay trở lại trang web dự đoán, chọn “Back to predict” hoặc truy cập lại đường dẫn http://127.0.0.1:8000/predict.


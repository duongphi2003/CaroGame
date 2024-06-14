"""
Mô tả: Trò chơi Caro với giao diện đồ họa sử dụng Pygame và Pygame mixer cho âm thanh nền.

Cách hoạt động:
1. Chương trình khởi tạo các thành phần cần thiết của Pygame và Pygame mixer.
2. Menu chính hiển thị các tùy chọn: Chơi game, Chơi với AI, Cài đặt, Thoát.
3. Trong trò chơi, người chơi có thể chơi với nhau hoặc với AI, với luật thắng là 5 ô liên tiếp.
4. Có các cài đặt như bật/tắt âm nhạc nền và quay lại menu chính từ màn hình cài đặt.
5. Trò chơi có thời gian giới hạn cho mỗi lượt đi của người chơi.

Thư viện:
- pygame: Thư viện đồ họa chính.
- sys: Để thoát chương trình.
- time: Để theo dõi thời gian và xử lý thời gian.
- random: Để chọn ngẫu nhiên vị trí đặt quân cờ của AI.
- PIL (Python Imaging Library): Để xử lý ảnh GIF làm nền.

Biến:
- BOARD_SIZE: Kích thước của bàn cờ (số ô vuông).
- CELL_SIZE: Kích thước của mỗi ô vuông trên bàn cờ.
- window_size: Kích thước cửa sổ trò chơi.
- screen: Màn hình hiển thị chính.
- play_button, play_ai_button, settings_button, quit_button: Các nút bấm trong menu chính.
- WHITE, BLACK, DARK_GRAY, TOMATO: Các màu sắc sử dụng trong trò chơi.
- font_path, font_size, button_font_size: Đường dẫn và kích thước font chữ.
- font, button_font: Đối tượng font chữ.
- gif_image, frames: Đối tượng ảnh GIF và các frame của ảnh GIF.
- BOARD_WIDTH, BOARD_HEIGHT, SCREEN_SIZE: Kích thước của bàn cờ và màn hình.
- WIN_CONDITION: Điều kiện thắng (số quân cờ liên tiếp).
- background_image_path, icon_image_path, piece_image_path, player1_icon_path, player2_icon_path, settings_icon_path: Đường dẫn tới các tệp ảnh.

Hàm:
- draw_text_centered: Vẽ văn bản ở giữa một hình chữ nhật.
- draw_button: Vẽ nút bấm với văn bản.
- load_background, load_icon, load_pieces, load_player_icon: Các hàm tải ảnh và biểu tượng.
- Board: Lớp đại diện cho bàn cờ, với các phương thức vẽ bàn cờ, đặt quân cờ, và kiểm tra thắng.
- Player: Lớp đại diện cho người chơi, với các thuộc tính quân cờ, biểu tượng, và thời gian còn lại.
- Game: Lớp đại diện cho trò chơi, với các phương thức khởi tạo, đặt lại trò chơi, chuyển lượt chơi, AI di chuyển, chạy trò chơi, và hiển thị cài đặt.

Cách chạy:
1. Khởi động trò chơi bằng cách chạy file Python này.
2. Chọn các tùy chọn từ menu chính để bắt đầu trò chơi, chơi với AI, thay đổi cài đặt, hoặc thoát.
"""

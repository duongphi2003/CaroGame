# docstrings.py

board_doc = """
Class Board:
- size: int: Kích thước của bảng Caro.
- grid: list: Lưới chứa các nước đi của trò chơi.

Methods:
- reset(): Đặt lại lưới chơi.
- make_move(x, y, symbol): Thực hiện nước đi tại vị trí (x, y) với ký hiệu 'symbol'.
- check_winner(): Kiểm tra người chiến thắng.
"""

player_doc = """
Class Player:
- name: str: Tên của người chơi.
- symbol: str: Ký hiệu của người chơi (ví dụ: 'X' hoặc 'O').

Methods:
- make_move(board): Thực hiện nước đi của người chơi trên bảng.
"""

game_doc = """
Class Game:
- board: Board: Bảng chơi.
- players: list: Danh sách người chơi.
- current_turn: int: Lượt chơi hiện tại.

Methods:
- add_player(player): Thêm người chơi vào trò chơi.
- start(): Bắt đầu trò chơi.
- switch_turn(): Chuyển lượt chơi.
- is_over(): Kiểm tra trò chơi đã kết thúc hay chưa.
"""

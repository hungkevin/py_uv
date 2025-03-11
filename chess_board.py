class Piece:
    def __init__(self, color, piece_type):
        self.color = color  # 'white' 或 'black'
        self.type = piece_type  # 'king', 'queen', 'rook', 'bishop', 'knight', 'pawn'
        self.has_moved = False

class ChessBoard:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.current_player = 'white'
        self.initialize_board()

    def initialize_board(self):
        # 设置白方棋子
        piece_order = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook']
        for i in range(8):
            self.board[1][i] = Piece('white', 'pawn')
            self.board[0][i] = Piece('white', piece_order[i])

        # 设置黑方棋子
        for i in range(8):
            self.board[6][i] = Piece('black', 'pawn')
            self.board[7][i] = Piece('black', piece_order[i])

    def is_valid_move(self, from_pos, to_pos):
        from_row, from_col = from_pos
        to_row, to_col = to_pos

        # 检查是否超出边界
        if not (0 <= from_row <= 7 and 0 <= from_col <= 7 and
                0 <= to_row <= 7 and 0 <= to_col <= 7):
            return False

        piece = self.board[from_row][from_col]
        target = self.board[to_row][to_col]

        # 检查起始位置是否有棋子
        if not piece or piece.color != self.current_player:
            return False

        # 检查目标位置是否为己方棋子
        if target and target.color == piece.color:
            return False

        # 计算移动的距离
        row_diff = to_row - from_row
        col_diff = to_col - from_col

        # 根据不同棋子类型检查移动规则
        valid = False
        if piece.type == 'pawn':
            # 兵的移动规则
            direction = 1 if piece.color == 'white' else -1
            if not piece.has_moved:
                valid = (col_diff == 0 and row_diff == direction * 2) or \
                       (col_diff == 0 and row_diff == direction)
            else:
                valid = col_diff == 0 and row_diff == direction

            # 兵吃子规则
            if target:
                valid = abs(col_diff) == 1 and row_diff == direction

        elif piece.type == 'rook':
            # 车的移动规则
            valid = (row_diff == 0 or col_diff == 0) and \
                   self._is_path_clear(from_pos, to_pos)

        elif piece.type == 'knight':
            # 马的移动规则
            valid = (abs(row_diff), abs(col_diff)) in [(2, 1), (1, 2)]

        elif piece.type == 'bishop':
            # 相的移动规则
            valid = abs(row_diff) == abs(col_diff) and \
                   self._is_path_clear(from_pos, to_pos)

        elif piece.type == 'queen':
            # 后的移动规则
            valid = (row_diff == 0 or col_diff == 0 or
                    abs(row_diff) == abs(col_diff)) and \
                   self._is_path_clear(from_pos, to_pos)

        elif piece.type == 'king':
            # 王的移动规则
            valid = abs(row_diff) <= 1 and abs(col_diff) <= 1

        return valid

    def _is_path_clear(self, from_pos, to_pos):
        from_row, from_col = from_pos
        to_row, to_col = to_pos

        row_dir = 0 if to_row == from_row else (to_row - from_row) // abs(to_row - from_row)
        col_dir = 0 if to_col == from_col else (to_col - from_col) // abs(to_col - from_col)

        current_row, current_col = from_row + row_dir, from_col + col_dir
        while (current_row, current_col) != (to_row, to_col):
            if self.board[current_row][current_col]:
                return False
            current_row += row_dir
            current_col += col_dir
        return True

    def is_king_in_check(self, color):
        # 找到王的位置
        king_pos = None
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece.color == color and piece.type == 'king':
                    king_pos = (row, col)
                    break
            if king_pos:
                break

        # 检查对方所有棋子是否可以吃到王
        opponent_color = 'black' if color == 'white' else 'white'
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece.color == opponent_color:
                    if self.is_valid_move((row, col), king_pos):
                        return True
        return False

    def move_piece(self, from_pos, to_pos):
        if self.is_valid_move(from_pos, to_pos):
            piece = self.board[from_pos[0]][from_pos[1]]
            self.board[to_pos[0]][to_pos[1]] = piece
            self.board[from_pos[0]][from_pos[1]] = None
            piece.has_moved = True
            self.current_player = 'black' if self.current_player == 'white' else 'white'
            return True
        return False

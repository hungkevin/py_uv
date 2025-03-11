import pygame

class ChessUI:
    def __init__(self, screen, board):
        self.screen = screen
        self.board = board
        self.square_size = 100
        self.selected_piece = None
        self.selected_square = None
        self.valid_moves = []  # 用于存储当前选中棋子的有效移动位置
        self.piece_names = {
            'white': {
                'king': '王', 'queen': '后', 'rook': '车',
                'bishop': '相', 'knight': '马', 'pawn': '兵'
            },
            'black': {
                'king': '王', 'queen': '后', 'rook': '车',
                'bishop': '相', 'knight': '马', 'pawn': '兵'
            }
        }
        self.font = pygame.font.SysFont('SimHei', 50)

    def load_images(self):
        self.pieces_images = {}
        pieces = ['king', 'queen', 'rook', 'bishop', 'knight', 'pawn']
        colors = ['white', 'black']
        for piece in pieces:
            for color in colors:
                image_path = f"images/{color}_{piece}.png"
                # TODO: 加载棋子图片

    def draw(self):
        # 绘制棋盘
        for row in range(8):
            for col in range(8):
                # 绘制基本棋盘格
                color = (255, 206, 158) if (row + col) % 2 == 0 else (209, 139, 71)

                # 高亮选中的格子
                if (row, col) == self.selected_square:
                    color = (186, 202, 68)  # 选中的格子显示为浅绿色
                elif (row, col) in self.valid_moves:
                    color = (186, 186, 68)  # 可移动位置显示为浅黄色

                pygame.draw.rect(self.screen, color,
                               (col * self.square_size, row * self.square_size,
                                self.square_size, self.square_size))

                # 绘制棋子
                piece = self.board.board[row][col]
                if piece:
                    text_color = (255, 255, 255) if piece.color == 'white' else (0, 0, 0)
                    text = self.piece_names[piece.color][piece.type]
                    text_surface = self.font.render(text, True, text_color)
                    text_rect = text_surface.get_rect(center=(
                        col * self.square_size + self.square_size // 2,
                        row * self.square_size + self.square_size // 2
                    ))
                    self.screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            row = y // self.square_size
            col = x // self.square_size

            # 如果已经选中了一个棋子
            if self.selected_square:
                from_pos = self.selected_square
                to_pos = (row, col)

                # 尝试移动棋子
                if self.board.move_piece(from_pos, to_pos):
                    # 检查将军状态
                    if self.board.is_king_in_check(self.board.current_player):
                        print(f"警告：{self.board.current_player}方国王正在被将军！")

                # 无论移动是否成功，都清除选中状态
                self.selected_square = None
                self.valid_moves = []

            # 选择新的棋子
            else:
                piece = self.board.board[row][col]
                if piece and piece.color == self.board.current_player:
                    self.selected_square = (row, col)
                    # 计算所有可能的移动位置
                    self.valid_moves = self.calculate_valid_moves(row, col)

    def calculate_valid_moves(self, row, col):
        """计算指定位置棋子的所有合法移动位置"""
        valid_moves = []
        for to_row in range(8):
            for to_col in range(8):
                if self.board.is_valid_move((row, col), (to_row, to_col)):
                    valid_moves.append((to_row, to_col))
        return valid_moves

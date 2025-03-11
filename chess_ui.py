import pygame

class ChessUI:
    """棋盘界面类：负责处理所有的界面显示和用户交互"""
    def __init__(self, screen, board):
        # 游戏窗口对象
        self.screen = screen
        # 棋盘逻辑对象
        self.board = board
        # 每个格子的大小（像素）
        self.square_size = 100
        # 当前选中的棋子
        self.selected_piece = None
        # 当前选中的格子位置
        self.selected_square = None
        # 当前选中棋子的有效移动位置列表
        self.valid_moves = []
        # 设置中文棋子显示
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
        self.game_over = False
        self.winner = None
        self.font_large = pygame.font.SysFont('SimHei', 72)

    def load_images(self):
        """加载棋子图片（预留功能）"""
        self.pieces_images = {}
        pieces = ['king', 'queen', 'rook', 'bishop', 'knight', 'pawn']
        colors = ['white', 'black']
        for piece in pieces:
            for color in colors:
                image_path = f"images/{color}_{piece}.png"
                # TODO: 加载棋子图片

    def draw(self):
        """绘制整个棋盘和棋子"""
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

        # 如果游戏结束，显示胜利信息
        if self.game_over:
            # 创建半透明的遮罩
            overlay = pygame.Surface((800, 800))
            overlay.fill((0, 0, 0))
            overlay.set_alpha(128)
            self.screen.blit(overlay, (0, 0))

            # 显示胜利信息
            winner_text = f"{'白方' if self.winner == 'white' else '黑方'}胜利!"
            text_surface = self.font_large.render(winner_text, True, (255, 215, 0))  # 金色文字
            text_rect = text_surface.get_rect(center=(400, 350))
            self.screen.blit(text_surface, text_rect)

            # 显示重新开始提示
            restart_text = "按空格键开始新局"
            restart_surface = self.font.render(restart_text, True, (255, 255, 255))
            restart_rect = restart_surface.get_rect(center=(400, 450))
            self.screen.blit(restart_surface, restart_rect)

    def handle_event(self, event):
        """处理用户事件（鼠标点击）"""
        if self.game_over:
            # 游戏结束时，按空格键或鼠标点击可以重新开始
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE or \
               event.type == pygame.MOUSEBUTTONDOWN:
                # 重置游戏
                self.board.reset_board()
                self.game_over = False
                self.winner = None
                self.selected_square = None
                self.valid_moves = []
            return

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            row = y // self.square_size
            col = x // self.square_size

            # 如果已经选中了一个棋子
            if self.selected_square:
                from_pos = self.selected_square
                to_pos = (row, col)

                # 获取目标位置的棋子（如果有的话）
                target_piece = self.board.board[row][col]

                # 尝试移动棋子
                if self.board.move_piece(from_pos, to_pos):
                    # 立即检查是否吃掉了国王
                    if target_piece and target_piece.type == 'king':
                        self.game_over = True
                        self.winner = self.board.board[row][col].color
                    # 如果没有吃掉国王，则检查将军状态
                    elif self.board.is_king_in_check(self.board.current_player):
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
        """
        计算指定位置棋子的所有合法移动位置
        row: 行号
        col: 列号
        返回: 所有可能的移动位置列表
        """
        valid_moves = []
        for to_row in range(8):
            for to_col in range(8):
                if self.board.is_valid_move((row, col), (to_row, to_col)):
                    valid_moves.append((to_row, to_col))
        return valid_moves

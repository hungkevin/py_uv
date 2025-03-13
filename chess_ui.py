import pygame
import time

class ChessUI:
    """棋盘界面类：负责处理所有的界面显示和用户交互"""
    def __init__(self, screen, board):
        self.screen = screen
        self.board = board
        # 棋盘在窗口中的起始位置，为时间显示留出空间
        self.board_start_y = 50  # 修改顶部空间
        self.square_size = 50    # 从100改为50，缩小格子大小
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
        self.font = pygame.font.SysFont('SimHei', 28)  # 从50改为28
        self.game_over = False
        self.winner = None
        self.font_large = pygame.font.SysFont('SimHei', 30)  # 从36改为30
        self.timer_font = pygame.font.Font(None, 24)  # 从48改为24

        # 添加计时相关的属性
        self.white_time = 0  # 白方用时（秒）
        self.black_time = 0  # 黑方用时（秒）
        self.last_time = time.time()  # 上次更新时间
        self.game_active = True  # 游戏是否进行中

        # 添加颜色常量
        self.SELECTED_COLOR = (255, 255, 0, 128)  # 黄色，半透明
        self.VALID_MOVE_COLOR = (0, 255, 0, 76)   # 绿色，半透明
        self.selected_piece = None

    def load_images(self):
        """加载棋子图片（预留功能）"""
        self.pieces_images = {}
        pieces = ['king', 'queen', 'rook', 'bishop', 'knight', 'pawn']
        colors = ['white', 'black']
        for piece in pieces:
            for color in colors:
                image_path = f"images/{color}_{piece}.png"
                # TODO: 加载棋子图片

    def get_square_rect(self, row, col):
        """获取棋盘格子的矩形区域"""
        x = col * self.square_size
        y = row * self.square_size + self.board_start_y  # 加上顶部偏移
        return pygame.Rect(x, y, self.square_size, self.square_size)

    def get_board_position(self, mouse_pos):
        """将鼠标位置转换为棋盘位置"""
        x, y = mouse_pos
        y = y - self.board_start_y  # 减去顶部偏移
        row = y // self.square_size
        col = x // self.square_size
        if 0 <= row < 8 and 0 <= col < 8:
            return row, col
        return None

    def draw(self):
        # 填充背景色
        self.screen.fill((128, 128, 128))  # 使用灰色背景

        # 绘制时间信息，使用英文
        # 白方时间（左侧）
        white_text = f"WHITE: {self.format_time(self.white_time)}"
        white_surface = self.timer_font.render(white_text, True, (255, 255, 255))
        white_rect = white_surface.get_rect()
        white_rect.left = 10  # 调整左边距
        white_rect.top = 10   # 调整上边距
        self.screen.blit(white_surface, white_rect)

        # 黑方时间（右侧）
        black_text = f"BLACK: {self.format_time(self.black_time)}"
        black_surface = self.timer_font.render(black_text, True, (0, 0, 0))
        black_rect = black_surface.get_rect()
        black_rect.right = 390  # 调整到窗口宽度(400)减去边距(10)
        black_rect.top = 10     # 与白方计时器对齐
        self.screen.blit(black_surface, black_rect)

        # 绘制棋盘和棋子
        for row in range(8):
            for col in range(8):
                rect = self.get_square_rect(row, col)
                # 绘制基本棋盘格
                color = (255, 206, 158) if (row + col) % 2 == 0 else (209, 139, 71)

                # 高亮选中的格子
                if (row, col) == self.selected_square:
                    color = (186, 202, 68)  # 选中的格子显示为浅绿色
                elif (row, col) in self.valid_moves:
                    color = (186, 186, 68)  # 可移动位置显示为浅黄色

                pygame.draw.rect(self.screen, color, rect)

                # 绘制棋子
                piece = self.board.board[row][col]
                if piece:
                    text_color = (255, 255, 255) if piece.color == 'white' else (0, 0, 0)
                    shadow_color = (128, 128, 128)  # 灰色阴影
                    text = self.piece_names[piece.color][piece.type]

                    # 绘制阴影文字
                    shadow_surface = self.font.render(text, True, shadow_color)
                    shadow_rect = shadow_surface.get_rect(center=(
                        rect.x + self.square_size // 2 + 2,  # 阴影偏移2像素
                        rect.y + self.square_size // 2 + 2
                    ))
                    self.screen.blit(shadow_surface, shadow_rect)

                    # 绘制主要文字
                    text_surface = self.font.render(text, True, text_color)
                    text_rect = text_surface.get_rect(center=(
                        rect.x + self.square_size // 2,
                        rect.y + self.square_size // 2
                    ))
                    self.screen.blit(text_surface, text_rect)

        # 在绘制棋子之前，添加选中和移动提示的绘制
        if self.selected_piece:
            row, col = self.selected_piece
            # 绘制选中效果
            s = pygame.Surface((self.square_size, self.square_size))
            s.set_alpha(128)
            s.fill(self.SELECTED_COLOR)
            self.screen.blit(s, (col * self.square_size, row * self.square_size + self.board_start_y))

            # 绘制可移动位置
            valid_moves = self.board.get_valid_moves(row, col)
            for move in valid_moves:
                s = pygame.Surface((self.square_size, self.square_size))
                s.set_alpha(76)
                s.fill(self.VALID_MOVE_COLOR)
                self.screen.blit(s, (move[1] * self.square_size, move[0] * self.square_size + self.board_start_y))

        # 如果游戏结束，显示胜利信息
        if self.game_over:
            # 创建半透明的遮罩，覆盖整个窗口
            overlay = pygame.Surface((400, 450))  # 修改遮罩大小为当前窗口大小
            overlay.fill((0, 0, 0))
            overlay.set_alpha(128)
            self.screen.blit(overlay, (0, 0))

            # 显示胜利信息的位置调整
            winner_text = f"{'白方' if self.winner == 'white' else '黑方'}胜利!"
            text_surface = self.font_large.render(winner_text, True, (255, 215, 0))
            text_rect = text_surface.get_rect(center=(200, 200))  # 调整到窗口中心
            self.screen.blit(text_surface, text_rect)

            # 显示重新开始提示的位置调整
            restart_text = "点击任意位置开始新局"
            restart_surface = self.font.render(restart_text, True, (255, 255, 255))
            restart_rect = restart_surface.get_rect(center=(200, 250))  # 调整位置
            self.screen.blit(restart_surface, restart_rect)

    def handle_event(self, event):
        """处理用户事件（鼠标点击）"""
        if self.game_over:
            # 只响应鼠标点击来重新开始游戏
            if event.type == pygame.MOUSEBUTTONDOWN:
                # 重置游戏
                self.board.reset_board()
                self.game_over = False
                self.winner = None
                self.selected_square = None
                self.valid_moves = []
                self.reset_timers()
            return

        if event.type == pygame.MOUSEBUTTONDOWN:
            board_pos = self.get_board_position(event.pos)
            if board_pos is None:
                return
            row, col = board_pos

            if self.selected_piece is None:
                # 直接使用board数组访问棋子
                piece = self.board.board[row][col]
                if piece and piece.color == self.board.current_player:
                    self.selected_piece = (row, col)
            else:
                # 移动棋子
                from_row, from_col = self.selected_piece
                if self.board.move_piece((from_row, from_col), (row, col)):
                    # 检查是否吃掉国王
                    if self.board.is_king_captured(self.board.current_player):
                        self.game_over = True
                        self.winner = 'white' if self.board.current_player == 'black' else 'black'
                        self.game_active = False
                    self.selected_piece = None
                else:
                    # 如果移动失败，检查是否选择新棋子
                    piece = self.board.board[row][col]
                    if piece and piece.color == self.board.current_player:
                        self.selected_piece = (row, col)
                    else:
                        self.selected_piece = None

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

    def update_timer(self):
        if not self.game_active:
            return

        current_time = time.time()
        elapsed = current_time - self.last_time

        # 根据当前回合更新对应方的用时
        if self.board.is_white_turn:
            self.white_time += elapsed
        else:
            self.black_time += elapsed

        self.last_time = current_time

    def reset_timers(self):
        """重置计时器"""
        self.white_time = 0
        self.black_time = 0
        self.last_time = time.time()
        self.game_active = True

    def format_time(self, seconds):
        """将秒数转换为时:分:秒格式"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = int(seconds % 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

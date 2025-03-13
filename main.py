import pygame
from chess_board import ChessBoard
from chess_ui import ChessUI

class ChessGame:
    def __init__(self):
        # 初始化Pygame
        pygame.init()
        # 修改为合适的窗口大小
        self.screen = pygame.display.set_mode((400, 450))
        pygame.display.set_caption("国际象棋")

        # 创建棋盘逻辑对象
        self.board = ChessBoard()
        # 创建棋盘UI对象
        self.ui = ChessUI(self.screen, self.board)

def main():
    game = ChessGame()

    # 主游戏循环
    running = True
    while running:
        # 处理所有事件
        for event in pygame.event.get():
            # 如果点击关闭窗口，则退出游戏
            if event.type == pygame.QUIT:
                running = False
            # 如果按下空格键，重置游戏和计时器
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game.board.reset_board()
                    game.ui.reset_timers()
            # 处理棋盘上的鼠标事件
            game.ui.handle_event(event)

        # 更新计时器
        game.ui.update_timer()

        # 绘制棋盘和棋子
        game.ui.draw()

        # 更新屏幕显示
        pygame.display.flip()

    # 退出Pygame
    pygame.quit()

if __name__ == "__main__":
    main()
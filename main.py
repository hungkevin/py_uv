import pygame
from chess_board import ChessBoard
from chess_ui import ChessUI

def main():
    # 初始化Pygame
    pygame.init()
    # 修改窗口高度，增加顶部空间用于显示时间
    screen = pygame.display.set_mode((800, 900))  # 高度从800改为900
    # 设置窗口标题
    pygame.display.set_caption("国际象棋")

    # 创建棋盘逻辑对象
    board = ChessBoard()
    # 创建棋盘UI对象
    ui = ChessUI(screen, board)

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
                    board.reset_board()
                    ui.reset_timers()
            # 处理棋盘上的鼠标事件
            ui.handle_event(event)

        # 更新计时器
        ui.update_timer()

        # 绘制棋盘和棋子
        ui.draw()
        # 更新屏幕显示
        pygame.display.flip()

    # 退出Pygame
    pygame.quit()

if __name__ == "__main__":
    main()

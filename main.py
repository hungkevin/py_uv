import pygame
from chess_board import ChessBoard
from chess_ui import ChessUI

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("国际象棋")

    board = ChessBoard()
    ui = ChessUI(screen, board)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            ui.handle_event(event)

        ui.draw()
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()

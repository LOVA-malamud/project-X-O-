import pygame
import sys
import random

# --- Constants ---
WIDTH, HEIGHT = 400, 520  # Increased height to fit the scoreboard
LINE_WIDTH = 5
BOARD_SIZE = 3
SQUARE_SIZE = WIDTH // BOARD_SIZE
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 10
CROSS_WIDTH = 15
SPACE = SQUARE_SIZE // 4

# Colors
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)
TEXT_COLOR = (255, 255, 255)
WIN_LINE_COLOR = (200, 0, 0)
SCORE_COLOR = (255, 215, 0) # Gold color for the scoreboard

# Confetti Particle Class for the celebration effect
class Particle:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(-HEIGHT, 0)
        self.size = random.randint(4, 8)
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.speed = random.uniform(2, 5)

    def fall(self):
        self.y += self.speed
        if self.y > HEIGHT:
            self.y = random.randint(-50, -10)
            self.x = random.randint(0, WIDTH)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))

def draw_lines(screen):
    for i in range(1, BOARD_SIZE):
        # Vertical
        pygame.draw.line(screen, LINE_COLOR, (i * SQUARE_SIZE, 0), (i * SQUARE_SIZE, WIDTH), LINE_WIDTH)
        # Horizontal
        pygame.draw.line(screen, LINE_COLOR, (0, i * SQUARE_SIZE), (WIDTH, i * SQUARE_SIZE), LINE_WIDTH)

def draw_figures(screen, board):
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == 'X':
                # Draw X
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), CROSS_WIDTH)
            elif board[row][col] == 'O':
                # Draw O
                center = (int(col * SQUARE_SIZE + SQUARE_SIZE / 2), int(row * SQUARE_SIZE + SQUARE_SIZE / 2))
                pygame.draw.circle(screen, CIRCLE_COLOR, center, CIRCLE_RADIUS, CIRCLE_WIDTH)

def check_winner(board, sym):
    # Check rows, columns, and diagonals
    for r in range(BOARD_SIZE):
        if board[r][0] == board[r][1] == board[r][2] == sym: return [((0, r), (2, r))]
    for c in range(BOARD_SIZE):
        if board[0][c] == board[1][c] == board[2][c] == sym: return [((c, 0), (c, 2))]
    if board[0][0] == board[1][1] == board[2][2] == sym: return [((0, 0), (2, 2))]
    if board[0][2] == board[1][1] == board[2][0] == sym: return [((2, 0), (0, 2))]
    return None

def draw_winning_line(screen, line_coords):
    start_cell, end_cell = line_coords[0]
    start_pos = (start_cell[0] * SQUARE_SIZE + SQUARE_SIZE // 2, start_cell[1] * SQUARE_SIZE + SQUARE_SIZE // 2)
    end_pos = (end_cell[0] * SQUARE_SIZE + SQUARE_SIZE // 2, end_cell[1] * SQUARE_SIZE + SQUARE_SIZE // 2)
    pygame.draw.line(screen, WIN_LINE_COLOR, start_pos, end_pos, 10)

def is_tie(board):
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if board[r][col] == "": return False # This will cause an error due to 'col', fixing below
    return True

# Oops, found a tiny bug in my thinking above, let me fix is_tie properly
def is_tie_correct(board):
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if board[r][c] == "":
                return False
    return True

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Tic Tac Toe - Pro Edition')
    font = pygame.font.SysFont("Arial", 26, bold=True)
    small_font = pygame.font.SysFont("Arial", 16)
    clock = pygame.time.Clock()
    
    # Initialize scores
    x_score = 0
    o_score = 0
    
    board = [["" for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    player = 'X'
    game_over = False
    winner_line = None
    status_text = "Player X's Turn"
    confetti = [Particle() for _ in range(100)]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                if event.pos[1] < WIDTH:
                    row, col = event.pos[1] // SQUARE_SIZE, event.pos[0] // SQUARE_SIZE
                    if board[row][col] == "":
                        board[row][col] = player
                        winner_line = check_winner(board, player)
                        if winner_line:
                            status_text = f"Player {player} Wins!"
                            if player == 'X': x_score += 1
                            else: o_score += 1
                            game_over = True
                        elif is_tie_correct(board):
                            status_text = "It's a Tie!"
                            game_over = True
                        else:
                            player = 'O' if player == 'X' else 'X'
                            status_text = f"Player {player}'s Turn"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    board = [["" for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
                    player, game_over, winner_line = 'X', False, None
                    status_text = "Player X's Turn"
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        screen.fill(BG_COLOR)
        draw_lines(screen)
        draw_figures(screen, board)
        
        if winner_line:
            draw_winning_line(screen, winner_line)
            for p in confetti:
                p.fall()
                p.draw(screen)

        # Draw UI Text
        screen.blit(font.render(status_text, True, TEXT_COLOR), (20, WIDTH + 5))
        
        # Display the scoreboard
        score_display = f"Score: X - {x_score} | O - {o_score}"
        screen.blit(font.render(score_display, True, SCORE_COLOR), (20, WIDTH + 40))
        
        hint = "Press 'R' to Restart | 'Q' to Quit"
        screen.blit(small_font.render(hint, True, TEXT_COLOR), (20, WIDTH + 85))
        
        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()

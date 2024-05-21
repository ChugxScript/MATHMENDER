import pygame

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 200, 64)  # Optional for background (not used for tiles)
RED = (255, 0, 0)  # Color for tiles divisible by 7

# Define tile properties
TILE_SIZE = 50
TILE_MARGIN = 5

# Define font size and color for tile text and button text
FONT_SIZE = 22
FONT_COLOR = BLACK

# Create a Pygame window
pygame.init()
screen_width = 1280
screen_height = 850
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Math Scrabble")

# Load a font
font = pygame.font.Font(None, FONT_SIZE)

# Define the game board layout
board_rows = 15
board_cols = 15

# Calculate board dimensions based on tile size and margin
board_width = (TILE_SIZE + TILE_MARGIN) * board_cols
board_height = (TILE_SIZE + TILE_MARGIN) * board_rows

# Example tiles for Math Scrabble
tiles = [("0", 1), ("1", 1), ("2", 2), ("3", 2), ("4", 3), ("5", 3), ("6", 4), ("7", 4), ("8", 5), ("9", 5),
         ("+", 2), ("-", 3), ("x", 4), ("/", 5), ("=", 1), (".", 20)]

# Function to draw a single tile
def draw_tile(text, value, x, y, is_red):
    # Draw the black border (optional, can be removed)
    pygame.draw.rect(screen, BLACK, (x, y, TILE_SIZE, TILE_SIZE), 2)

    # Fill the tile with white or red based on divisibility
    color = WHITE if not is_red else RED
    pygame.draw.rect(screen, color, (x + 2, y + 2, TILE_SIZE - 4, TILE_SIZE - 4))

    # No longer render text (commented out)
    # tile_text = font.render(text, True, FONT_COLOR)
    # screen.blit(tile_text, (text_background_x, text_background_y))

# Main loop
running = True
while running:
    # ... (rest of the code for event handling, screen filling, etc.)

    # Draw the game board
    board_x = (screen_width - board_width) // 2
    board_y = (screen_height - board_height) // 2
    for row in range(board_rows):
        for col in range(board_cols):
            x = board_x + col * (TILE_SIZE + TILE_MARGIN)
            y = board_y + row * (TILE_SIZE + TILE_MARGIN)
            is_red = (row % 7 == 0) and (col % 7 == 0)
            draw_tile("", 0, x, y, is_red)  # Pass an empty string for text

    # ... (rest of the code)

# Quit Pygame
pygame.quit()

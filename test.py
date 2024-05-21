import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Define screen dimensions
screen_width = 1920
screen_height = 1080
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("MATHMENDER")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Define tile properties
TILE_SIZE = 60
TILE_MARGIN = 5

# Define font size and color for tile text and button text
FONT_SIZE = 22
FONT_COLOR = BLACK

# Load font
font = pygame.font.Font(None, FONT_SIZE)

# Define the game board layout
board_rows = 15
board_cols = 15

# Calculate board dimensions based on tile size and margin
board_width = (TILE_SIZE + TILE_MARGIN) * board_cols
board_height = (TILE_SIZE + TILE_MARGIN) * board_rows

# Define game states
STATE_MAIN_MENU = 0
STATE_GAME = 1
STATE_HOW_TO_PLAY = 2

# Current game state
current_state = STATE_MAIN_MENU

# Load images
# (Assuming you have the required images in the specified locations)
background_main_menu_img = pygame.image.load('images/background_main_menu.png')
background_game_img = pygame.image.load('images/background_game.png')
background_how_to_play_img = pygame.image.load('images/background_how_to_play.png')

play_button_img = pygame.image.load('images/play_button.png')
play_button_hover_img = pygame.image.load('images/play_button_hover.png')

how_to_play_button_img = pygame.image.load('images/how_to_play_button.png')
how_to_play_button_hover_img = pygame.image.load('images/how_to_play_button_hover.png')

quit_button_img = pygame.image.load('images/quit_button.png')
quit_button_hover_img = pygame.image.load('images/quit_button_hover.png')

# Define tile values
tile_number = {
    '1': 1, '2': 1, '3': 2, '4': 2, '5': 3,
    '6': 2, '7': 4, '8': 2, '9': 2, '0': 1,
    'blank': 0
}

tile_operator = {
    '+': 1, '-': 1, 'x': 2, '÷': 3, '^2': 3,
    '√': 3
}

tile_equal ={
    '=': 1
}

tile_values = {**tile_number, **tile_operator, **tile_equal}

# Initialize dragged tile position variables
dragged_tile_x = 0
dragged_tile_y = 0

# Initialize dragged tile variables
dragged_tile = None


# Function to draw a single tile
def draw_tile(text, value, x, y, is_red, is_special=False, is_green=False, is_blue=False, is_yellow=False, show_value=True):
    # Draw the black border
    pygame.draw.rect(screen, BLACK, (x, y, TILE_SIZE, TILE_SIZE), 2)

    # Fill the tile with appropriate color
    if is_special:
        color = YELLOW
    elif is_red:
        color = RED
    elif is_green:
        color = GREEN
    elif is_blue:
        color = BLUE
    elif is_yellow:
        color = YELLOW
    else:
        color = WHITE

    pygame.draw.rect(screen, color, (x + 2, y + 2, TILE_SIZE - 4, TILE_SIZE - 4))

    # Render the text
    text_surface = font.render(text, True, FONT_COLOR)
    # Calculate the position to center the text on the tile
    text_rect = text_surface.get_rect(center=(x + TILE_SIZE // 2, y + TILE_SIZE // 2))
    # Blit the text onto the screen
    screen.blit(text_surface, text_rect)

    # Render the value in smaller font at the lower right corner if show_value is True
    if show_value:
        small_font = pygame.font.Font(None, FONT_SIZE - 8)
        value_surface = small_font.render(str(value), True, FONT_COLOR)
        value_rect = value_surface.get_rect(bottomright=(x + TILE_SIZE - 5, y + TILE_SIZE - 5))
        screen.blit(value_surface, value_rect)

# Function to draw the player's tiles
def draw_player_tiles(tiles):
    tile_x = 100  # Move tiles to the left by setting a fixed position
    tile_y = screen_height - TILE_SIZE - TILE_MARGIN * 5

    for i, tile in enumerate(tiles):
        x = tile_x + i * (TILE_SIZE + TILE_MARGIN)
        if dragged_tile is not None and i == dragged_tile_index:
            continue
        draw_tile(tile, tile_values[tile], x, tile_y, False)

    # If a tile is being dragged, draw it separately
    if dragged_tile is not None:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        x = mouse_x - TILE_SIZE // 2
        y = mouse_y - TILE_SIZE // 2
        draw_tile(dragged_tile, tile_values[dragged_tile], x, y, False)

# Function to draw the main menu
def draw_main_menu():
    screen.blit(background_main_menu_img, (0, 0))

    play_button = draw_button(play_button_img, play_button_hover_img, screen_width // 2, screen_height // 2)
    how_to_play_button = draw_button(how_to_play_button_img, how_to_play_button_hover_img, screen_width // 2, screen_height // 2 + 100)
    quit_button = draw_button(quit_button_img, quit_button_hover_img, screen_width // 2, screen_height // 2 + 200)

    return play_button, how_to_play_button, quit_button

# Function to draw a button
def draw_button(img, hover_img, x, y):
    rect = img.get_rect(center=(x, y))
    
    if rect.collidepoint(pygame.mouse.get_pos()):
        screen.blit(hover_img, rect)
    else:
        screen.blit(img, rect)
    
    return rect

# Function to draw the game board
def draw_game_board():
    screen.blit(background_game_img, (0, 0))
    board_x = (screen_width - board_width) // 2 + 300  # to the right
    board_y = (screen_height - board_height) // 2 

    for row in range(board_rows):
        for col in range(board_cols):
            x = board_x + col * (TILE_SIZE + TILE_MARGIN)
            y = board_y + row * (TILE_SIZE + TILE_MARGIN)
            is_center = (row == board_rows // 2 and col == board_cols // 2)
            
            # Define specific green columns and rows
            is_green = (                (row == 0 and col in {3, 11}) or
                (row == 1 and col in {5, 9}) or
                (row == 3 and col in {0, 7, 14}) or
                (row == 5 and col in {1, 13}) or
                (row == 6 and col in {6, 8}) or
                (row == 7 and col in {3, 11}) or
                (row == 8 and col in {6, 8}) or
                (row == 9 and col in {1, 13}) or
                (row == 11 and col in {0, 7, 14}) or
                (row == 13 and col in {5, 9}) or
                (row == 14 and col in {3, 11})
            )

            is_blue = (
                (row == 2 and col in {4, 10}) or
                (row == 4 and col in {2, 6, 8, 12}) or 
                (row == 5 and col in {5, 9}) or
                (row == 6 and col in {4, 10}) or
                (row == 8 and col in {4, 10})or
                (row == 9 and col in {5, 9})or
                (row == 10 and col in {2, 6, 8, 12})or 
                (row == 12 and col in {4, 10}) 

            )
            
            is_yellow = (
                (row == 1 and col in {1, 13}) or
                (row == 2 and col in {2, 12}) or 
                (row == 3 and col in {3,11}) or
                (row == 4 and col in {4, 10}) or
                (row == 10 and col in {4, 10})or
                (row == 11 and col in {3, 11})or
                (row == 12 and col in {2,12})or 
                (row == 13 and col in {1, 13}) 

            )

            # Ensure top-left and bottom-right corners are red
            if (row == 0 and col == 0) or (row == board_rows - 1 and col == board_cols - 1):
                is_red = True
    
            # Ensure top-right and bottom-left corners are red
            elif (row == 0 and col == board_cols - 1) or (row == board_rows - 1 and col == 0):
                is_red = True
      
            elif row == col or row + col == board_rows - 1:
                is_red = False
            else:
                is_red = (row % 7 == 0) and (col % 7 == 0)
            
            draw_tile("", 0, x, y, is_red, is_center)

            if (row == 0 and col == 0) or (row == board_rows - 1 and col == board_cols - 1):
                is_red = True   

            if is_red:
                text_surface = font.render("test", True, BLACK)
                text_rect = text_surface.get_rect(center=(x + TILE_SIZE // 2, y + TILE_SIZE // 2))
                screen.blit(text_surface, text_rect)
         
            # Draw green tiles
            if is_green:
                pygame.draw.rect(screen, GREEN, (x + 2, y + 2, TILE_SIZE - 4, TILE_SIZE - 4))
                text_surface = font.render("2N", True, BLACK)
                text_rect = text_surface.get_rect(center=(x + TILE_SIZE // 2, y + TILE_SIZE // 2))
                screen.blit(text_surface, text_rect)
                
            if is_blue:
                pygame.draw.rect(screen, BLUE, (x + 2, y + 2, TILE_SIZE - 4, TILE_SIZE - 4))
                text_surface = font.render("2L", True, BLACK)
                text_rect = text_surface.get_rect(center=(x + TILE_SIZE // 2, y + TILE_SIZE // 2))
                screen.blit(text_surface, text_rect)

            if is_yellow:
                pygame.draw.rect(screen, YELLOW, (x + 2, y + 2, TILE_SIZE - 4, TILE_SIZE - 4))
                text_surface = font.render("2L", True, BLACK)
                text_rect = text_surface.get_rect(center=(x + TILE_SIZE // 2, y + TILE_SIZE // 2))
                screen.blit(text_surface, text_rect)

    # Draw the "Start" tile in the center
    center_tile_x = board_x + (board_cols // 2) * (TILE_SIZE + TILE_MARGIN)
    center_tile_y = board_y + (board_rows // 2) * (TILE_SIZE + TILE_MARGIN)
    draw_tile("Start", 0, center_tile_x, center_tile_y, False, True)


# Function to draw the "How to Play" screen
def draw_how_to_play():
    screen.blit(background_how_to_play_img, (0, 0))
    info_font = pygame.font.Font(None, 36)

    info_text = []

    for i, line in enumerate(info_text):
        text_surface = info_font.render(line, True, WHITE)
        text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height // 4 + i * 40))
        screen.blit(text_surface, text_rect)

def generate_random_tiles():
    operators = list(tile_operator.keys())
    numbers = list(tile_number.keys())
    equal_sign = list(tile_equal.keys())
    
    # Randomly select 2 operators
    random_operators = random.sample(operators, 2)
    # Randomly select 1 equal sign
    random_equal_sign = random.sample(equal_sign, 1)
    # Randomly select 6 numbers
    random_numbers = random.sample(numbers, 6)
    
    # Concatenate all the selected tiles
    tiles = random_operators + random_equal_sign + random_numbers
    
    return tiles

# Main loop
running = True
player_tiles = generate_random_tiles()
selected_tile = None
selected_tile_pos = None
dragged_tile = None  # Define dragged_tile here
dragging = False  # Define dragging here

# Main loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if current_state == STATE_GAME or current_state == STATE_HOW_TO_PLAY:
                    current_state = STATE_MAIN_MENU
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_pos = event.pos
                if current_state == STATE_MAIN_MENU:
                    play_button, how_to_play_button, quit_button = draw_main_menu()
                    if play_button.collidepoint(mouse_pos):
                        current_state = STATE_GAME
                    elif how_to_play_button.collidepoint(mouse_pos):
                        current_state = STATE_HOW_TO_PLAY
                    elif quit_button.collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit()
                elif current_state == STATE_GAME:
                    # Check if a tile is clicked
                    tile_x = 100  # Position of the first player tile
                    tile_y = screen_height - TILE_SIZE - TILE_MARGIN * 5
                    for i, tile in enumerate(player_tiles):
                        x = tile_x + i * (TILE_SIZE + TILE_MARGIN)
                        rect = pygame.Rect(x, tile_y, TILE_SIZE, TILE_SIZE)
                        if rect.collidepoint(mouse_pos):
                            selected_tile = tile
                            selected_tile_pos = i
                            dragged_tile = selected_tile  # Set dragged_tile here
                            dragged_tile_index = selected_tile_pos  # Set dragged_tile_index here
                            dragging = True
                            # Calculate the offset for smooth dragging
                            offset_x = mouse_pos[0] - x
                            offset_y = mouse_pos[1] - tile_y
                            break

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and dragging:  # Left mouse button and currently dragging
                dragging = False
                # Drop the tile on the game board
                mouse_pos = event.pos
                board_x = (screen_width - board_width) // 2 + 300
                board_y = (screen_height - board_height) // 2
                col = (mouse_pos[0] - board_x) // (TILE_SIZE + TILE_MARGIN)
                row = (mouse_pos[1] - board_y) // (TILE_SIZE + TILE_MARGIN)

                if 0 <= col < board_cols and 0 <= row < board_rows:
                    # Place the tile on the board (update your board state as needed)
                    player_tiles[dragged_tile_index] = 'blank'
                    dragged_tile = None
                    dragged_tile_index = None

                    # Get the value of the dropped tile
                    if selected_tile:
                        dragged_tile_value = tile_values[selected_tile]  # Retrieve the value of the dropped tile
                        print("Dropped tile value:", dragged_tile_value)

                        # Generate a new random tile to replace the dropped tile
                        if selected_tile in tile_number:  # If the dropped tile is a number
                            new_tile = random.choice([key for key, value in tile_number.items() if key != 'blank'])
                        elif selected_tile in tile_operator:  # If the dropped tile is an operation
                            new_tile = random.choice([key for key, value in tile_operator.items() if key != 'blank'])
                        else:  # If the dropped tile is an equal sign
                            new_tile = random.choice([key for key, value in tile_equal.items() if key != 'blank'])
                        
                        print("New tile:", new_tile)

                        # Find the first empty slot in the player's tile list
                        for i in range(len(player_tiles)):
                            if player_tiles[i] == 'blank':
                                player_tiles[i] = new_tile
                                print("Replacing with:", new_tile)
                                break

                    print("Updated player tiles:", player_tiles)



        elif event.type == pygame.MOUSEMOTION and dragging:
            # If currently dragging, move the selected tile with the mouse
            mouse_pos = event.pos
            tile_x = mouse_pos[0] - offset_x
            tile_y = mouse_pos[1] - offset_y

    # Clear the screen
    screen.fill(WHITE)

    # Draw based on the current state
    if current_state == STATE_MAIN_MENU:
        play_button, how_to_play_button, quit_button = draw_main_menu()
    elif current_state == STATE_GAME:
        draw_game_board()
        draw_player_tiles(player_tiles)
        # Draw the selected tile if dragging
        if dragged_tile:
            draw_tile(dragged_tile, tile_values[dragged_tile], pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], False)
    elif current_state == STATE_HOW_TO_PLAY:
        draw_how_to_play()

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()



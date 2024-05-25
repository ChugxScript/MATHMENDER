import pygame
import os
import random

### remove after dev
from game_state_manager import GameStateManager
###
class MathMender():
    def __init__(self, display, gameStateManager):
        pygame.init()
        self.display = display
        self.gameStateManager = gameStateManager
        self.FPS = 60
        self.clock = pygame.time.Clock()
        self.total_points = 0

        # define tile tile status
        self.START_TILE = (7, 7)
        self.GREEN_TILES = [
            (0, 3), (0, 11),
            (1, 5), (1, 9),
            (3, 0), (3, 7), (3, 14),
            (5, 1), (5, 13),
            (6, 6), (6, 8),
            (7, 3), (7, 11),
            (8, 6), (8, 8),
            (9, 1), (9, 13),
            (11, 0), (11, 7), (11, 14),
            (13, 5), (13, 9),
            (14, 3), (14, 11),
        ]
        self.BLUE_TILES = [
            (2, 4), (2, 10),
            (4, 2), (4, 6), (4, 8), (4, 12),
            (5, 5), (5, 9),
            (6, 4), (6, 10),
            (8, 4), (8, 10),
            (9, 5), (9, 9),
            (10, 2), (10, 6), (10, 8), (10, 12),
            (12, 4), (12, 10),
        ]
        self.YELLOW_TILES = [
            (1, 1), (1, 13),
            (2, 2), (2, 12),
            (3, 3), (3, 11),
            (4, 4), (4, 10),
            (10, 4), (10, 10),
            (11, 3), (11, 11),
            (12, 2), (12, 12),
            (13, 1), (13, 13),
        ]
        self.RED_TILES = [
            (0, 0), (0, 7), (0, 14),
            (7, 0), (7, 14),
            (14, 0), (14, 7), (14, 14),
        ]
        
        # colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.YELLOW = (255, 255, 0)
        self.CORAL = (218, 112, 214)

        # board details
        self.TILE_SIZE = 39
        self.TILE_MARGIN = 3
        self.FONT_SIZE = 15
        self.FONT_COLOR = self.BLACK

        # tile details
        self.TILE_NUMBER_POINTS = {
            '1': 1, '2': 1, '3': 2, '4': 2, '5': 3,
            '6': 2, '7': 4, '8': 2, '9': 2, '0': 1,
            'blank': 0
        }
        self.TILE_OPERATOR_POINTS = {
            '+': 1, '-': 1, 'x': 2, '÷': 3, 
            '^2': 5, '√': 5
        }
        self.TILE_EQUAL_POINTS = {
            '=': 1
        }
        # pieces each tiles
        self.TILE_PCS = {
            '1': 5, '2': 5, '3': 5, '4': 5, '5': 5,
            '6': 5, '7': 5, '8': 5, '9': 5, '0': 5,
            
            '+': 7, '-': 7, 'x': 5, '÷': 5, 
            '^2': 2, '√': 2,
            '=': 20, 'blank': 4,
        }

        # click click haha
        self.clicked_tile = None
        self.curr_equation = []

        # Define the game board grid
        self.curr_game_board = [[None for _ in range(15)] for _ in range(15)]
        self.game_board_details = [[None for _ in range(15)] for _ in range(15)]

    def run(self):
        self.load_assets()
        self.draw_bg()
        self.init_board()
        self.draw_pieces_pcs()
        self.get_player_pieces()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                
                # piece clicked
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        for piece in self.player_pieces:
                            if piece["rect"].collidepoint(mouse_x, mouse_y):
                                self.toggle_expand_tile(piece)
                                break

                # play pass buttons
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        for rect in self.rect_buttions:
                            if rect["rect_btn"].collidepoint(mouse_x, mouse_y):
                                print("Rectangle clicked:", rect["id"])
                                if rect["id"] == "play":
                                    print("play button clicked")
                                    if self.is_valid():
                                        print("Valid equation!")
                                        # Take appropriate action for a valid equation
                                    else:
                                        print("Invalid equation!")
                                        # Take appropriate action for an invalid equation
                                if rect["id"] == "pass":
                                    print("pass button clicked")

                # clickable board
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        self.handle_clicked_board_xy(pygame.mouse.get_pos(), "add_tile")
                    if event.button == 3:
                        self.handle_clicked_board_xy(pygame.mouse.get_pos(), "remove_tile")

            self.display.blit(self.math_mender_bg, (0, 0))
            self.init_board()
            self.draw_updated_board()
            self.draw_pieces_pcs()
            self.draw_player_pieces()
            self.draw_player_pieces_with_click()
            self.draw_rect_btn()
            self.calculate_total_points()
            self.draw_total_points()
            pygame.display.flip()
            self.clock.tick(self.FPS)
    
    def draw_bg(self):
        self.math_mender_bg = pygame.image.load(os.path.join(self.images_dir, "GAME_BG.png"))

    def init_board(self):
        for row in range(15):
            for col in range(15):
                tile_color = self.WHITE
                font_text = ''
                self.game_board_details[row][col] = ''

                if (row, col) in self.GREEN_TILES:
                    tile_color = self.GREEN
                    font_text = '3N'
                    self.game_board_details[row][col] = '3N'
                elif (row, col) in self.BLUE_TILES:
                    tile_color = self.BLUE
                    font_text = '2N'
                    self.game_board_details[row][col] = '2N'
                elif (row, col) in self.YELLOW_TILES:
                    tile_color = self.YELLOW
                    font_text = '2A'
                    self.game_board_details[row][col] = '2A'
                elif (row, col) in self.RED_TILES:
                    tile_color = self.RED
                    font_text = '3A'
                    self.game_board_details[row][col] = '3A'
                elif (row, col) == self.START_TILE:
                    tile_color = self.YELLOW
                    font_text = 'START'
                    self.game_board_details[row][col] = 'START'

                x = (col + 13) * (self.TILE_SIZE + self.TILE_MARGIN)
                y = (row + 0.3) * (self.TILE_SIZE + self.TILE_MARGIN)

                pygame.draw.rect(self.display, tile_color, (x, y, self.TILE_SIZE, self.TILE_SIZE))
                pygame.draw.rect(self.display, self.BLACK, (x, y, self.TILE_SIZE, self.TILE_SIZE), 1)

                if font_text:
                    text_surface = self.FONT.render(font_text, True, self.FONT_COLOR)
                    text_rect = text_surface.get_rect(center=(x + self.TILE_SIZE / 2, y + self.TILE_SIZE / 2))
                    self.display.blit(text_surface, text_rect)
    
    def draw_updated_board(self):
        for row in range(15):
            for col in range(15):
                piece = self.curr_game_board[row][col]
                if piece:
                    x = (col + 13) * (self.TILE_SIZE + self.TILE_MARGIN)
                    y = (row + 0.3) * (self.TILE_SIZE + self.TILE_MARGIN)

                    self.draw_tile(piece["tile"], piece["points"], x, y, self.CORAL)

    def handle_clicked_board_xy(self, pos, mode):
        x, y = pos
        col = int((x - 13 * (self.TILE_SIZE + self.TILE_MARGIN)) // (self.TILE_SIZE + self.TILE_MARGIN))
        row = int((y - 0.3 * (self.TILE_SIZE + self.TILE_MARGIN)) // (self.TILE_SIZE + self.TILE_MARGIN))
        
        # Check if col and row are within the board
        if 0 <= row < 15 and 0 <= col < 15:
            print("Clicked cell:", row, col)
            
            if mode == "add_tile":
                # Check if there is an expanded tile to be placed
                if self.clicked_tile:
                    # Place the expanded tile onto the game board if the cell is empty
                    if self.curr_game_board[row][col] is None:
                        # Create a copy of the clicked tile to modify its value
                        placed_tile = self.clicked_tile.copy()

                        # Store the original value
                        placed_tile["original_tile"] = placed_tile["tile"]

                        # Mark the tile as not fixed initially
                        placed_tile["fixed"] = False

                        # Adjust the tile value based on tile color, but not for the answer tile
                        if placed_tile["tile"] != '=':
                            # Remove the multiplication effect when landing on colored tiles
                            if (row, col) in self.GREEN_TILES or (row, col) in self.BLUE_TILES or \
                                    (row, col) in self.YELLOW_TILES or (row, col) in self.RED_TILES:
                                if placed_tile["tile"].isdigit():
                                    placed_tile["tile"] = str(int(placed_tile["tile"]))
                        
                        # Store the row and col in the placed tile
                        placed_tile["row"] = row
                        placed_tile["col"] = col

                        self.curr_game_board[row][col] = placed_tile
                        self.curr_equation.append(placed_tile)
                        # Print the current equation without problematic characters
                        print(f"\n>>curr_equation: {[piece['tile'] for piece in self.curr_equation if piece['tile'] not in ['√']]}")
                        # Remove the tile from player pieces
                        self.player_pieces.remove(self.clicked_tile)
                        # Reset expanded_tile
                        self.clicked_tile = None

            
            if mode == "remove_tile":
                # Create a list to store pieces to be removed
                pieces_to_remove = []
                for piece in self.curr_equation:
                    if self.curr_game_board[row][col] == piece and not piece.get("fixed", False):
                        # Restore the original value
                        if "original_tile" in piece:
                            piece["tile"] = piece["original_tile"]
                            del piece["original_tile"]
                        self.curr_game_board[row][col] = None
                        pieces_to_remove.append(piece)
                
                # Remove the pieces from curr_equation and add them back to player_pieces
                for piece in pieces_to_remove:
                    self.curr_equation.remove(piece)
                    self.player_pieces.append(piece)

        else:
            print("Clicked outside the board")

    def draw_pieces_pcs(self):
        x_offsets = [40, 110, 170, 230]
        y_offset = 190
        line_spacing = 20

        def draw_text(text, x, y):
            self.FONT_PCS = pygame.font.Font(None, 20)
            text_surface = self.FONT_PCS.render(text, True, self.WHITE)
            self.display.blit(text_surface, (x, y))

        def draw_column(items, x_offset, y_offset):
            y = y_offset
            for key, value in items:
                draw_text(f"[ {key} ]: {value}", x_offset, y)
                y += line_spacing
        
        # Prepare items to display in columns
        items = list(self.TILE_PCS.items())
        quarter = (len(items) + 3) // 4
        columns = [items[i * quarter:(i + 1) * quarter] for i in range(4)]

        # Draw each column
        for i, column in enumerate(columns):
            draw_column(column, x_offsets[i], y_offset)

    def get_player_pieces(self):
        
        operators = random.sample(list(self.TILE_OPERATOR_POINTS.keys()), 2)
        numbers = random.sample(list(self.TILE_NUMBER_POINTS.keys()), 6)
        equal_sign = random.sample(list(self.TILE_EQUAL_POINTS.keys()), 1)

        selected_tiles = equal_sign + numbers + operators

        self.player_pieces = []
        for tile in selected_tiles:
            piece = {
                "tile": tile,
                "points": self.TILE_NUMBER_POINTS.get(tile) or self.TILE_OPERATOR_POINTS.get(tile) or self.TILE_EQUAL_POINTS.get(tile) or 0,
                "rect": pygame.Rect(0, 0, self.TILE_SIZE, self.TILE_SIZE)
            }
            self.player_pieces.append(piece)
            if tile in self.TILE_PCS:
                self.TILE_PCS[tile] -= 1

        self.update_player_pieces_positions()

    def update_player_pieces_positions(self):
        x_offset = 40
        y_offset = 390
        for i, piece in enumerate(self.player_pieces):
            piece["rect"].x = x_offset + i * (self.TILE_SIZE + 10)
            piece["rect"].y = y_offset

    def draw_player_pieces(self):
        for piece in self.player_pieces:
            self.draw_tile(piece["tile"], piece["points"], piece["rect"].x, piece["rect"].y, self.CORAL)

    def draw_tile(self, tile, points, x, y, curr_color):
        tile_surface = pygame.Surface((self.TILE_SIZE, self.TILE_SIZE))
        tile_surface.fill(curr_color)
        pygame.draw.rect(tile_surface, self.CORAL, (2, 2, self.TILE_SIZE - 4, self.TILE_SIZE - 4))
        pygame.draw.rect(tile_surface, self.BLACK, (0, 0, self.TILE_SIZE, self.TILE_SIZE), 1)

        # Render the text
        text_surface = self.FONT.render(tile, True, self.BLACK)
        text_rect = text_surface.get_rect(center=(self.TILE_SIZE // 2, self.TILE_SIZE // 2))
        tile_surface.blit(text_surface, text_rect)

        # Render the value in smaller font at the lower right corner
        small_font = pygame.font.Font(None, self.FONT_SIZE)
        value_surface = small_font.render(str(points), True, self.RED)
        value_rect = value_surface.get_rect(bottomright=(self.TILE_SIZE - 5, self.TILE_SIZE - 5))
        tile_surface.blit(value_surface, value_rect)

        # Blit the tile surface onto the display
        self.display.blit(tile_surface, (x, y))
    
    def toggle_expand_tile(self, clicked_tile):
        if self.clicked_tile == clicked_tile:
            # If the clicked tile is already expanded, revert it
            self.clicked_tile = None
        else:
            # Otherwise, expand the clicked tile and revert the previously expanded tile
            self.clicked_tile = clicked_tile

    def draw_player_pieces_with_click(self):
        for piece in self.player_pieces:
            # Draw tile with click effect if it's the expanded tile
            if piece == self.clicked_tile:
                enlarged_rect = piece["rect"].inflate(5, 5)  
                self.draw_tile(piece["tile"], piece["points"], enlarged_rect.x, enlarged_rect.y, self.YELLOW)
            else:
                self.draw_tile(piece["tile"], piece["points"], piece["rect"].x, piece["rect"].y, self.CORAL)

    def draw_rect_btn(self):
        self.rect_buttions = [
            {"id": "play", "rect_btn": pygame.Rect(104, 530, 139, 45)},
            {"id": "pass", "rect_btn": pygame.Rect(265, 530, 139, 45)},
        ]

        for rect in self.rect_buttions:
            pygame.draw.rect(self.display, self.WHITE, rect["rect_btn"], 1)

    def get_ai_pieces(self):
        pass

    def is_valid(self):
        def evaluate_equation(equation):
            try:
                equation = equation.replace('x', '*').replace('÷', '/').replace('^2', '**2').replace('√', 'math.sqrt(')
                equation = equation.replace('math.sqrt(', 'math.sqrt(').replace('math.sqrt(', 'math.sqrt(')
                return eval(equation)
            except Exception as e:
                print(f"Error evaluating equation '{equation}': {e}")
                return None

        def check_equation(equation, answer_pos):
            if '=' in equation:
                left, right = equation.split('=')
                for num in range(10):
                    modified_left = left.replace('blank', str(num))
                    modified_right = right.replace('blank', str(num))
                    left_value = evaluate_equation(modified_left)
                    right_value = evaluate_equation(modified_right)
                    if left_value is not None and right_value is not None and left_value == right_value:
                        print(f"Valid equation with blank as {num}: {modified_left} == {modified_right}")
                        return True
                return False
            return False

        def extract_equation(row, col, direction):
            equation = ""
            answer_pos = None
            if direction == "horizontal":
                while col < 15 and self.curr_game_board[row][col] is not None:
                    equation += self.curr_game_board[row][col]["tile"]
                    if self.curr_game_board[row][col]["tile"] == '=':
                        if col > 0 and self.curr_game_board[row][col - 1] is not None:
                            answer_pos = (row, col + 1)
                        else:
                            answer_pos = (row, col - 1)
                    col += 1
            elif direction == "vertical":
                while row < 15 and self.curr_game_board[row][col] is not None:
                    equation += self.curr_game_board[row][col]["tile"]
                    if self.curr_game_board[row][col]["tile"] == '=':
                        if row > 0 and self.curr_game_board[row - 1][col] is not None:
                            answer_pos = (row + 1, col)
                        else:
                            answer_pos = (row - 1, col)
                    row += 1
            return equation, answer_pos

        # Check if any equation touches or lands on the START tile
        start_touched = False
        for piece in self.curr_equation:
            if (piece["row"], piece["col"]) == self.START_TILE:
                start_touched = True
                break
        
        if not start_touched:
            print("No equation touches or lands on the START tile. Equation is invalid.")
            self.show_invalid_equation_prompt()
            return False

        for piece in self.curr_equation:
            row, col = piece["row"], piece["col"]
            horizontal_equation, horizontal_answer_pos = extract_equation(row, col, "horizontal")
            if check_equation(horizontal_equation, horizontal_answer_pos):
                for piece in self.curr_equation:
                    piece["fixed"] = True
                self.draw_new_random_tiles()
                
                # Multiply the answer by 2 if the tile color is 2N
                if self.game_board_details[horizontal_answer_pos[0]][horizontal_answer_pos[1]] == '2N':
                    print("Answer multiplied by 2!")
                # Multiply the answer by 3 if the tile color is 3N
                elif self.game_board_details[horizontal_answer_pos[0]][horizontal_answer_pos[1]] == '3N':
                    print("Answer multiplied by 3!")
                return True

            vertical_equation, vertical_answer_pos = extract_equation(row, col, "vertical")
            if check_equation(vertical_equation, vertical_answer_pos):
                for piece in self.curr_equation:
                    piece["fixed"] = True
                self.draw_new_random_tiles()
                
                # Multiply the answer by 2 if the tile color is 2N
                if self.game_board_details[vertical_answer_pos[0]][vertical_answer_pos[1]] == '2N':
                    print("Answer multiplied by 2!")
                # Multiply the answer by 3 if the tile color is 3N
                elif self.game_board_details[vertical_answer_pos[0]][vertical_answer_pos[1]] == '3N':
                    print("Answer multiplied by 3!")
                return True

        print("Invalid equation. Please try again.")
        self.show_invalid_equation_prompt()

        for piece in self.curr_equation:
            row, col = piece["row"], piece["col"]
            if "original_tile" in piece:
                piece["tile"] = piece["original_tile"]
                del piece["original_tile"]
            self.curr_game_board[row][col] = None
            self.player_pieces.append(piece)
        self.curr_equation.clear()
        return False

    def draw_new_random_tiles(self):
        used_tiles = [piece["tile"] for piece in self.curr_equation]

        for tile in used_tiles:
            if tile.isdigit() or tile == '0':
                new_tile = random.choice(list(self.TILE_NUMBER_POINTS.keys()))
            elif tile in self.TILE_OPERATOR_POINTS:
                new_tile = random.choice(list(self.TILE_OPERATOR_POINTS.keys()))
            else:
                new_tile = '='

            piece = {
                "tile": new_tile,
                "points": self.TILE_NUMBER_POINTS.get(new_tile) or self.TILE_OPERATOR_POINTS.get(new_tile) or self.TILE_EQUAL_POINTS.get(new_tile) or 0,
                "rect": pygame.Rect(0, 0, self.TILE_SIZE, self.TILE_SIZE)
            }
            self.player_pieces.append(piece)
            if new_tile in self.TILE_PCS:
                self.TILE_PCS[new_tile] -= 1

        self.update_player_pieces_positions()

    def show_invalid_equation_prompt(self):
        # Create a semi-transparent overlay
        overlay = pygame.Surface((self.display.get_width(), self.display.get_height()), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # Black with 50% opacity

        # Render the text
        font = pygame.font.Font(None, 48)
        text_surface = font.render("Invalid", True, self.RED)
        text_rect = text_surface.get_rect(center=(self.display.get_width() // 2, self.display.get_height() // 2))

        # Blit the overlay and text onto the display
        self.display.blit(overlay, (0, 0))
        self.display.blit(text_surface, text_rect)
        pygame.display.flip()
        pygame.time.wait(750)  

    def calculate_total_points(self):
        # Reset total points
        self.total_points = 0

        # Iterate through all tiles and add their points
        for row in self.curr_game_board:
            for tile in row:
                if tile:
                    self.total_points += tile["points"]

    def draw_total_points(self):
        # Render the total points text
        font = pygame.font.Font(None, 36)
        text_surface = font.render(f"{self.total_points}", True, self.WHITE)

        # Define the position of the text
        text_rect = text_surface.get_rect(topleft=(170, 92))  # Adjust the position of the text

        # Blit the text onto the display
        self.display.blit(text_surface, text_rect)

    def load_assets(self):
        self.assets_dir = os.path.join("assets")
        self.images_dir = os.path.join(self.assets_dir, "images")
        self.FONT = pygame.font.Font(None, self.FONT_SIZE)

### remove after dev
if __name__ == "__main__":
    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 650
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    game_state_manager = GameStateManager('MathMender')
    game_state_manager.set_state(MathMender(screen, game_state_manager))
    game_state_manager.get_state().run()
###

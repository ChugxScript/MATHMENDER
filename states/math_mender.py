import pygame
import os
import random
import math
import numpy as np

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
        self.valid_tiles = [(7,7)]

        # players details
        self.PLAYER_TURN = True
        self.AI_TURN = False
        self.PLAYER_SCORE = 0
        self.AI_SCORE = 0

        # Include additional initialization for ACO parameters
        self.pheromone = np.ones((15, 15))  # Example initialization, adjust as needed
        self.alpha = 1.0  # Influence of pheromone
        self.beta = 2.0   # Influence of heuristic information
        self.evaporation_rate = 0.5
        self.ant_count = 10
        self.iterations = 100

        # Define the game board grid
        self.game_board = [[None for _ in range(15)] for _ in range(15)]
        self.curr_game_board = [[None for _ in range(15)] for _ in range(15)]
        self.game_board_details = [[None for _ in range(15)] for _ in range(15)]

    def run(self):
        self.load_assets()
        self.draw_bg()
        self.init_board()
        self.draw_pieces_pcs()
        self.get_player_pieces()
        self.get_ai_pieces()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                
                if self.PLAYER_TURN:
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
            
            if self.AI_TURN:
                self.ai_make_move()

            self.display.blit(self.math_mender_bg, (0, 0))
            self.init_board()
            self.draw_updated_board()
            self.draw_pieces_pcs()
            self.draw_player_pieces()
            self.draw_player_pieces_with_click()
            self.draw_rect_btn()
            self.draw_total_points()
            self.valid_tiles = self.valid_tiles_to_drop()
            self.draw_valid_tiles()
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
        
        # print(f"\n>>self.valid_tiles: {self.valid_tiles}")
        if ((row, col) in self.valid_tiles):
            print("Clicked cell:", row, col)
            
            if mode == "add_tile":
                # Check if there is an expanded tile to be placed
                if self.clicked_tile:
                    # Place the expanded tile onto the game board if the cell is empty
                    if self.curr_game_board[row][col] is None:
                        # Create a copy of the clicked tile to modify its value
                        placed_tile = self.clicked_tile.copy()

                        # Mark the tile as not fixed initially
                        placed_tile["fixed"] = False

                        if self.PLAYER_TURN:
                            placed_tile["player"] = "PLAYER"
                        if self.AI_TURN:
                            placed_tile["player"] = "AI"

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
                        print(f"\n>>self.curr_equation: {[piece['tile'] for piece in self.curr_equation if piece['tile'] not in ['√']]}")
                        # Remove the tile from player pieces
                        self.player_pieces.remove(self.clicked_tile)
                        # Reset expanded_tile
                        self.clicked_tile = None

        elif self.curr_game_board[row][col] is not None:
            if mode == "remove_tile":
                for piece in self.curr_equation:
                    if piece == self.curr_game_board[row][col]:
                        self.player_pieces.append(piece)
                        self.curr_equation.remove(piece)

                self.curr_game_board[row][col] = None

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

    def is_valid(self):
        if self.curr_game_board[7][7] is not None:
            if self.curr_game_board != self.game_board:
                curr_row = []
                curr_col = []
                print(f"\n>>self.curr_game_board: ")
                for tile in self.curr_game_board:
                    print(tile)
                
                print(f"\n>>self.curr_equation: ")
                for tile in self.curr_equation:
                    print(tile)
                    curr_row.append(tile["row"])
                    curr_col.append(tile["col"])

                print(f"\n>>curr_row: {curr_row}")
                print(f">>curr_col: {curr_col}")

                '''
                    check the equation horizontal and vertical

                    check curr_row if all are the same
                        meaning the user is making equation horizontally

                        we will also check previous rows to check
                        if the user continue a previous equation
                '''

                prev_equation = ""
                curr_equation = ""
                curr_equation_points = 0
                has_blank = False
                is_2N = False # BLUE
                is_3N = False # GREEN
                is_2A = False # YELLOW
                is_3A= False # RED

                # Check if there is a blank tile in the equation
                has_blank = any(tile["tile"] == "blank" for tile in self.curr_equation)
                all_tiles = set(self.BLUE_TILES) | set(self.GREEN_TILES) | set(self.YELLOW_TILES) | set(self.RED_TILES)

                if not has_blank:
                    if all(x == curr_row[0] for x in curr_row):
                        print(f"\n>>curr_row: {curr_row}")
                        for col_a in range(15):
                            if self.curr_game_board[curr_row[0]][col_a] is not None:
                                curr_equation += self.curr_game_board[curr_row[0]][col_a]['tile']
                                # curr_equation_points += self.curr_game_board[curr_row[0]][col_a]['points']

                                # check if tile in power ups
                                if (curr_row[0], col_a) in self.BLUE_TILES:
                                    # the point of the tile that land on 2N tile will multiplied by 2
                                    is_2N = True
                                    curr_equation_points += (int(self.curr_game_board[curr_row[0]][col_a]['points']) * 2)

                                if (curr_row[0], col_a) in self.GREEN_TILES:
                                    # the point of the tile that land on 3N tile will multiplied by 3
                                    is_3N = True
                                    curr_equation_points += (int(self.curr_game_board[curr_row[0]][col_a]['points']) * 3)

                                if (curr_row[0], col_a) in self.YELLOW_TILES:
                                    is_2A = True
                                    curr_equation_points += int(self.curr_game_board[curr_row[0]][col_a]['points'])

                                if (curr_row[0], col_a) in self.RED_TILES:
                                    is_3A = True
                                    curr_equation_points += int(self.curr_game_board[curr_row[0]][col_a]['points'])
                                
                                if (curr_row[0], col_a) not in all_tiles:
                                    curr_equation_points += int(self.curr_game_board[curr_row[0]][col_a]['points'])

                            if self.game_board[curr_row[0]][col_a] is not None:
                                prev_equation += self.game_board[curr_row[0]][col_a]['tile']
                            
                    elif all(x == curr_col[0] for x in curr_col):
                        print(f"\n>>curr_col: {curr_col}")
                        for row_a in range(15):
                            if self.curr_game_board[row_a][curr_col[0]] is not None:
                                curr_equation += self.curr_game_board[row_a][curr_col[0]]['tile']
                                # curr_equation_points += self.curr_game_board[row_a][curr_col[0]]['points']

                                if (row_a, curr_col[0]) in self.BLUE_TILES:
                                    is_2N = True
                                    curr_equation_points += (int(self.curr_game_board[row_a][curr_col[0]]['points']) * 2)

                                if (row_a, curr_col[0]) in self.GREEN_TILES:
                                    is_3N = True
                                    curr_equation_points += (int(self.curr_game_board[row_a][curr_col[0]]['points']) * 3)

                                if (row_a, curr_col[0]) in self.YELLOW_TILES:
                                    is_2A = True
                                    curr_equation_points += int(self.curr_game_board[row_a][curr_col[0]]['points'])

                                if (row_a, curr_col[0]) in self.RED_TILES:
                                    is_3A = True
                                    curr_equation_points += int(self.curr_game_board[row_a][curr_col[0]]['points'])

                                if (row_a, curr_col[0]) not in all_tiles:
                                    curr_equation_points += int(self.curr_game_board[row_a][curr_col[0]]['points'])

                            if self.game_board[row_a][curr_col[0]] is not None:
                                prev_equation += self.game_board[row_a][curr_col[0]]['tile']

                else:
                    for tile in self.curr_equation:
                        if tile['tile'] != 'blank':
                            curr_equation += tile['tile']

                print(f"\n>>prev_equation: {prev_equation}")
                print(f">>curr_equation: {curr_equation}")
                print(f">>curr_equation_points: {curr_equation_points}")

                lhs, rhs = self.convert_operators(curr_equation)
                if lhs is not None and rhs is not None:
                    evaluated_lhs = eval(lhs)
                    evaluated_rhs = eval(rhs)
                    is_correct = evaluated_lhs == evaluated_rhs
                    print(f">>is_correct: {is_correct}")
                    print(f">>evaluated_lhs: {evaluated_lhs}")

                    if is_correct:
                        if self.PLAYER_TURN:
                            if is_2A:
                                # the answer of the equation will multiply by 2 plus the points of each tiles
                                self.PLAYER_SCORE += (int(evaluated_lhs) * 2) + curr_equation_points
                            if is_3A:
                                # the answer of the equation will multiply by 3 plus the points of each tiles
                                self.PLAYER_SCORE += (int(evaluated_lhs) * 3) + curr_equation_points
                            
                            if is_2N or is_3N:
                                # already added in checking of power ups
                                self.PLAYER_SCORE += curr_equation_points
                            
                            if not is_2N and not is_3N and not is_2A and not is_3A:
                                self.PLAYER_SCORE += curr_equation_points
                        
                        if self.AI_TURN:
                            if is_2A:
                                # the answer of the equation will multiply by 2 plus the points of each tiles
                                self.AI_SCORE += (evaluated_lhs * 2) + curr_equation_points
                            if is_3A:
                                # the answer of the equation will multiply by 3 plus the points of each tiles
                                self.AI_SCORE += (evaluated_lhs * 3) + curr_equation_points
                            
                            if is_2N or is_3N:
                                # already added in checking of power ups
                                self.AI_SCORE += curr_equation_points
                            
                            if not is_2N and not is_3N and not is_2A and not is_3A:
                                self.AI_SCORE += curr_equation_points
                        
                        self.draw_total_points()
                        self.draw_new_random_tiles()
                        '''
                            copy the curr_game_board content to the game_board
                        '''
                        for row in range(15):
                            for col in range(15):
                                self.game_board[row][col] = self.curr_game_board[row][col]

                        self.curr_equation.clear()
                        return True
                    else:
                        for piece in self.curr_equation:
                            self.curr_game_board[piece["row"]][piece["col"]] = None
                            self.player_pieces.append(piece)
                        self.curr_equation.clear()

                        print(f"\n>>[ERROR] INVALID EQUATION")
                        self.show_invalid_equation_prompt("[ERROR] INVALID EQUATION")
                        return False
                else:
                    for piece in self.curr_equation:
                        self.curr_game_board[piece["row"]][piece["col"]] = None
                        self.player_pieces.append(piece)
                    self.curr_equation.clear()

                    print(f"\n>>[ERROR] INVALID EQUATION")
                    self.show_invalid_equation_prompt("[ERROR] INVALID EQUATION")
                    return False
            else:
                for piece in self.curr_equation:
                    self.curr_game_board[piece["row"]][piece["col"]] = None
                    self.player_pieces.append(piece)
                self.curr_equation.clear()

                print(f"\n>>[ERROR] NO CHANGES IN BOARD")
                self.show_invalid_equation_prompt("[ERROR] NO CHANGES IN BOARD")
                return False
        else:
            for piece in self.curr_equation:
                self.curr_game_board[piece["row"]][piece["col"]] = None
                self.player_pieces.append(piece)
            self.curr_equation.clear()

            print(f"\n>>[ERROR] CENTER IS EMPTY")
            self.show_invalid_equation_prompt("[ERROR] CENTER IS EMPTY")
            return False
    
    def convert_operators(self, equation_str):
        # Replace special operators with Python arithmetic operators or math functions
        conversion_dict = {
            '^2': '**2',
            'x': '*',
            '÷': '/',
            '=': '==',
        }
        for op, replacement in conversion_dict.items():
            equation_str = equation_str.replace(op, replacement)

        try:
            # Handle square root operator
            equation_parts = equation_str.split('==')
            lhs = equation_parts[0]
            rhs = equation_parts[1]

            if '√' in lhs:
                # Extract the number after the square root operator
                lhs = lhs.replace('√', 'math.sqrt(') + ')'
            
            if '√' in rhs:
                rhs = rhs.replace('√', 'math.sqrt(') + ')'

            return lhs, rhs
        except Exception as e:
            return None, None
    
    def valid_tiles_to_drop(self):
        if self.curr_game_board[7][7] is not None:
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            valid_positions = []
            occupied_tiles = []

            for row in range(15):
                for col in range(15):
                    if self.curr_game_board[row][col] is not None:
                        occupied_tiles.append((row, col))

            for row_a, col_a in occupied_tiles:
                for dx, dy in directions:
                    new_x, new_y = row_a + dx, col_a + dy
                    if self.is_valid_tile(new_x, new_y):
                        valid_positions.append((new_x, new_y))
        else:
            valid_positions = [(7,7)]
        
        return valid_positions

    def is_valid_tile(self, row, col):
        size = 15
        if 0 <= row < size and 0 <= col < size and self.curr_game_board[row][col] is None:
            return True
        return False
    
    def draw_valid_tiles(self):
        for row, col in self.valid_tiles:
            x = (col + 13) * (self.TILE_SIZE + self.TILE_MARGIN)
            y = (row + 0.3) * (self.TILE_SIZE + self.TILE_MARGIN)
            
            # Create a surface with per-pixel alpha values
            border_surface = pygame.Surface((self.TILE_SIZE, self.TILE_SIZE), pygame.SRCALPHA)
            
            # Draw a semi-transparent gold rectangle on the surface
            pygame.draw.rect(border_surface, (255, 215, 0, 153), (0, 0, self.TILE_SIZE, self.TILE_SIZE))
            
            # Draw black border on the surface
            pygame.draw.rect(border_surface, (0, 150, 0), (0, 0, self.TILE_SIZE, self.TILE_SIZE), 3)
            
            # Blit the surface onto the display at the tile position
            self.display.blit(border_surface, (x, y))

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

    def show_invalid_equation_prompt(self, message):
        # Create a semi-transparent overlay
        overlay = pygame.Surface((self.display.get_width(), self.display.get_height()), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # Black with 50% opacity

        # Render the text with a black background
        font = pygame.font.Font(None, 48)
        text_surface = font.render(message, True, self.RED)
        text_rect = text_surface.get_rect(center=(self.display.get_width() // 2, self.display.get_height() // 2))
        
        # Create a surface for the text with a black background
        text_bg_surface = pygame.Surface((text_rect.width + 20, text_rect.height + 20))
        text_bg_surface.fill((0, 0, 0))  # Black background
        text_bg_surface.blit(text_surface, (10, 10))  # Blit the text onto the black background surface
        
        # Blit the overlay onto the display
        self.display.blit(overlay, (0, 0))
        
        # Blit the text with black background onto the display
        self.display.blit(text_bg_surface, (text_rect.x - 10, text_rect.y - 10))  # Adjust position for padding
        
        pygame.display.flip()
        pygame.time.wait(1000)

    def draw_total_points(self):
        # Render the total points text
        font = pygame.font.Font(None, 36)
        PLAYERscore_surface = font.render(f"{self.PLAYER_SCORE}", True, self.WHITE)
        AIscore_surface = font.render(f"{self.AI_SCORE}", True, self.WHITE)

        # Define the position of the text
        PLAYERscore_rect = PLAYERscore_surface.get_rect(topleft=(160, 92)) 
        AIscore_rect = PLAYERscore_surface.get_rect(topleft=(420, 92)) 

        # Blit the text onto the display
        self.display.blit(PLAYERscore_surface, PLAYERscore_rect)
        self.display.blit(AIscore_surface, AIscore_rect)
    
    ### ----- AI PART -----
    def ai_make_move(self):
        best_solution = None
        best_score = -float('inf')
        for iteration in range(self.iterations):
            solutions = []
            for ant in range(self.ant_count):
                solution, score = self.construct_solution()
                solutions.append((solution, score))
                if score > best_score:
                    best_solution = solution
                    best_score = score
            self.update_pheromones(solutions)
        
        if best_solution:
            self.apply_solution(best_solution)
            self.AI_TURN = False
            self.PLAYER_TURN = True
    
    def construct_solution(self):
        current_solution = []
        current_score = 0
        for tile in self.ai_pieces:
            possible_positions = self.valid_tiles_to_drop()  # Method to get valid positions for a tile
            probabilities = self.calculate_probabilities(possible_positions, tile)
            chosen_position = self.select_position(possible_positions, probabilities)
            if chosen_position:
                self.place_tile(tile, chosen_position)  # Method to place a tile on the board
                current_solution.append((tile, chosen_position))
                current_score += self.evaluate_position(chosen_position, tile)  # Method to evaluate position score
        return current_solution, current_score
    
    def calculate_probabilities(self, positions, tile):
        probabilities = []
        total_sum = 0
        for pos in positions:
            pheromone_level = self.pheromone[pos]
            heuristic_value = self.heuristic_value(pos, tile)
            probability = (pheromone_level ** self.alpha) * (heuristic_value ** self.beta)
            probabilities.append(probability)
            total_sum += probability
        probabilities = [prob / total_sum for prob in probabilities]
        return probabilities

    def select_position(self, positions, probabilities):
        return random.choices(positions, probabilities, k=1)[0]

    def update_pheromones(self, solutions):
        self.pheromone *= (1 - self.evaporation_rate)
        for solution, score in solutions:
            for tile, pos in solution:
                self.pheromone[pos] += score

    def apply_solution(self, solution):
        for tile, pos in solution:
            self.place_tile(tile, pos)

    def heuristic_value(self, pos, tile):
        row, col = pos
        heuristic_score = 0

        '''
            check the valid tile (pos) if the adjacent tiles is not None
                meaning the adjacent tile is either a number, operation, or equal sign
            
            first is check if the valid tile has 2 or more adjacent tiles
            
            if theres only one djacent tile meaning the either the left, right, top, or bottom tiles of the valid tile
                is empty or None
            
            if there are 2 adjacent tile meaning the left and right OR top and bottom are adjacent
                we'll deal with this by comparing if the both adjacent tiles (2 tiles) has same rows or cols
                
                if both adjacent tiles has SAME ROWS meaning the current tile (pos) is between top and bottom tiles
                    this position is valid since it has only 2 adjcent tiles
                    [
                        ' ', ' ', '   ', ' ', ' ', '',
                        '3', '+', ' 3 ', '=', '6', '',
                        ' ', ' ', '[P]', ' ', ' ', '',
                        '4', '=', ' 2 ', '+', '2', '',
                        ' ', ' ', '   ', ' ', ' ', '',
                    ]

                if both adjacent tiles has SAME COLS meaning the current tile (pos) is between left and right tiles
                    this position is valid since it has only 2 adjcent tiles 
                    [
                        ' ', '1', ' + ', '3', '=', '4',
                        ' ', '+', '   ', '+', ' ', '',
                        ' ', '11','[P]', '2', ' ', '',
                        ' ', '=', '   ', '=', ' ', '',
                        ' ', '12','   ', '5', ' ', '',
                        ' ', ' ', '   ', ' ', ' ', '',
                    ]
            
            elif there are more than 2; like the current tile (pos) has 3 or 4 adjacent tiles:
                IS IT POSSIBLE TO MAKE AN EQUATION FROM IT ???
                [
                    ' ', '1', '   ', ' ', ' ', '',
                    '3', '+', ' 3 ', '=', '6', '',
                    ' ', '1', '[P]', ' ', ' ', '',
                    '4', '=', ' 2 ', '+', '2', '',
                    ' ', '2', '   ', ' ', ' ', '',
                ]
                adjacent tiles are 3(1,2), 1(2,1), and 2(3,2) 

                [
                    ' ', '1', '   ', '5', ' ', '',
                    '3', '+', ' 3 ', '=', '6', '',
                    ' ', '1', '[P]', '2', ' ', '',
                    '4', '=', ' 2 ', '+', '2', '',
                    ' ', '2', '   ', '3', ' ', '',
                ]
                adjacent tiles are 3(1,2), 1(2,1), 2(3,2), and 2(2,3)

                its kinda difficult tho
                for safetly purposes we will not include if the current tile(pos) that has more than 2 adacent tiles HAHAHAHAHA
        '''
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
        adj_pos = []
        adj_score = 0
        is_tile_number = False
        is_tile_operator = False
        is_tile_equal = False

        for d_row, d_col in directions:
            if 0 <= row + d_row < 15 and 0 <= col + d_col < 15 and self.curr_game_board[row + d_row][col + d_col] is not None:
                adj_row, adj_col = row + d_row, col + d_col
                adj_pos.append((adj_row, adj_col))
        
        if len(adj_pos) < 3:
            for d_row, d_col in adj_pos:
                # give points
                if self.curr_game_board[d_row][d_col]['tile'] in self.TILE_NUMBER_POINTS:
                    is_tile_number = True
                    adj_score += 1 
                if self.curr_game_board[d_row][d_col]['tile'] in self.TILE_OPERATOR_POINTS:
                    is_tile_operator = True
                    adj_score += 1 
                if self.curr_game_board[d_row][d_col]['tile'] in self.TILE_EQUAL_POINTS:
                    is_tile_equal = True
                    adj_score += 1 
        
        if is_tile_number:
            heuristic_score += adj_score * 30
        if is_tile_operator:
            heuristic_score += adj_score * 20
        if is_tile_equal:
            heuristic_score += adj_score * 10

        # check if the current tile (pos) is in power up tiles
        if (row, col) in self.BLUE_TILES:
            heuristic_score += 30
        elif (row, col) in self.GREEN_TILES:
            heuristic_score += 50
        elif (row, col) in self.YELLOW_TILES:
            heuristic_score += 75
        elif (row, col) in self.RED_TILES:
            heuristic_score += 100 

        '''
            Potential to complete an equation
            Here you can implement a check to see if placing the tile helps form a complete equation
            For simplicity, we'll just give a flat score if it completes an equation
        '''
        equation_completion_bonus = 0

        if len(adj_pos) < 3:
            equation = ""

            if len(adj_pos) == 1:
                row_a, col_a = adj_pos[0]
                if row_a == row:
                    # horizontal
                    equation = self.form_equation_from_position(pos, tile, "horizontal")
                elif col_a == col:
                    # vertical
                    equation = self.form_equation_from_position(pos, tile, "vertical")
            
            elif len(adj_pos) == 2:
                row_a, col_a = adj_pos[0]
                row_b, col_b = adj_pos[1]

                if row_a == row_b:
                    # horizontal
                    equation = self.form_equation_from_position(pos, tile, "horizontal")
                elif col_a == col_b:
                    # vertical
                    equation = self.form_equation_from_position(pos, tile, "vertical")

            if self.is_valid_equation(equation):
                equation_completion_bonus = 100

        heuristic_score += equation_completion_bonus

        return heuristic_score

    def form_equation_from_position(self, pos, tile, mode):
        # Form a potential equation string starting from this position
        # For simplicity, we'll assume it's a horizontal equation
        row, col = pos
        equation_a = []
        equation_b = []
        equation_c = []
        equation_b.append(tile)
        equation = ""

        if mode == "vertical":
            # get part a 
            row_n = row
            while True:
                row_n -= 1
                if row_n < 0: 
                    break
                if self.curr_game_board[row_n][col] is not None:
                    equation_a.append(self.curr_game_board[row_n][col])
                else:
                    break
            
            # get part c
            row_n = row
            while True:
                row_n += 1
                if row_n > 15: 
                    break
                if self.curr_game_board[row_n][col] is not None:
                    equation_c.append(self.curr_game_board[row_n][col])
                else:
                    break

            # combine all parts
            for t in equation_b:
                equation_a.append(t)
            for t in equation_c:
                equation_a.append(t)

            # get the equation string
            for t in equation_a:
                equation += t['tile']

        elif mode == "horizontal":
            # get part a 
            col_n = col
            while True:
                col_n -= 1
                if col_n < 0: 
                    break
                if self.curr_game_board[row][col_n] is not None:
                    equation_a.append(self.curr_game_board[row][col_n])
                else:
                    break
            
            # get part c
            col_n = col
            while True:
                col_n += 1
                if col_n > 15: 
                    break
                if self.curr_game_board[row][col_n] is not None:
                    equation_c.append(self.curr_game_board[row][col_n])
                else:
                    break

            # combine all parts
            for t in equation_b:
                equation_a.append(t)
            for t in equation_c:
                equation_a.append(t)

            # get the equation string
            for t in equation_a:
                equation += t['tile']

        return equation

    def is_valid_equation(self, equation):
        lhs, rhs = self.convert_operators(equation)
        if lhs is not None and rhs is not None:
            return eval(lhs) == eval(rhs)
        return False

    def get_ai_pieces(self):
        operators = random.sample(list(self.TILE_OPERATOR_POINTS.keys()), 2)
        numbers = random.sample(list(self.TILE_NUMBER_POINTS.keys()), 6)
        equal_sign = random.sample(list(self.TILE_EQUAL_POINTS.keys()), 1)

        selected_tiles = equal_sign + numbers + operators

        self.ai_pieces = []
        for tile in selected_tiles:
            piece = {
                "tile": tile,
                "points": self.TILE_NUMBER_POINTS.get(tile) or self.TILE_OPERATOR_POINTS.get(tile) or self.TILE_EQUAL_POINTS.get(tile) or 0,
                "rect": pygame.Rect(0, 0, self.TILE_SIZE, self.TILE_SIZE)
            }
            self.ai_pieces.append(piece)
            if tile in self.TILE_PCS:
                self.TILE_PCS[tile] -= 1

    def place_tile(self, tile, position):
        # Place the tile on the board at the specified position
        row, col = position
        self.curr_game_board[row][col] = tile

    def evaluate_position(self, position, tile):
        '''
            Evaluate the score of placing the tile at the position

            if len adjacent tile is 1:
                if adjacent tile is number:
                    any piece can be placed on that position so +1 score
                    example: 
                        1[1] or 1[+] or 1[=] are valid

                if adjacent tile is operator:
                    only number pieces can be placed so +3 score
                    example:
                        +[1] is valid
                        +[+] and +[=] are not valid

                if adjacent tile is equal:
                    only number pieces can be placed so +2 score
                    example:
                        =[1] is valid
                        =[+] and =[=] are not valid
            
            elif len adjacent tile is 2:
                if adjacent tile are both number:
                    operator or equal pieces can be placed +2 score
                    example:
                        adjacent left and right:
                            [
                                '', ' ', '   ', ' ', '',
                                '', '1', '[+]', '1', '', 
                                '', ' ', '   ', ' ', '',
                            ]
                            or
                            [
                                '', ' ', '   ', ' ', '',
                                '', '1', '[=]', '1', '', 
                                '', ' ', '   ', ' ', '',
                            ]

                        adjacent top and bottom:
                            [
                                '', '', '   ', '', '', 
                                '', '', ' 1 ', '', '', 
                                '', '', '[+]', '', '', 
                                '', '', ' 1 ', '', '', 
                                '', '', '   ', '', '', 
                            ]
                            or
                            [
                                '', '', '   ', '', '', 
                                '', '', ' 1 ', '', '', 
                                '', '', '[=]', '', '', 
                                '', '', ' 1 ', '', '', 
                                '', '', '   ', '', '', 
                            ]

                if adjacent tile both operator:
                    only number pieces can be placed +3 score
                    example:
                        adjacent left and right:
                            [
                                '', ' ', '   ', ' ', '',
                                '', '+', '[1]', '-', '', 
                                '', ' ', '   ', ' ', '',
                            ] is valid
                            
                            [
                                '', ' ', '   ', ' ', '',
                                '', '+', '[x]', '-', '', 
                                '', ' ', '   ', ' ', '',
                            ] and 
                            [
                                '', ' ', '   ', ' ', '',
                                '', '+', '[=]', '-', '', 
                                '', ' ', '   ', ' ', '',
                            ] are not valid

                        adjacent top and bottom:
                            [
                                '', '', '   ', '', '', 
                                '', '', ' + ', '', '', 
                                '', '', '[1]', '', '', 
                                '', '', ' - ', '', '', 
                                '', '', '   ', '', '', 
                            ] is valid
                            
                            [
                                '', '', '   ', '', '', 
                                '', '', ' + ', '', '', 
                                '', '', '[x]', '', '', 
                                '', '', ' - ', '', '', 
                                '', '', '   ', '', '', 
                            ] and
                            [
                                '', '', '   ', '', '', 
                                '', '', ' + ', '', '', 
                                '', '', '[=]', '', '', 
                                '', '', ' - ', '', '', 
                                '', '', '   ', '', '', 
                            ] are not valid

                if adjacent tile both equal:
                    example: =1=1 ??? is that valid?
                                1=1=1 possible but..
                                to be safe lets set the score to 0 HAHAHAHA
                
                if adjacent tile [1] is number and [2] is operator or vice versa:
                    only number can be placed
                    example:
                        adjacent left and right:
                            [
                                '', ' ', '   ', ' ', '',
                                '', '1', '[1]', '-', '', 
                                '', ' ', '   ', ' ', '',
                            ] is valid
                            
                            [
                                '', ' ', '   ', ' ', '',
                                '', '1', '[x]', '-', '', 
                                '', ' ', '   ', ' ', '',
                            ] and 
                            [
                                '', ' ', '   ', ' ', '',
                                '', '1', '[=]', '-', '', 
                                '', ' ', '   ', ' ', '',
                            ] are not valid

                        adjacent top and bottom:
                            [
                                '', '', '   ', '', '', 
                                '', '', ' 1 ', '', '', 
                                '', '', '[1]', '', '', 
                                '', '', ' - ', '', '', 
                                '', '', '   ', '', '', 
                            ] is valid
                            
                            [
                                '', '', '   ', '', '', 
                                '', '', ' 1 ', '', '', 
                                '', '', '[x]', '', '', 
                                '', '', ' - ', '', '', 
                                '', '', '   ', '', '', 
                            ] and
                            [
                                '', '', '   ', '', '', 
                                '', '', ' 1 ', '', '', 
                                '', '', '[=]', '', '', 
                                '', '', ' - ', '', '', 
                                '', '', '   ', '', '', 
                            ] are not valid
                
                if adjacent tile [1] is number and [2] is equal or vice versa
                    OR 
                if adjacent tile [1] is operator and [2] is equal or vice versa:
                    no pieces can be placed score = 0
                    example:
                        adjacent left and right:
                            [
                                '', ' ', '   ', ' ', '',
                                '', '1', '[1]', '=', '', 
                                '', ' ', '   ', ' ', '',
                            ] not valid
                            [
                                '', ' ', '   ', ' ', '',
                                '', '1', '[x]', '=', '', 
                                '', ' ', '   ', ' ', '',
                            ] not valid 
                            [
                                '', ' ', '   ', ' ', '',
                                '', '1', '[=]', '-', '', 
                                '', ' ', '   ', ' ', '',
                            ] not valid
                            [
                                '', ' ', '   ', ' ', '',
                                '', '+', '[1]', '=', '', 
                                '', ' ', '   ', ' ', '',
                            ] not valid
                            [
                                '', ' ', '   ', ' ', '',
                                '', '+', '[x]', '=', '', 
                                '', ' ', '   ', ' ', '',
                            ] not valid 
                            [
                                '', ' ', '   ', ' ', '',
                                '', '+', '[=]', '-', '', 
                                '', ' ', '   ', ' ', '',
                            ] not valid

                        adjacent top and bottom:
                            [
                                '', '', '   ', '', '', 
                                '', '', ' 1 ', '', '', 
                                '', '', '[1]', '', '', 
                                '', '', ' = ', '', '', 
                                '', '', '   ', '', '', 
                            ] not valid
                            
                            [
                                '', '', '   ', '', '', 
                                '', '', ' 1 ', '', '', 
                                '', '', '[x]', '', '', 
                                '', '', ' - ', '', '', 
                                '', '', '   ', '', '', 
                            ] and
                            [
                                '', '', '   ', '', '', 
                                '', '', ' 1 ', '', '', 
                                '', '', '[=]', '', '', 
                                '', '', ' - ', '', '', 
                                '', '', '   ', '', '', 
                            ] are not valid
        '''
        return 1  # Placeholder, implement your scoring logic

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

import pygame
import os
import random
import math
import numpy as np
import itertools
import re

# from states.ACO import AntColonyOptimization

### remove after dev
from game_state_manager import GameStateManager
from ACO import AntColonyOptimization
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
        self.FONT_SIZE = 17
        self.FONT_COLOR = self.BLACK

        # tile details
        self.TILE_NUMBER_POINTS = {
            '1': 1, '2': 1, '3': 2, '4': 2, '5': 3,
            '6': 2, '7': 4, '8': 2, '9': 2, '0': 1,
        }
        self.TILE_OPERATOR_POINTS = {
            '+': 1, '-': 1, 'x': 2, '÷': 3, 
            '^2': 5, 
        }
        self.TILE_EQUAL_POINTS = {
            '=': 1
        }
        # pieces each tiles
        self.TILE_PCS = {
            '1': 5, '2': 5, '3': 5, '4': 5, '5': 5,
            '6': 5, '7': 5, '8': 5, '9': 5, '0': 5,
            
            '+': 7, '-': 7, 'x': 5, '÷': 5, 
            '^2': 2, '=': 20, 
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
                                            self.show_green_prompt("AI TURN.")
                                            self.AI_TURN = True
                                            self.PLAYER_TURN = False
                                        else:
                                            print("Invalid equation!")
                                            for piece in self.curr_equation:
                                                self.curr_game_board[piece["row"]][piece["col"]] = None
                                                self.player_pieces.append(piece)
                                            self.curr_equation.clear()

                                            print(f"\n>>[ERROR] INVALID EQUATION")
                                            self.show_invalid_equation_prompt("[ERROR] INVALID EQUATION")

                                    if rect["id"] == "pass":
                                        print("pass button clicked")
                                        self.show_green_prompt("YOU PASS.")
                                        self.show_green_prompt("AI TURN.")
                                        self.AI_TURN = True
                                        self.PLAYER_TURN = False

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
                        print(f"\n>>self.curr_equation: {[piece['tile'] for piece in self.curr_equation if piece['tile'] not in ['√']]}")
                        self.player_pieces.remove(self.clicked_tile)
                        self.clicked_tile = None

        elif self.curr_game_board[row][col] is not None:
            if mode == "remove_tile":
                for piece in self.curr_equation:
                    print(f"\n>>piece: {piece}")
                    print(f"\n>>self.game_board[row][col]: {self.game_board[row][col]}")
                    if piece != self.game_board[row][col]:
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
        large_font_size = self.FONT_SIZE + 3
        large_font = pygame.font.Font(None, large_font_size)
        text_surface = large_font.render(tile, True, self.BLACK)
        text_rect = text_surface.get_rect(center=(self.TILE_SIZE // 2, self.TILE_SIZE // 2.3))
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
                if len(self.curr_equation) == 1:
                    start_row = self.curr_equation[0]['row']
                    start_col = self.curr_equation[0]['col']

                    # horizontal
                    horiz_arr = []
                    horiz_str = ''
                    horiz_arr.append(self.curr_game_board[start_row][start_col])

                    # start col to left
                    move_idx = 1
                    while move_idx < 15:
                        move_col = start_col + move_idx
                        if self.curr_game_board[start_row][move_col] is not None:
                            horiz_arr.append(self.curr_game_board[start_row][move_col])
                            move_idx += 1
                        else:
                            break
                    
                    # start col to right
                    move_idx = 1
                    while move_idx >= 0:
                        move_col = start_col - move_idx
                        if self.curr_game_board[start_row][move_col] is not None:
                            horiz_arr.append(self.curr_game_board[start_row][move_col])
                            move_idx += 1
                        else:
                            break

                    # sort horizontal array in ascending order base on col
                    sorted_horiz_arr = sorted(horiz_arr, key=lambda x: x['col'])
                    for item in sorted_horiz_arr:
                        print(item)
                    
                    horiz_str = ''.join(sorted_horiz_arr['tile'])
                    print(f">>horiz_str: {horiz_str}")


                    # vertical
                    verti_arr = []
                    verti_str = ''
                    verti_arr.append(self.curr_game_board[start_row][start_col])

                    # start row to downward
                    move_idx = 1
                    while move_idx < 15:
                        move_row = start_row + move_idx
                        if self.curr_game_board[move_row][start_col] is not None:
                            verti_arr.append(self.curr_game_board[move_row][start_col])
                            move_idx += 1
                        else:
                            break
                    
                    # start row to upward
                    move_idx = 1
                    while move_idx >= 0:
                        move_row = start_row - move_idx
                        if self.curr_game_board[move_row][start_col] is not None:
                            verti_arr.append(self.curr_game_board[move_row][start_col])
                            move_idx += 1
                        else:
                            break
                    
                    # sort vertical array in ascending order base on row
                    sorted_verti_arr = sorted(horiz_arr, key=lambda x: x['row'])
                    for item in sorted_verti_arr:
                        print(item)
                    
                    verti_str = ''.join(sorted_verti_arr['tile'])
                    print(f">>verti_str: {verti_str}")

                    horiz_parts = horiz_str.split('=')
                    verti_parts = verti_str.split('=')
                    horiz_ref = eval(horiz_parts[0])
                    verti_ref = eval(verti_parts[0])
                    horiz_eval = True
                    verti_eval = True

                    for part in horiz_parts[1:]:
                        if eval(part) != horiz_ref:
                            horiz_eval = False
                            break
                    for part in verti_parts[1:]:
                        if eval(part) != verti_ref:
                            verti_eval = False
                            break
                    
                    if horiz_eval and verti_eval:
                        # if horiz_ref == verti_ref: # not sure kung need neto
                        one_tile_point = 0
                        all_tiles = set(self.BLUE_TILES) | set(self.GREEN_TILES) | set(self.YELLOW_TILES) | set(self.RED_TILES)
                        
                        if (start_row, start_col) in self.BLUE_TILES:
                            one_tile_point += (int(self.curr_game_board[start_row][start_col]['points']) * 2)
                            print(f">>one_tile_point blue: {one_tile_point}")
                        if (start_row, start_col) in self.GREEN_TILES:
                            one_tile_point += (int(self.curr_game_board[start_row][start_col]['points']) * 3)
                            print(f">>one_tile_point green: {one_tile_point}")
                        
                        if (start_row, start_col) in self.YELLOW_TILES:
                            one_tile_point += (int(horiz_ref) * 2)
                            print(f">>one_tile_point yellow: {one_tile_point}")
                        if (start_row, start_col) in self.RED_TILES:
                            one_tile_point += (int(horiz_ref) * 3)
                            print(f">>one_tile_point red: {one_tile_point}")
                        
                        if (start_row, start_col) not in all_tiles:
                            one_tile_point += int(self.curr_game_board[start_row][start_col]['points'])
                            print(f">>one_tile_point no bonus: {one_tile_point}")
                        
                        print(f">>one_tile_point total: {one_tile_point}")
                        self.PLAYER_SCORE += one_tile_point
                        self.curr_game_board[start_row][start_col] = self.curr_equation[0]

                        self.draw_total_points()
                        self.draw_new_random_tiles()
                        for row in range(15):
                            for col in range(15):
                                self.game_board[row][col] = self.curr_game_board[row][col]
                        
                        self.curr_equation.clear()
                        self.show_green_prompt("VALID EQUATION.")
                        return True
                    
                    else:
                        for piece in self.curr_equation:
                            self.curr_game_board[piece["row"]][piece["col"]] = None
                            self.player_pieces.append(piece)
                        self.curr_equation.clear()

                        print(f"\n>>[ERROR] INVALID EQUATION")
                        self.show_invalid_equation_prompt("[ERROR] INVALID EQUATION")
                        return False
                
                elif self.curr_equation[0]['row'] == self.curr_equation[1]['row']:
                    # horizontal, col will move
                    print(f"HORIZONTAL EQUATION.")

                    print(f"HORIZONTAL self.curr_equation.")
                    for item in self.curr_equation:
                        print(item)

                    print(f"HORIZONTAL sorted_array.")
                    sorted_array = sorted(self.curr_equation, key=lambda x: x['col'])
                    for item in sorted_array:
                        print(item)

                    stay_row = int(sorted_array[0]['row'])
                    start_col = int(sorted_array[0]['col'])
                    horizontal_str = ''

                    dec_start = 1
                    start_idx = 0
                    while True:
                        currr_col = start_col - dec_start
                        if currr_col < 0:
                            break
                        if self.curr_game_board[stay_row][currr_col] is not None:
                            dec_start += 1
                        else:
                            start_idx = currr_col + 1
                            break
                    print(f">>start_idx: {start_idx}")
                    print(f">>self.curr_game_board[stay_row][start_idx]: {self.curr_game_board[stay_row][start_idx]}")
                    
                    move_idx = 0
                    col_eq_arr = []
                    while start_idx < 15:
                        move_col = start_idx + move_idx
                        if self.curr_game_board[stay_row][move_col] is not None:
                            col_eq_arr.append(self.curr_game_board[stay_row][move_col])
                            horizontal_str += self.curr_game_board[stay_row][move_col]['tile']
                            move_idx += 1
                        else:
                            break
                    print(f">>col_eq_arr: {col_eq_arr}")
                    print(f">>horizontal_str: {horizontal_str}")
                    
                    if self.is_valid_chain_equation(horizontal_str):
                        # validation board
                        temp_col_arr = []
                        temp_col_str = ''
                        for sheesh in range(15):
                            if self.curr_game_board[stay_row][sheesh] is not None:
                                temp_col_str += self.curr_game_board[stay_row][sheesh]['tile']
                            else:
                                if temp_col_str:
                                    temp_col_arr.append(temp_col_str)
                                temp_col_str = ''
                        
                        if temp_col_str:
                            temp_col_arr.append(temp_col_str)
                        
                        print(f">>temp_col_aaarr: {temp_col_arr}")
                        print(f">>temp_col_ssstr: {temp_col_str}")
                        
                        for ttt in temp_col_arr:
                            if len(ttt) > 1:
                                print(f">>1 ttt: {ttt}")
                                if self.is_valid_chain_equation(ttt):
                                    print(f">>2 horizontal_str: {horizontal_str}")
                                    print(f">>2 ttt: {ttt}")
                                    if horizontal_str == ttt:
                                        break
                                else:
                                    for piece in self.curr_equation:
                                        self.curr_game_board[piece["row"]][piece["col"]] = None
                                        self.player_pieces.append(piece)
                                    self.curr_equation.clear()

                                    print(f"\n>>[ERROR] INVALID EQUATION")
                                    self.show_invalid_equation_prompt("[ERROR] INVALID EQUATION")
                                    return False 

                        hoz_point = 0
                        all_tiles = set(self.BLUE_TILES) | set(self.GREEN_TILES) | set(self.YELLOW_TILES) | set(self.RED_TILES)
                        parts = horizontal_str.split('=')
                        part_a = parts[0]
                        conversion_dict = {
                            '^2': '**2',
                            'x': '*',
                            '÷': '/',
                        }
                        for op, replacement in conversion_dict.items():
                            part_a = part_a.replace(op, replacement)
                        print(f">>part_a: {part_a}")
                        eq_result = eval(part_a)
                        print(f">>eq_result: {eq_result}")
                        
                        for col_arr in col_eq_arr:
                            print(f"\n>>col_arr: {col_arr}")
                            print(f">>col_arr['points']: {col_arr['points']}")

                            if (col_arr['row'], col_arr['col']) in self.BLUE_TILES:
                                hoz_point += (int(col_arr['points']) * 2)
                                print(f">>hoz_point blue: {hoz_point}")
                            if (col_arr['row'], col_arr['col']) in self.GREEN_TILES:
                                hoz_point += (int(col_arr['points']) * 3)
                                print(f">>hoz_point green: {hoz_point}")
                            
                            if (col_arr['row'], col_arr['col']) in self.YELLOW_TILES:
                                hoz_point += (int(eq_result) * 2)
                                print(f">>hoz_point yellow: {hoz_point}")
                            if (col_arr['row'], col_arr['col']) in self.RED_TILES:
                                hoz_point += (int(eq_result) * 3)
                                print(f">>hoz_point red: {hoz_point}")
                            
                            if (col_arr['row'], col_arr['col']) not in all_tiles:
                                hoz_point += int(col_arr['points'])
                                print(f">>hoz_point no bonus: {hoz_point}")
                            
                            print(f">>hoz_point total: {hoz_point}")
                            self.PLAYER_SCORE += hoz_point
                            self.curr_game_board[col_arr['row']][col_arr['col']] = col_arr

                        self.draw_total_points()
                        self.draw_new_random_tiles()
                        for row in range(15):
                            for col in range(15):
                                self.game_board[row][col] = self.curr_game_board[row][col]
                        
                        self.curr_equation.clear()
                        self.show_green_prompt("VALID EQUATION.")
                        return True
                    
                    else:
                        print(f">>INVALID horizontal_str: {horizontal_str}")
                    
                elif self.curr_equation[0]['col'] == self.curr_equation[1]['col']:
                    # vertical, row will move
                    print(f"VERTICAL EQUATION.")

                    print(f"VERTICAL self.curr_equation.")
                    for item in self.curr_equation:
                        print(item)

                    print(f"VERTICAL sorted_array.")
                    sorted_array = sorted(self.curr_equation, key=lambda x: x['row'])
                    for item in sorted_array:
                        print(item)

                    start_row = int(sorted_array[0]['row'])
                    stay_col = int(sorted_array[0]['col'])
                    vertical_str = ''

                    dec_start = 1
                    start_idx = 0
                    while True:
                        currr_row = start_row - dec_start
                        if currr_row < 0:
                            break
                        if self.curr_game_board[currr_row][stay_col] is not None:
                            dec_start += 1
                        else:
                            start_idx = currr_row + 1
                            break
                    print(f">>start_idx: {start_idx}")
                    print(f">>self.curr_game_board[start_idx][stay_col]: {self.curr_game_board[start_idx][stay_col]}")
                    
                    move_idx = 0
                    row_eq_arr = []
                    while start_idx < 15:
                        move_row = start_idx + move_idx
                        if self.curr_game_board[move_row][stay_col] is not None:
                            row_eq_arr.append(self.curr_game_board[move_row][stay_col])
                            vertical_str += self.curr_game_board[move_row][stay_col]['tile']
                            move_idx += 1
                        else:
                            break
                    print(f">>row_eq_arr: {row_eq_arr}")
                    print(f">>vertical_str: {vertical_str}")
                    
                    if self.is_valid_chain_equation(vertical_str):
                        # validation board
                        temp_row_arr = []
                        temp_row_str = ''
                        for sheesh in range(15):
                            if self.curr_game_board[sheesh][stay_col] is not None:
                                temp_row_str += self.curr_game_board[sheesh][stay_col]['tile']
                            else:
                                if temp_row_str:
                                    temp_row_arr.append(temp_row_str)
                                temp_row_str = ''
                        
                        if temp_row_str:
                            temp_row_arr.append(temp_row_str)
                        
                        print(f">>temp_row_aaarr: {temp_row_arr}")
                        print(f">>temp_row_ssstr: {temp_row_str}")
                        
                        for ttt in temp_row_arr:
                            if len(ttt) > 1:
                                print(f">>1 ttt: {ttt}")
                                if self.is_valid_chain_equation(ttt):
                                    print(f">>2 vertical_str: {vertical_str}")
                                    print(f">>2 ttt: {ttt}")
                                    if vertical_str == ttt:
                                        break
                                else:
                                    for piece in self.curr_equation:
                                        self.curr_game_board[piece["row"]][piece["col"]] = None
                                        self.player_pieces.append(piece)
                                    self.curr_equation.clear()

                                    print(f"\n>>[ERROR] INVALID EQUATION")
                                    self.show_invalid_equation_prompt("[ERROR] INVALID EQUATION")
                                    return False 

                        ver_point = 0
                        all_tiles = set(self.BLUE_TILES) | set(self.GREEN_TILES) | set(self.YELLOW_TILES) | set(self.RED_TILES)
                        parts = vertical_str.split('=')
                        part_a = parts[0]
                        conversion_dict = {
                            '^2': '**2',
                            'x': '*',
                            '÷': '/',
                        }
                        for op, replacement in conversion_dict.items():
                            part_a = part_a.replace(op, replacement)
                        print(f">>part_a: {part_a}")
                        eq_result = eval(part_a)
                        print(f">>eq_result: {eq_result}")

                        for row_arr in row_eq_arr:
                            print(f"\n>>row_arr: {row_arr}")
                            print(f">>row_arr['points']: {row_arr['points']}")

                            if (row_arr['row'], row_arr['col']) in self.BLUE_TILES:
                                ver_point += (int(row_arr['points']) * 2)
                                print(f">>ver_point blue: {ver_point}")
                            if (row_arr['row'], row_arr['col']) in self.GREEN_TILES:
                                ver_point += (int(row_arr['points']) * 3)
                                print(f">>ver_point green: {ver_point}")
                            
                            if (row_arr['row'], row_arr['col']) in self.YELLOW_TILES:
                                ver_point += (int(eq_result) * 2)
                                print(f">>ver_point yellow: {ver_point}")
                            if (row_arr['row'], row_arr['col']) in self.RED_TILES:
                                ver_point += (int(eq_result) * 3)
                                print(f">>ver_point red: {ver_point}")
                            
                            if (row_arr['row'], row_arr['col']) not in all_tiles:
                                ver_point += int(row_arr['points'])
                                print(f">>ver_point no bonus: {ver_point}")
                                
                            self.PLAYER_SCORE += ver_point
                            self.curr_game_board[row_arr['row']][row_arr['col']] = row_arr

                        self.draw_total_points()
                        self.draw_new_random_tiles()
                        for row in range(15):
                            for col in range(15):
                                self.game_board[row][col] = self.curr_game_board[row][col]
                        
                        self.curr_equation.clear()
                        self.show_green_prompt("VALID EQUATION.")
                        return True
                    
                    else:
                        print(f">>INVALID vertical_str: {vertical_str}")

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
    
    def handle_blank_eq(self, blank_eq):
        conversion_dict = {
            '^2': '**2',
            'x': '*',
            '÷': '/',
            '=': '==',
            'blank': '',
        }
        permutation_arr = [
            '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
            '+', '-', '*', '/', '**2', '√', '==',  
        ]

        for b_eq in blank_eq:
            beq_list = list(b_eq)

            temp_blank_eq = []
            for op, replacement in conversion_dict.items():
                beq_list = beq_list.replace(op, replacement)
            temp_blank_eq.append(beq_list)

            empty_indices = [j for j, char in enumerate(temp_blank_eq) if char == '']
            permutations = itertools.permutations(permutation_arr, len(empty_indices))

            equations = []
            for perm in permutations:
                eq_copy = temp_blank_eq.copy()
                for idx, val in zip(empty_indices, perm):
                    eq_copy[idx] = val
                equations.append(''.join(eq_copy))

            for eq in equations:
                if '==' in eq:
                    if self.is_valid_chain_equation(eq):
                        return True
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
    
    def show_green_prompt(self, message):
        # Create a semi-transparent overlay
        overlay = pygame.Surface((self.display.get_width(), self.display.get_height()), pygame.SRCALPHA)
        overlay.fill((0, 255, 0, 128)) 

        # Render the text with a background
        font = pygame.font.Font(None, 48) 
        text_surface = font.render(message, True, self.GREEN)
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
        ant_best_equation = self.construct_solution()
        print(f"\n\n\n\n>>ant_best_equation: {ant_best_equation}")
        
        if ant_best_equation:
            print(f">>ant_best_equation['rowcol']: {ant_best_equation['rowcol']}")
            if ant_best_equation['rowcol'] == 'horizontal':
                ant_eq_list = list(ant_best_equation['equation_str'])
                c_row = int(ant_best_equation['row']) # stay
                c_col = int(ant_best_equation['col']) # moving

                print(f">>ant_eq_list: {ant_eq_list}")
                print(f">>c_row: {c_row}")
                print(f">>c_col: {c_col}")
                
                for tile in ant_eq_list:
                    print(f">>ant_best_equation['tile_used']: {ant_best_equation['tile_used']}")
                    print(f">>tile: {tile}")
                    if tile in ant_best_equation['tile_used']:
                        for ai_piece in self.ai_pieces:
                            if self.curr_game_board[c_row][c_col] is None:
                                print(f">>1 self.curr_game_board[c_row][c_col]: {self.curr_game_board[c_row][c_col]}")
                                print(f">>ai_piece: {ai_piece}")
                                print(f">>ai_piece['tile']: {ai_piece['tile']}")
                                if tile == ai_piece['tile']:
                                    ant_tile = ai_piece.copy()
                                    ant_tile['row'] = c_row
                                    ant_tile['col'] = c_col
                                    self.curr_game_board[c_row][c_col] = ant_tile
                                    self.ai_pieces.remove(ai_piece)
                                    print(f">>2 self.curr_game_board[c_row][c_col]: {self.curr_game_board[c_row][c_col]}")
                                    break 
                    c_col += 1

            elif ant_best_equation['rowcol'] == 'vertical':
                ant_eq_list = list(ant_best_equation['equation_str'])
                c_row = int(ant_best_equation['row']) # moving
                c_col = int(ant_best_equation['col']) # stay

                print(f">>ant_eq_list: {ant_eq_list}")
                print(f">>c_row: {c_row}")
                print(f">>c_col: {c_col}")
                
                for tile in ant_eq_list:
                    print(f">>ant_best_equation['tile_used']: {ant_best_equation['tile_used']}")
                    print(f">>tile: {tile}")
                    if tile in ant_best_equation['tile_used']:
                        for ai_piece in self.ai_pieces:
                            if self.curr_game_board[c_row][c_col] is None:
                                print(f">>1 self.curr_game_board[c_row][c_col]: {self.curr_game_board[c_row][c_col]}")
                                print(f">>ai_piece: {ai_piece}")
                                print(f">>ai_piece['tile']: {ai_piece['tile']}")
                                if tile == ai_piece['tile']:
                                    ant_tile = ai_piece.copy()
                                    ant_tile['row'] = c_row
                                    ant_tile['col'] = c_col
                                    self.curr_game_board[c_row][c_col] = ant_tile
                                    self.ai_pieces.remove(ai_piece)
                                    print(f">>2 self.curr_game_board[c_row][c_col]: {self.curr_game_board[c_row][c_col]}")
                                    break 
                    c_row += 1
            
            for tile in self.curr_game_board:
                print(tile)
                    

            # fix later the scoring in ai
            self.AI_SCORE += ant_best_equation['eq_score']
            self.draw_total_points()
            self.draw_new_random_tiles_ai(ant_best_equation)

            for row in range(15):
                for col in range(15):
                    self.game_board[row][col] = self.curr_game_board[row][col]

            self.show_green_prompt("YOUR TURN.")
            self.AI_TURN = False
            self.PLAYER_TURN = True
        
        else:
            # PASS
            self.show_green_prompt("AI DID NOT FIND EQUATION.")
            self.show_green_prompt("YOUR TURN.")
            self.AI_TURN = False
            self.PLAYER_TURN = True
    
    def construct_solution(self):
        '''
            get the first five per row and per column
            if the array all empty or '' then the start to get the forst five per row and col is in [1] index and so on

            else if the array are not all empty then do itertools.permuatation

                compute the score of the generated equation 
                store the valid equation and its score in an array
            
            continue the same proccess for colmuns then return the valid equations and its scores
        '''
        '''
            using ant colony optimization algorithm the ai will choose which equation seems to be the most optimal
            to put in the board
        '''

        conversion_dict = {
            '^2': '**2',
            'x': '*',
            '÷': '/',
        }
        rowcol_equation = []
        
        # COL - horizontal
        rc_idx = 0
        while rc_idx < 15:
            self.curr_idx = 'horizontal'
            col_equation = []
            for row in range(15):
                if self.curr_game_board[rc_idx][row] is not None:
                    for op, replacement in conversion_dict.items():
                        temp_tile = self.curr_game_board[rc_idx][row]['tile'].replace(op, replacement)
                    col_equation.append(temp_tile)
                else:
                    col_equation.append('')

            print(f">>col_equation: {col_equation}")
            temp_ai_tiles = []
            for aai in self.ai_pieces:
                for op, replacement in conversion_dict.items():
                    if aai['tile'] == '==':
                        continue
                    aai['tile'] = aai['tile'].replace(op, replacement)
                temp_ai_tiles.append(aai['tile']) 

            print(f">>temp_ai_tiles: {temp_ai_tiles}")
            print(f">>rc_idx: {rc_idx}")
            valid_equations = self.generate_equations(col_equation, temp_ai_tiles, rc_idx)
            for v_eq in valid_equations:
                print(f">>HORIZONTAL   valid_equations: {v_eq}")
            
            if len(valid_equations) > 0:
                for ve in valid_equations:
                    rowcol_equation.append(ve)

            # input(print(f"\n>>>>>>"))
            rc_idx += 1
        
        # ROW - vertical
        rc_idx = 0
        while rc_idx < 15:
            self.curr_idx = 'vertical'
            row_equation = []
            for row in range(15):
                if self.curr_game_board[row][rc_idx] is not None:
                    for op, replacement in conversion_dict.items():
                        temp_tile = self.curr_game_board[row][rc_idx]['tile'].replace(op, replacement)
                    row_equation.append(temp_tile)
                else:
                    row_equation.append('')

            print(f">>row_equation: {row_equation}")
            temp_ai_tiles = []
            for aai in self.ai_pieces:
                for op, replacement in conversion_dict.items():
                    if aai['tile'] == '==':
                        continue
                    aai['tile'] = aai['tile'].replace(op, replacement)
                temp_ai_tiles.append(aai['tile']) 
            
            print(f">>temp_ai_tiles: {temp_ai_tiles}")
            print(f">>rc_idx: {rc_idx}")
            valid_equations = self.generate_equations(row_equation, temp_ai_tiles, rc_idx)
            for v_eq in valid_equations:
                print(f">>VERTICALL  valid_equations: {v_eq}")

            if len(valid_equations) > 0:
                for ve in valid_equations:
                    rowcol_equation.append(ve)

            # input(print(f"\n>>>>>>"))
            rc_idx += 1
        
        aco = AntColonyOptimization(rowcol_equation)
        best_solution, best_score = aco.run()
        ant_solutions = []

        for t_best in best_solution:
            ant_solutions.append(rowcol_equation[t_best])
        
        total_score = sum(solution['eq_score'] for solution in ant_solutions)
        random_num = random.uniform(0, total_score)
        cumulative_score = 0
        ant_best_equation = None
        for solution in ant_solutions:
            cumulative_score += solution['eq_score']
            if random_num <= cumulative_score:
                ant_best_equation = solution
                break
        
        print(f">>ant_best_equation: {ant_best_equation}")
        return ant_best_equation

    def generate_equations(self, curr_equation, curr_ai_tiles, rc_idx):
        eq = []
        valid_equations = []

        for i in range(0, len(curr_equation)):
            # Check if all elements in the current slice are empty
            if self.all_empty(curr_equation, i, i+5):
                continue
            else:
                eq = curr_equation[i:i+5]
                if len(eq) == 5:
                    print(f"\n>>eq: {eq}")
                    start_idx = i
                    end_idx = i+5
                    empty_indices = [j for j, char in enumerate(eq) if char is None or char == '']

                    if len(empty_indices) > 0:
                        permutations = itertools.permutations(curr_ai_tiles, len(empty_indices))

                        for perm in permutations:
                            new_equation = eq.copy()
                            for index, tile in zip(empty_indices, perm):
                                new_equation[index] = tile
                            equation_str = ''.join(new_equation)

                            # Validate equation
                            if equation_str.count('=') == 1:
                                left, right = equation_str.split('=')
                                try:
                                    if eval(left) == eval(right):
                                        # Validate board
                                        temp_curr_equation = curr_equation.copy()
                                        equation_array = list(equation_str)
                                        tile_used = [equation_array[i] for i in range(len(eq)) if eq[i] == '' or eq[i] != equation_array[i]]
                                        print(f">>tile_used: {tile_used}")

                                        # Replace empty elements in temp_curr_equation with corresponding elements from equation_array
                                        for j in range(start_idx, end_idx):
                                            if temp_curr_equation[j] == '' or temp_curr_equation[j] is None:
                                                temp_curr_equation[j] = equation_array[j - start_idx]
                                        
                                        print(f">>temp_curr_equation: {temp_curr_equation}")
                                        temp_equation_str = []
                                        equation_b = ""
                                        for elem in temp_curr_equation:
                                            if elem != '':
                                                equation_b += elem
                                            else:
                                                if equation_b:
                                                    temp_equation_str.append(equation_b)
                                                    equation_b = ""

                                        if equation_b:
                                            temp_equation_str.append(equation_b)
                                        
                                        print(f">>temp_equation_str: {temp_equation_str}")
                                        # check if each equation by row or col is valid
                                        is_valid_gen_eq = False
                                        for temp_eq in temp_equation_str:
                                            if len(temp_eq) > 1:
                                                print(f">>temp_eq: {temp_eq}")
                                                print(f">>1 is_valid_gen_eq: {is_valid_gen_eq}")

                                                is_valid_gen_eq = self.is_valid_chain_equation(temp_eq)
                                                print(f">>2 is_valid_gen_eq: {is_valid_gen_eq}")
                                        
                                                if is_valid_gen_eq:
                                                    # get equation score
                                                    temp_parts = temp_eq.split('=')
                                                    temp_part_a = temp_parts[0]
                                                    conversion_dict = {
                                                        '^2': '**2',
                                                        'x': '*',
                                                        '÷': '/',
                                                    }
                                                    for op, replacement in conversion_dict.items():
                                                        temp_part_a = temp_part_a.replace(op, replacement)
                                                    temp_part_result = eval(temp_part_a)

                                                    all_tiles = set(self.BLUE_TILES) | set(self.GREEN_TILES) | set(self.YELLOW_TILES) | set(self.RED_TILES)
                                                    eq_score = 0
                                                    if self.curr_idx == 'horizontal':
                                                        if (rc_idx, start_idx) in self.YELLOW_TILES:
                                                            eq_score += int(temp_part_result) * 2
                                                        if (rc_idx, start_idx) in self.RED_TILES:
                                                            eq_score += int(temp_part_result) * 3

                                                    elif self.curr_idx == 'vertical':
                                                        if (start_idx, rc_idx) in self.YELLOW_TILES:
                                                            eq_score += int(temp_part_result) * 2
                                                        if (start_idx, rc_idx) in self.RED_TILES:
                                                            eq_score += int(temp_part_result) * 3
                                                    
                                                    temp_eq_array = list(temp_eq)
                                                    for t_arr in temp_eq_array:
                                                        if t_arr in self.TILE_NUMBER_POINTS or self.TILE_OPERATOR_POINTS or self.TILE_EQUAL_POINTS:
                                                            tile_point = self.TILE_NUMBER_POINTS.get(t_arr) or self.TILE_OPERATOR_POINTS.get(t_arr) or self.TILE_EQUAL_POINTS.get(t_arr)
                                                            
                                                            if self.curr_idx == 'horizontal':
                                                                if (rc_idx, start_idx) in self.BLUE_TILES:
                                                                    eq_score += int(tile_point) * 2
                                                                if (rc_idx, start_idx) in self.GREEN_TILES:
                                                                    eq_score += int(tile_point) * 3

                                                                if (rc_idx, start_idx) not in all_tiles:
                                                                    eq_score += int(tile_point)

                                                            elif self.curr_idx == 'vertical':
                                                                if (start_idx, rc_idx) in self.BLUE_TILES:
                                                                    eq_score += int(tile_point) * 2
                                                                if (start_idx, rc_idx) in self.GREEN_TILES:
                                                                    eq_score += int(tile_point) * 3
                                                                
                                                                if (start_idx, rc_idx) not in all_tiles:
                                                                    eq_score += int(tile_point)
                                                    
                                                    print(f">>eq_score: {eq_score}")
                                                    temp_vEQ = {}
                                                    temp_vEQ['equation_str'] = temp_eq
                                                    temp_vEQ['tile_used'] = tile_used
                                                    temp_vEQ['eq_score'] = eq_score
                                                    temp_vEQ['rowcol'] = self.curr_idx

                                                    if self.curr_idx == 'horizontal':
                                                        temp_vEQ['col'] = start_idx
                                                        temp_vEQ['row'] = rc_idx
                                                    elif self.curr_idx == 'vertical':
                                                        temp_vEQ['col'] = rc_idx
                                                        temp_vEQ['row'] = start_idx

                                                    print(f">>temp_vEQ: {temp_vEQ} \n")

                                                    valid_equations.append(temp_vEQ)
                                            
                                except:
                                    pass

        return valid_equations

    def all_empty(self, arr, start, end):
        return all(elem is None or elem == '' for elem in arr[start:end])

    def is_valid_chain_equation(self, equation):
        conversion_dict = {
            '^2': '**2',
            'x': '*',
            '÷': '/',
            '=': '==',
        }
        for op, replacement in conversion_dict.items():
            equation = equation.replace(op, replacement)

        # Split the equation by the equality operator
        parts = equation.split('==')
        
        if len(parts) < 2:
            return False
        
        try:
            # Evaluate the first part
            reference_value = eval(parts[0])
            
            # Check that all parts evaluate to the same value
            for part in parts[1:]:
                if eval(part) != reference_value:
                    return False
                    
            return True
        except:
            # If evaluation fails, it's not a valid equation
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
    
    def draw_new_random_tiles_ai(self, ant_best_equation):
        used_tiles = [piece for piece in ant_best_equation['tile_used']]

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
            self.ai_pieces.append(piece)
            if new_tile in self.TILE_PCS:
                self.TILE_PCS[new_tile] -= 1

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

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

        # define tile tile status
        self.START_TILE = (7,7)
        self.GREEN_TILES = [
            (0,3), (0,11),
            (1,5), (1,9),
            (3,0), (3,7), (3,14),
            (5,1), (5,13), 
            (6,6), (6,8),
            (7,3), (7,11),
            (8,6), (8,8),
            (9,1), (9,13),
            (11,0), (11,7), (11,14),
            (13,5), (13,9),
            (14,3), (14,11), 
        ]
        self.BLUE_TILES = [
            (2,4), (2,10),
            (4,2), (4,6), (4,8), (4,12),
            (5,5), (5,9),
            (6,4), (6,10),
            (8,4), (8,10),
            (9,5), (9,9),
            (10,2), (10,6), (10,8), (10,12),
            (12,4), (12,10),
        ]
        self.YELLOW_TILES = [
            (1,1), (1,13),
            (2,2), (2,12),
            (3,3), (3,11),
            (4,4), (4,10),
            (10,4), (10,10),
            (11,3), (11,11),
            (12,2), (12,12),
            (13,1), (13,13),
        ]
        self.RED_TILES = [
            (0,0), (0,7), (0,14),
            (7,0), (7,14),
            (14,0), (14,7), (14,14),
        ]
        
        # colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.YELLOW = (255, 255, 0)

        # board details
        self.TILE_SIZE = 35
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
            '1': 10, '2': 10, '3': 10, '4': 10, '5': 10,
            '6': 10, '7': 10, '8': 10, '9': 10, '0': 10,
            
            '+': 10, '-': 10, 'x': 8, '÷': 6, 
            '^2': 5, '√': 5,
            '=': 10, 'blank': 10,
        }
    
    def run(self):
        self.load_assets()
        self.draw_bg()
        self.draw_board()
        self.draw_pieces_pcs()
        self.get_player_pieces()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                
            
            self.display.blit(self.math_mender_bg, (0, 0))
            self.draw_board()
            self.draw_pieces_pcs()
            self.draw_player_pieces()
            pygame.display.flip()
            self.clock.tick(self.FPS)
    
    def draw_bg(self):
        self.math_mender_bg = pygame.image.load(os.path.join(self.images_dir, "GAME_BG.png"))

    def draw_board(self):
        for row in range(15):
            for col in range(15):
                tile_color = self.WHITE
                font_text = ''

                if (row, col) in self.GREEN_TILES:
                    tile_color = self.GREEN
                    # font_text = '3X\nPCS'
                    font_text = '3N'
                elif (row, col) in self.BLUE_TILES:
                    tile_color = self.BLUE
                    # font_text = '2X\nPCS'
                    font_text = '2N'
                elif (row, col) in self.YELLOW_TILES:
                    tile_color = self.YELLOW
                    # font_text = '2X\nEQ'
                    font_text = '2A'
                elif (row, col) in self.RED_TILES:
                    tile_color = self.RED
                    # font_text = '3X\nEQ'
                    font_text = '3A'
                elif (row, col) == self.START_TILE:
                    tile_color = self.YELLOW
                    font_text = 'START'

                x = (col + 11) * (self.TILE_SIZE + self.TILE_MARGIN)
                y = (row + 0.5) * (self.TILE_SIZE + self.TILE_MARGIN)

                pygame.draw.rect(self.display, tile_color, (x, y, self.TILE_SIZE, self.TILE_SIZE))
                pygame.draw.rect(self.display, self.BLACK, (x, y, self.TILE_SIZE, self.TILE_SIZE), 1)

                if font_text:
                    lines = font_text.split('\n')
                    total_height = len(lines) * self.FONT_SIZE
                    for i, line in enumerate(lines):
                        text_surface = self.FONT.render(line, True, self.FONT_COLOR)
                        text_rect = text_surface.get_rect(center=(x + self.TILE_SIZE / 2, y + (i + 0.5) * (self.TILE_SIZE / len(lines))))
                        self.display.blit(text_surface, text_rect)

    def draw_pieces_pcs(self):
        x_offsets = [20, 90, 150, 210]
        y_offset = 170
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
        selected_tiles = random.sample(list(self.TILE_PCS.keys()), 7)
        self.player_pieces = [(tile, self.TILE_NUMBER_POINTS.get(tile) or self.TILE_OPERATOR_POINTS.get(tile) or self.TILE_EQUAL_POINTS.get(tile) or 0) for tile in selected_tiles]
        for tile, _ in self.player_pieces:
            if tile in self.TILE_PCS:
                self.TILE_PCS[tile] -= 1

    def draw_player_pieces(self):
        x_offset = 20
        y_offset = 380  
        line_spacing = 40
        self.TILE_SIZE_B = 42

        def draw_tile(tile, points, x, y):
            tile_surface = pygame.Surface((self.TILE_SIZE_B, self.TILE_SIZE_B))
            tile_surface.fill(self.WHITE)
            pygame.draw.rect(tile_surface, self.WHITE, (2, 2, self.TILE_SIZE_B - 4, self.TILE_SIZE_B - 4))
            pygame.draw.rect(tile_surface, self.BLACK, (0, 0, self.TILE_SIZE_B, self.TILE_SIZE_B), 1)

            # Render the text
            text_surface = self.FONT_PCS.render(tile, True, self.BLACK)
            # Calculate the position to center the text on the tile
            text_rect = text_surface.get_rect(center=(self.TILE_SIZE_B // 2, self.TILE_SIZE_B // 2))
            # Blit the text onto the tile surface
            tile_surface.blit(text_surface, text_rect)

            # Render the value in smaller font at the lower right corner
            small_font = pygame.font.Font(None, self.FONT_SIZE)
            value_surface = small_font.render(str(points), True, self.RED)
            value_rect = value_surface.get_rect(bottomright=(self.TILE_SIZE_B - 5, self.TILE_SIZE_B - 5))
            tile_surface.blit(value_surface, value_rect)

            # Blit the tile surface onto the display
            self.display.blit(tile_surface, (x, y))

        for i, (tile, points) in enumerate(self.player_pieces):
            draw_tile(tile, points, x_offset + i * (self.TILE_SIZE_B + 10), y_offset)

    def get_ai_pieces(self):
        pass

    def load_assets(self):
        self.assets_dir = os.path.join("assets")
        self.images_dir = os.path.join(self.assets_dir, "images")
        self.FONT = pygame.font.Font(None, self.FONT_SIZE)

### remove after dev
if __name__ == "__main__":
    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    game_state_manager = GameStateManager('MathMender')
    game_state_manager.set_state(MathMender(screen, game_state_manager))
    game_state_manager.get_state().run()
###
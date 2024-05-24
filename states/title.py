import pygame
import os

### remove after dev
from game_state_manager import GameStateManager
###

class Title():
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager
        self.SCREEN_WIDTH = 1000
        self.SCREEN_HEIGHT = 600
        self.FPS = 60
        self.clock = pygame.time.Clock()

        # Define the game board area
        self.game_board_rect = pygame.Rect(100, 100, 800, 400)  # Adjust position and size as needed

        # Initialize an array to store dropped piece positions
        self.dropped_positions = []

        # for drag and drop
        self.dragging = False
        self.dragged_rect = None
        self.offset_x = 0
        self.offset_y = 0

        # Initialize the rectangles
        self.rectangles = [
            {"id": 1, "rect": pygame.Rect(370, 248, 255, 50)},
            {"id": 2, "rect": pygame.Rect(370, 326, 255, 50)},
            {"id": 3, "rect": pygame.Rect(370, 402, 255, 50)},
        ]

    def run(self):
        ### change the import to this after dev
        # from states.instruction import Instruction
        # from states.math_mender import MathMender
        from instruction import Instruction
        from math_mender import MathMender

        self.load_assets()
        self.draw_bg()
        self.draw_rect_btns()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        for rect in self.rectangles:
                            if rect["rect"].collidepoint(mouse_x, mouse_y):
                                self.dragging = True
                                self.dragged_rect = rect
                                self.offset_x = rect["rect"].x - mouse_x
                                self.offset_y = rect["rect"].y - mouse_y
                                break
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        if self.dragging:
                            self.dragging = False
                            mouse_x, mouse_y = pygame.mouse.get_pos()
                            if self.game_board_rect.collidepoint(mouse_x, mouse_y):
                                # Store the position of the dropped piece
                                self.dropped_positions.append((mouse_x, mouse_y))
                                print("Tile dropped in the game board area")
                            else:
                                print("Tile dropped outside the game board area")
                            
                            for rect in self.rectangles:
                                if rect["rect"].collidepoint(mouse_x, mouse_y):
                                    print("Rectangle clicked:", rect["id"])
                                    if rect["id"] == 1:
                                        print("button 1 is clicked")
                                        self.gameStateManager.set_state(MathMender(self.display, self.gameStateManager))
                                        self.gameStateManager.get_state().run()
                                    elif rect["id"] == 2:
                                        print("button 2 is clicked")
                                        self.gameStateManager.set_state(Instruction(self.display, self.gameStateManager))
                                        self.gameStateManager.get_state().run()
                                    elif rect["id"] == 3:
                                        print("button 3 is clicked")
                                        pygame.quit()
                                        quit()
                elif event.type == pygame.MOUSEMOTION:
                    if self.dragging:
                        mouse_x, mouse_y = event.pos
                        new_x = mouse_x + self.offset_x
                        new_y = mouse_y + self.offset_y

                        # Prevent the rect from going outside the screen
                        if 0 <= new_x <= self.SCREEN_WIDTH - self.dragged_rect["rect"].width:
                            self.dragged_rect["rect"].x = new_x
                        if 0 <= new_y <= self.SCREEN_HEIGHT - self.dragged_rect["rect"].height:
                            self.dragged_rect["rect"].y = new_y

            self.display.blit(self.main_menu_bg, (0, 0))
            self.draw_rect_btns()
            # Comment out or remove the line below to remove the blue outline square
            # pygame.draw.rect(self.display, (0, 0, 255), self.game_board_rect, 2)  # Draw the game board area
            pygame.display.flip()
            self.clock.tick(self.FPS)

    def draw_bg(self):
        self.main_menu_bg = pygame.image.load(os.path.join(self.images_dir, "MAIN_MENU_BG.png"))

    def draw_rect_btns(self):
        transparent_surface = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.SRCALPHA)
        for rect in self.rectangles:
            pygame.draw.rect(transparent_surface, (255, 255, 255, 0), rect["rect"], 0)  # Set alpha to 0 for full transparency
        self.display.blit(transparent_surface, (0, 0))

    def load_assets(self):
        self.assets_dir = os.path.join("assets")
        self.images_dir = os.path.join(self.assets_dir, "images")

        # Initialize the rectangles
        self.rectangles = [
            {"id": 1, "rect": pygame.Rect(370, 248, 255, 50)},
            {"id": 2, "rect": pygame.Rect(370, 326, 255, 50)},
            {"id": 3, "rect": pygame.Rect(370, 402, 255, 50)},
        ]

### remove after dev
if __name__ == "__main__":
    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    game_state_manager = GameStateManager('title')
    game_state_manager.set_state(Title(screen, game_state_manager))
    game_state_manager.get_state().run()
###

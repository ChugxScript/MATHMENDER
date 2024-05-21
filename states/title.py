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

    def run(self):
        ### change the import to this after dev
        # from states.instruction import Instruction
        # from states.math_mender import MathMender
        from instruction import Instruction
        from math_mender import MathMender

        self.load_assets()
        self.draw_bg()
        self.draw_rect_btns()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        for rect in self.rectangles:
                            if rect["rect"].collidepoint(mouse_x, mouse_y):
                                print("Rectangle clicked:", rect["id"])
                                if rect["id"] == 1:
                                    print("button 1 is clicked")
                                    self.gameStateManager.set_state(MathMender(self.display, self.gameStateManager))
                                    self.gameStateManager.get_state().run()
                                if rect["id"] == 2:
                                    print("button 2 is clicked")
                                    self.gameStateManager.set_state(Instruction(self.display, self.gameStateManager))
                                    self.gameStateManager.get_state().run()
                                if rect["id"] == 3:
                                    print("button 3 is clicked")
                                    pygame.quit()
                                    quit()
            
            self.display.blit(self.main_menu_bg, (0, 0))
            self.draw_rect_btns()
            pygame.display.flip()
            self.clock.tick(self.FPS)

    def draw_bg(self):
        self.main_menu_bg = pygame.image.load(os.path.join(self.images_dir, "MAIN_MENU_BG.png"))

    def draw_rect_btns(self):
        WHITE = (255,255 , 255)
        self.rectangles = [
            {"id": 1, "rect": pygame.Rect(370, 248, 255, 50)},
            {"id": 2, "rect": pygame.Rect(370, 326, 255, 50)},
            {"id": 3, "rect": pygame.Rect(370, 402, 255, 50)},
        ]
        for rect in self.rectangles:
            pygame.draw.rect(self.display, WHITE, rect["rect"], 1)

    def load_assets(self):
        self.assets_dir = os.path.join("assets")
        self.images_dir = os.path.join(self.assets_dir, "images")

### remove after dev
if __name__ == "__main__":
    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    game_state_manager = GameStateManager('title')
    game_state_manager.set_state(Title(screen, game_state_manager))
    game_state_manager.get_state().run()
###
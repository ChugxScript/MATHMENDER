import pygame
import os

class Instruction():
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager
        self.FPS = 60
        self.clock = pygame.time.Clock()
    
    def run(self):
        ### change the import to this after dev
        # from states.title import Title
        from title import Title

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
                                    self.gameStateManager.set_state(Title(self.display, self.gameStateManager))
                                    self.gameStateManager.get_state().run()

            self.display.blit(self.instruction_bg, (0, 0))
            self.draw_rect_btns()
            pygame.display.flip()
            self.clock.tick(self.FPS)

    def draw_bg(self):
        self.instruction_bg = pygame.image.load(os.path.join(self.images_dir, "INSTRUCTION_BG.png"))

    def draw_rect_btns(self):
        WHITE = (255,255 , 255)
        self.rectangles = [
            {"id": 1, "rect": pygame.Rect(370, 544, 205, 40)},
        ]
        for rect in self.rectangles:
            pygame.draw.rect(self.display, WHITE, rect["rect"], 1)

    def load_assets(self):
        self.assets_dir = os.path.join("assets")
        self.images_dir = os.path.join(self.assets_dir, "images")
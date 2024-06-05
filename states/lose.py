import os
import pygame

class Lose():
    def __init__(self, display, gameStateManager):
        pygame.init()
        self.display = display
        self.gameStateManager = gameStateManager
        self.FPS = 60
        self.clock = pygame.time.Clock()      
        self.RED = (255, 0, 0)  
        self.WHITE = (255, 255, 255)  

    def run(self, player_score, ai_score):
        from states.title import Title
        self.load_assets()
        self.draw_bg()
        self.draw_rectangles()

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
                                    self.gameStateManager.set_state(Title(self.display, self.gameStateManager))
                                    self.gameStateManager.get_state().run()
                                    
                                if rect["id"] == 2:
                                    pygame.quit()
                                    quit()
            
            self.display.blit(self.lose_bg, (0, 0))
            self.player_score_text = self.font.render(f'{player_score}', True, self.RED)
            self.display.blit(self.player_score_text, (640, 248))
            self.ai_score_text = self.font.render(f'{ai_score}', True, self.WHITE)
            self.display.blit(self.ai_score_text, (680, 305))
            self.draw_rectangles()
            pygame.display.flip()
            self.clock.tick(self.FPS)

    def draw_rectangles(self):
        self.rectangles = [
            {"id": 1, "rect": pygame.Rect(458, 430, 160, 47)},
            {"id": 2, "rect": pygame.Rect(645, 430, 160, 47)}
        ]
        for rect in self.rectangles:
            pygame.draw.rect(self.display, self.WHITE, rect["rect"], 1)
    
    def draw_bg(self):
        self.lose_bg = pygame.image.load(os.path.join(self.images_dir, "LOSE.png"))

    def load_assets(self):
        self.assets_dir = os.path.join("assets")
        self.images_dir = os.path.join(self.assets_dir, "images")
        self.font = pygame.font.Font(None, 36)
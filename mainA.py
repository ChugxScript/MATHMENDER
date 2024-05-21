import pygame
import os
from states.game_state_manager import GameStateManager

class Game():
    def __init__(self):
        pygame.init()
        self.SCREEN_WIDTH = 1000
        self.SCREEN_HEIGHT = 600
        self.FPS = 60
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.game_state_manager = GameStateManager('title')

    def run(self):
        from states.title import Title
        pygame.display.set_caption("MATH MENDER")

        ### icon will be added later
        # icon = pygame.image.load(os.path.join('assets', 'board', 'img', 'GameIcon1.png'))
        # pygame.display.set_icon(icon)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            self.game_state_manager.set_state(Title(self.screen, self.game_state_manager))
            self.game_state_manager.get_state().run()
            
            pygame.display.flip()
            self.clock.tick(self.FPS)


if __name__ == "__main__":
    g = Game()
    g.run()
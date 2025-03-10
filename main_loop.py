import pygame

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800,600))
        pygame.display.set_caption("CSshot Game")
        self.running = True

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.fill((173,216,230))
            pygame.display.flip()

        pygame.quit()
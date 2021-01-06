import pygame

class Game:
    def __init__(self, screen):
        self.SCREEN = screen
        self.running = True

    def update(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def render(self):

        # Fill the background with white
        self.SCREEN.fill((255, 255, 255))

        # Draw a solid blue circle in the center
        pygame.draw.circle(self.SCREEN, (0, 0, 255), (250, 250), 75)

        # Update the display
        pygame.display.update()

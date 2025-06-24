import pygame
import random

pygame.init()

class DrawInformation:
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    GREEN = 0, 255, 0
    RED = 255, 0, 0
    GREY = 128, 128, 128
    BACKGROUND_COLOUR = WHITE
    GRADIENTS = [
        (128, 128, 128),
        (160, 160, 160),
        (192, 192, 192)
    ]
    SIDE_PAD = 100
    TOP_PAD = 150

    def __init__(self, width, height, lst):
        self.width = width
        self.height = height
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Algorithm Visualizer")
        self.set_list(lst)

    def set_list(self, lst):
        self.lst = lst
        self.max_val = max(lst)
        self.min_val = min(lst)

        self.block_width = (self.width - self.SIDE_PAD) // len(lst)
        self.block_height = (self.height - self.TOP_PAD) // (self.max_val - self.min_val)
        self.start_x = self.SIDE_PAD // 2

    def draw(self):
        self.window.fill(self.BACKGROUND_COLOUR)
        self.draw_list()  # FIXED: calling internal method with self
        pygame.display.update()

    def draw_list(self):
        for i, val in enumerate(self.lst):
            x = self.start_x + i * self.block_width
            y = self.height - (val - self.min_val) * self.block_height

            color = self.GRADIENTS[i % 3]
            pygame.draw.rect(self.window, color, (x, y, self.block_width, self.height))

    @staticmethod
    def generate_starting_list(n, min_val, max_val):
        return [random.randint(min_val, max_val) for _ in range(n)]

def main():
    run = True
    clock = pygame.time.Clock()
    n = 50
    min_val = 0
    max_val = 100
    lst = DrawInformation.generate_starting_list(n, min_val, max_val)
    draw_info = DrawInformation(800, 600, lst)

    while run:
        clock.tick(60)
        draw_info.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    pygame.quit()

if __name__ == "__main__":
    main()

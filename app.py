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
    FONT = pygame.font.SysFont('poppins', 30)
    LARGE_FONT = pygame.font.SysFont('comicsans', 40)

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
        # Avoid division by zero
        self.block_height = (self.height - self.TOP_PAD) // (self.max_val - self.min_val) if self.max_val != self.min_val else 1
        self.start_x = self.SIDE_PAD // 2

    def draw(self):
        self.window.fill(self.BACKGROUND_COLOUR)
        controls = self.FONT.render('R - Reset | SPACE - Start Sorting | A - Ascending | D - Descending', 1, self.BLACK)
        self.window.blit(controls, (self.width / 2 - controls.get_width() / 2, 5))

        sorting = self.FONT.render('I + SPACE - Insertion Sort , B + SPACE - Bubble Sort', 1, self.BLACK)
        self.window.blit(sorting, (self.width / 2 - sorting.get_width() / 2, 35))

        self.draw_list()
        pygame.display.update()

    def draw_list(self, color_positions={}, clear_bg=False):
        if clear_bg:
            clear_rect = (self.SIDE_PAD // 2, self.TOP_PAD, self.width - self.SIDE_PAD, self.height - self.TOP_PAD)
            pygame.draw.rect(self.window, self.BACKGROUND_COLOUR, clear_rect)
        for i, val in enumerate(self.lst):
            x = self.start_x + i * self.block_width
            y = self.height - (val - self.min_val) * self.block_height

            color = self.GRADIENTS[i % 3]
            if i in color_positions:
                color = color_positions[i]

            pygame.draw.rect(self.window, color, (x, y, self.block_width, self.height))
        if clear_bg:
            pygame.display.update()

    @staticmethod
    def generate_starting_list(n, min_val, max_val):
        return [random.randint(min_val, max_val) for _ in range(n)]

    def bubble_sort(self, ascending=True):
        lst = self.lst
        for j in range(len(lst) - 1):
            for k in range(len(lst) - 1 - j):
                num1 = lst[k]
                num2 = lst[k + 1]
                if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                    lst[k], lst[k + 1] = lst[k + 1], lst[k]
                    self.draw_list({k: self.GREEN, k + 1: self.RED}, True)
                    yield True
        return lst

    def insertion_sort(self, ascending=True):
        lst = self.lst
        for i in range(1, len(lst)):
            current = lst[i]
            j = i - 1
            while j >= 0 and ((lst[j] > current and ascending) or (lst[j] < current and not ascending)):
                lst[j + 1] = lst[j]
                self.draw_list({j: self.GREEN, j + 1: self.RED}, True)
                yield True
                j -= 1
            lst[j + 1] = current
        return lst

def main():
    run = True
    clock = pygame.time.Clock()
    n = 50
    min_val = 0
    max_val = 100
    lst = DrawInformation.generate_starting_list(n, min_val, max_val)
    draw_info = DrawInformation(800, 600, lst)
    sorting = False
    ascending = True

    sorting_algorithm = draw_info.bubble_sort
    sorting_algo_name = "Bubble Sort"
    sorting_algorithm_generator = None

    while run:
        clock.tick(45)
        if sorting:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting = False
        else:
            draw_info.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_r:
                lst = DrawInformation.generate_starting_list(n, min_val, max_val)
                draw_info.set_list(lst)
                sorting = False
            elif event.key == pygame.K_SPACE and not sorting:
                sorting = True
                sorting_algorithm_generator = sorting_algorithm(ascending)
            elif event.key == pygame.K_a and not sorting:
                ascending = True
            elif event.key == pygame.K_d and not sorting:
                ascending = False
            elif event.key == pygame.K_b and not sorting:
                sorting_algorithm = draw_info.bubble_sort
                sorting_algo_name = "Bubble Sort"
            elif event.key == pygame.K_i and not sorting:
                sorting_algorithm = draw_info.insertion_sort
                sorting_algo_name = "Insertion Sort"
    pygame.quit()

if __name__ == "__main__":
    main()

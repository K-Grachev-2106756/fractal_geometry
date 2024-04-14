import pygame
import numpy as np
import os
import time


class IFS:

    def __init__(self, coeffs):
        # Initialize with coefficients
        self.coeffs = coeffs


    def create_functions(self):
        # Convert coefficients into transformation matrices
        transformations = []
        for c in self.coeffs:
            matrix = np.array(c[:4]).reshape(2, 2)
            translation = np.array(c[4:])
            transformations.append((matrix, translation))

        return transformations


    def create_attractor(self, base_surface, n_iter):
        # Create attractor applying the transformations to the base surface
        size = base_surface.get_size()
        transformations = self.create_functions()

        result_surface = pygame.Surface(size)
        iteration_surface = pygame.Surface(size)

        result_surface.blit(base_surface, (0, 0))

        size_np = np.array(size)
        for _ in range(n_iter):
            iteration_surface.fill(WHITE)
            for transform in transformations:
                size_scale = np.int32(np.round(transform[0] @ size_np))
                offset = np.int32(np.round(transform[1] * size_np))
                scaled_surface = pygame.transform.smoothscale(result_surface, size_scale)
                iteration_surface.blit(scaled_surface, offset)
            result_surface.blit(iteration_surface, (0, 0))

        return result_surface


if __name__ == "__main__":
    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    # Set window position
    x_position = 20
    y_position = 40
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x_position, y_position)

    pygame.init()

    # Window dimensions
    window_width = 1200
    window_height = 600

    # Set up the display
    screen = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Iterated Function System")
    screen.fill(WHITE)

    # Frame rate control
    FPS = 30
    clock = pygame.time.Clock()

    # Create base surface
    base_surface = pygame.Surface((200, 200))
    base_surface.fill(BLACK)
    pygame.draw.rect(base_surface, WHITE, base_surface.get_rect(), 60)

    # Define coefficients for transformations
    coefficients = [
        (0.5, 0, 0, 0.5, 0, 0),
        (0.5, 0, 0, 0.5, 0.5, 0),
        (0.5, 0, 0, 0.5, 0.25, 0.433),
    ]

    # Create IFS object and generate attractor
    ifs = IFS(coefficients)
    result_surface = ifs.create_attractor(base_surface, 0)
    result_surface = pygame.transform.flip(result_surface, False, True)
    screen.blit(result_surface, (100, 200))

    # Iteration settings
    num_iterations = 1
    step = 0

    # Main loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        # Control iteration and update display
        step += 1
        if step > FPS and num_iterations < 8:
            time.sleep(1)
            step = 0
            result_surface = ifs.create_attractor(base_surface, num_iterations)
            result_surface = pygame.transform.flip(result_surface, False, True)
            screen.blit(result_surface, (100, 200))
            num_iterations += 1

            if num_iterations == 7:
                pygame.image.save(screen, "result.png")

        pygame.display.update()
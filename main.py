import pygame

pygame.init()

BLACK = (0, 0, 0)
GREY = (128, 128, 128)
YELLOW = (255, 255, 0)

WIDTH, HEIGHT = 800, 800
TILE_SIZE = 20
GRID_WIDTH = WIDTH // TILE_SIZE
GRID_HEIGHT = HEIGHT // TILE_SIZE
FPS = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()

simulation_active = False  # Simulation flag

def draw_grid(positions):
    for position in positions:
        col, row = position
        top_left = (col * TILE_SIZE, row * TILE_SIZE)
        pygame.draw.rect(screen, BLACK, (*top_left, TILE_SIZE, TILE_SIZE))    

    for row in range(GRID_HEIGHT):
        pygame.draw.line(screen, BLACK, (0, row * TILE_SIZE), (WIDTH, row * TILE_SIZE))
    for col in range(GRID_WIDTH):
        pygame.draw.line(screen, BLACK, (col * TILE_SIZE, 0), (col * TILE_SIZE, HEIGHT))

def simulate_step(positions):
    new_positions = set()
    for position in positions:
        col, row = position
        neighbours = [
            (col - 1, row - 1),
            (col, row - 1),
            (col + 1, row - 1),
            (col - 1, row),
            (col + 1, row),
            (col - 1, row + 1),
            (col, row + 1),
            (col + 1, row + 1)
        ]
        living_neighbours = sum((neighbour in positions) for neighbour in neighbours)
        if living_neighbours == 3 or (living_neighbours == 2 and position in positions):
            new_positions.add(position)
        for neighbour in set(neighbours):
            if neighbour not in positions:
                col, row = neighbour
                surrounding = [
                    (col - 1, row - 1),
                    (col, row - 1),
                    (col + 1, row - 1),
                    (col - 1, row),
                    (col + 1, row),
                    (col - 1, row + 1),
                    (col, row + 1),
                    (col + 1, row + 1)
                ]
                living_surrounding = sum((n in positions) for n in surrounding)
                if living_surrounding == 3:
                    new_positions.add(neighbour)
    return new_positions

def main():
    running = True
    positions = set()
    global simulation_active
    while running:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                col, row = pygame.mouse.get_pos()
                col = col // TILE_SIZE
                row = row // TILE_SIZE
                position = (col, row)
                if position in positions:
                    positions.remove(position)
                else:
                    positions.add(position)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    positions = simulate_step(positions)
                if event.key == pygame.K_t:  # Toggle continuous simulation
                    simulation_active = not simulation_active

        if simulation_active:  # Check simulation flag independently
            positions = simulate_step(positions)

        screen.fill(GREY)
        draw_grid(positions)
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
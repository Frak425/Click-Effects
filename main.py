import pygame
from star_explosion import StarExplosion
from projectile import Projectile

pygame.init()

screenInfo = pygame.display.Info()
screen_x = screenInfo.current_w
screen_y = screenInfo.current_h
screen = pygame.display.set_mode((screen_x, screen_y))
clock = pygame.time.Clock()

particles = []
particle_props = {
    "particle_size": 10,
    "a_bounds": (-.2, -.1), #same
    "v_bounds": (3, 3.1),
    "p_y_bounds": (-10, 10),
    "p_x_bounds": (-10, 10),
    "r_a_bounds": (-1, 1),
    "r_v_bounds": (.75, 1.75),
    "r_bounds": (0, 180),
    "theta_bounds": (80, 100),
    "opacity_type": "linear",
    "duration": 1.2,
    "num_particles": 10
}


running = True
start_time = pygame.time.get_ticks()

update_list = []
while running:

    screen.fill((0, 0, 0))

    elapsed_time = (pygame.time.get_ticks() - start_time) / 1000  

    for event in pygame.event.get():
        
        if event == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                star_exp_duration = 1
                update_list.append(StarExplosion(screen, particle_props, (x, y), elapsed_time))

    update_list = [item for item in update_list if item.animating]
    for item in update_list:
        item.update(elapsed_time)

    pygame.display.flip()
            
    clock.tick(60)

pygame.quit()
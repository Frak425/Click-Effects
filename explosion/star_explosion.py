import pygame
import random
import pytweening as tween
import particle

"""
    "particle_size" 
    "a_bounds"
    "v_bounds"
    "p_y_bounds"
    "p_x_bounds"
    "r_a_bounds"
    "r_v_bounds"
    "r_bounds"
    "theta_bounds"
    "opacity_type"
    "duration"
    "num_particles"
"""

class StarExplosion:
    def __init__(self, screen: pygame.Surface, props: object, location: tuple, starting_time: float) -> None:
        self.screen = screen
        self.location = location
        self.particle_types = ["square", "rotated_square", "circle"]
        self.props = props
        self.num_particles = self.props["num_particles"]

        #parallel lists
        self.particle_names = []
        self.particle_objects: list[particle.Particle] = []

        for i in range(self.num_particles):
            rand_idx = random.randint(0, len(self.particle_types) - 1)
            self.particle_names.append(self.particle_types[rand_idx])

        self.particle_size = self.props["particle_size"]
        self.duration = self.props["duration"]

        #start time
        self.animating = True
        self.starting_time = starting_time
        self.time_elapsed = 0

        
        self.create_particles()

    def create_particles(self) -> None:
        for name in self.particle_names:
            if name == "circle":
                circle_img = pygame.surface.Surface((self.particle_size, self.particle_size))
                pygame.draw.circle(circle_img, (100, 100, 100, 255), (self.particle_size / 2, self.particle_size / 2), self.particle_size * .4, 1)
                self.particle_objects.append(particle.Particle(self.screen, circle_img, self.props))
            elif name == "square":
                square_img = pygame.surface.Surface((self.particle_size, self.particle_size), pygame.SRCALPHA)
                pygame.draw.rect(square_img, (100, 100, 100, 0), [self.particle_size * .1, self.particle_size * .1, self.particle_size * .8, self.particle_size * .8], 1)
                self.particle_objects.append(particle.Particle(self.screen, square_img, self.props))

            elif name == "rotated_square":
                rotated_square_img = pygame.surface.Surface((self.particle_size, self.particle_size))
                pygame.draw.rect(rotated_square_img, (100, 100, 100, 255), [self.particle_size * .1, self.particle_size * .1, self.particle_size * .8, self.particle_size * .8], 3)
                pygame.transform.rotate(rotated_square_img, 45)
                self.particle_objects.append(particle.Particle(self.screen, rotated_square_img, self.props))
            else:
                print("Error in particle_names. Name not found")

        
    def update(self, new_time) -> None: # also draws particles
        if self.time_elapsed >= self.duration: #check is animation is over before updating
            self.animating = False
            return
        
        dt = new_time - self.time_elapsed
        self.time_elapsed = new_time - self.starting_time
        t = self.time_elapsed / self.duration
        #self.time = self.current_time
        for particle in self.particle_objects:
            particle.update_info(dt, t)

        self.draw_particles()

    def draw_particles(self):
        for particle in self.particle_objects:
            particle.draw_particle(self.location)
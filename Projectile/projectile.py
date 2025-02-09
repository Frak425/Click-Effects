import pygame
import random
import pytweening as tween
from particle import Particle

class Projectile():
    def __init__(self, screen: pygame.Surface, main_particle_props: object, main_particle_sheet: pygame.Surface, main_particle_size: tuple, trailing_particle_props: object, trailing_particles_images: list[pygame.Surface], trailing_particle_prob_per_frame: int, location: tuple, duration: int, starting_time: float, theta: int, velocity: float) -> None:
        #animation attributes
        self.screen = screen
        self.location = location
        self.duration = duration
        self.starting_time = starting_time
        self.prob = trailing_particle_prob_per_frame

        #properties of different types of particles
        self.main_particle_props = main_particle_props
        self.trailing_particle_props = trailing_particle_props

        #main projectile
        self.main_particle_sheet = main_particle_sheet
        self.main_particle_size = main_particle_size
        self.main_particle_image = pygame.surface.Surface(self.main_particle_size)
        self.main_particle_image.blit(self.main_particle_sheet, [0, 0, self.main_particle_size[0], self.main_particle_size[1]])
        self.main_particle_object = Particle(self.screen, self.main_particle_image, self.trailing_particle_props)
        
        #trailing particle 
        self.trailing_particles_images = trailing_particles_images
        self.particle_objects: list[Particle] = [self.main_particle_object]
        self.trailing_particle_locations: list[tuple] = [self.location]


        #create_projectile_surfaces
        pass

    def add_to_particle_trail(self):
        test = random.random()
        if (test <= self.prob):
            self.particle_objects.append(self.create_particle(self.location))
            self.trailing_particle_locations.append(self.location)

    def create_particle(self) -> pygame.Surface:
        particle_idx = random.randint(0, len(self.trailing_particles_images) - 1)
        return Particle(self.screen, self.trailing_particles_images[particle_idx], self.trailing_particle_props)

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

    def draw_particles(self, location_i) -> None:
        #draw main particle
        self.main_particle_object.draw_particle(location_i)
        #draw falloff_particles
        for trailing_particle in self.trailing_particle_objects:
            trailing_particle.draw_particle(location_i)

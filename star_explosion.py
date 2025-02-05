import pygame
from pygame.surface import *
from particle import Particle
import random
import pytweening as tween
import os

"""
    "particle_size" 
    "a_bounds"
    "v_bounds"
    "p_y_bounds"
    "p_x_bounds"
    "r_a_bounds"
    "r_v_bounds"
    "r_bounds"
    "opacity_type"
    "duration"
    "num_particles"
"""

class StarExplosion:
    def __init__(self, screen: Surface, props: object, location: tuple, starting_time: float) -> None:
        self.screen = screen
        self.location = location
        self.particle_types = ["square", "rotated_square", "circle"]
        self.num_particles = props["num_particles"]

        #parallel lists
        self.particle_names = []
        self.particle_objects = []

        for i in range(self.num_particles):
            rand_idx = random.randint(0, len(self.particle_types) - 1)
            self.particle_names.append(self.particle_types[rand_idx])

        self.particle_size = props["particle_size"]
        self.duration = props["duration"]

        #start time
        self.animating = True
        self.starting_time = starting_time
        self.time_elapsed = 0

        self.a_bounds = props["a_bounds"]
        self.v_bounds = props["v_bounds"]
        self.p_y_bounds = props["p_y_bounds"]
        self.p_x_bounds = props["p_x_bounds"]
        self.r_a_bounds = props["r_a_bounds"]
        self.r_v_bounds = props["r_v_bounds"]
        self.r_bounds = props["r_bounds"]
        self.opacity_type = props["opacity_type"]

        self.create_particles()

    def create_particles(self) -> None:
        for name in self.particle_names:
            if name == "circle":
                circle_img = pygame.surface.Surface((self.particle_size, self.particle_size))
                pygame.draw.circle(circle_img, (100, 100, 100, 255), (self.particle_size / 2, self.particle_size / 2), self.particle_size * .4, 1)
                self.particle_objects.append(Particle(self.screen, circle_img, self.a_bounds, self.v_bounds, self.p_y_bounds, self.p_x_bounds, self.r_a_bounds, self.r_v_bounds, self.r_bounds, self.opacity_type))
            elif name == "square":
                square_img = pygame.surface.Surface((self.particle_size, self.particle_size), pygame.SRCALPHA)
                pygame.draw.rect(square_img, (100, 100, 100, 0), [self.particle_size * .1, self.particle_size * .1, self.particle_size * .8, self.particle_size * .8], 1)
                self.particle_objects.append(Particle(self.screen, square_img, self.a_bounds, self.v_bounds, self.p_y_bounds, self.p_x_bounds, self.r_a_bounds, self.r_v_bounds, self.r_bounds, self.opacity_type))

            elif name == "rotated_square":
                rotated_square_img = pygame.surface.Surface((self.particle_size, self.particle_size))
                pygame.draw.rect(rotated_square_img, (100, 100, 100, 255), [self.particle_size * .1, self.particle_size * .1, self.particle_size * .8, self.particle_size * .8], 3)
                pygame.transform.rotate(rotated_square_img, 45)
                self.particle_objects.append(Particle(self.screen, rotated_square_img, self.a_bounds, self.v_bounds, self.p_y_bounds, self.p_x_bounds, self.r_a_bounds, self.r_v_bounds, self.r_bounds, self.opacity_type))
            else:
                print("Error in particle_names. Name not found")

        
    def update(self, new_time) -> None: # also draws particles
        if self.time_elapsed >= self.duration: #check is animation is over before updating
            self.animating = False
            return
        
        dt = new_time - self.time_elapsed
        self.time_elapsed = new_time - self.starting_time
        #self.time = self.current_time
        for particle in self.particle_objects:
            particle.update_info(dt)

        self.draw_particles()

    def draw_particles(self):
        for particle in self.particle_objects:
            particle.draw_particle(self.location)
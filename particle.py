import pygame
from pygame.surface import *
import math
import random

class Particle:
    def __init__(self, screen: Surface, image: Surface, a_bounds: tuple, v_bounds: tuple, p_y_bounds: tuple, p_x_bounds: tuple, r_a_bounds: tuple, r_v_bounds: tuple, r_bounds: tuple, opacity_type: str):
        self.image = image
        self.screen = screen

        """
        Notes:
            -The prefix r_ implies rotational, without it, assume translational
            -The suffix _bounds means that the tuple = (min_value, max_value)
            -The suffix _range is the difference between max_value and min_val. Used to calculate amplitude of random or standard deviation of normal distributions
            -Opacity is meant to change over time, TO BE IMPLEMENTED
        """
        #rotational transformation
        #rotational acceleration (always > 0)
        self.r_a_bounds = r_a_bounds
        self.r_a_range = r_a_bounds[1] - r_a_bounds[0]
        self.r_a = random.random() * self.r_a_range + self.r_a_bounds[0]
        #rotational velocity
        self.r_v_bounds = r_v_bounds
        self.r_v_range = r_v_bounds[1] - r_v_bounds[0]
        self.r_v = random.random() * self.r_v_range + self.r_v_bounds[0]
        #rotational position
        self.r_bounds = r_bounds
        self.r_range = r_bounds[1] - r_bounds[0]
        self.r = random.random() * self.r_range + r_bounds[0]
        #theta (determines velocity)
        self.theta = random.random() * 90 + 45
        print(self.theta)

        
        #translational acceleration (y only)
        self.a_bounds = a_bounds
        self.a_range = a_bounds[1] - a_bounds[0]
        self.a = random.random() * self.a_range + self.a_bounds[0]
        #translational velocity
        self.v_bounds = v_bounds
        self.v_range = self.v_bounds[1] - self.v_bounds[0]
        self.v = random.random() * self.v_range + self.v_bounds[0]
        self.v_x = self.v * math.cos(self.r)
        self.v_y = -self.v * math.sin(self.r)
        #translational y position
        self.y_bounds = p_y_bounds
        self.y_range = p_y_bounds[1] - p_y_bounds[0]
        self.y = random.random() * self.y_range + self.y_bounds[0]
        #translational x position
        self.x_bounds = p_x_bounds
        self.x_range = p_x_bounds[1] - p_x_bounds[0]
        self.x = random.random() * self.x_range + self.x_bounds[0]
        print(self.v_y)

        self.opacity_type = opacity_type

    def update_info(self, dt):
        #update tranformational info
        self.y += self.v_y
        self.x += self.v_x
        self.v_y -= self.a
        #print((self.a, self.v, self.x, self.y, self.r_a, self.r_v, self.r))
        #update rotation info
        old_r =  self.r
        self.r += self.r_v
        dr = self.r - old_r
        self.r_v += self.r_a
        #print((self.a, self.v, self.v_x, self.v_y, self.x, self.y))
        #update image to match rotation
        pygame.transform.rotate(self.image, dr)

    def draw_particle(self, location_i):
        self.screen.blit(self.image, (location_i[0] + self.x, location_i[1] + self.y))
import pygame
import math
import pytweening as tween
import random

class Particle:
    def __init__(self, screen: pygame.Surface, image: pygame.Surface, props):
        self.image = image
        self.screen = screen
        self.props = props
        self.a_bounds = self.props["a_bounds"]
        self.v_bounds = self.props["v_bounds"]
        self.p_y_bounds = self.props["p_y_bounds"]
        self.p_x_bounds = self.props["p_x_bounds"]
        self.r_a_bounds = self.props["r_a_bounds"]
        self.r_v_bounds = self.props["r_v_bounds"]
        self.r_bounds = self.props["r_bounds"]
        self.theta_bounds = self.props["theta_bounds"]
        self.opacity_type = self.props["opacity_type"]

        """
        Notes:
            -The prefix r_ implies rotational, without it, assume translational
            -The suffix _bounds means that the tuple = (min_value, max_value)
            -The suffix _range is the difference between max_value and min_val. Used to calculate amplitude of random or standard deviation of normal distributions
            -Opacity is meant to change over time, TO BE IMPLEMENTED
        """
        #rotational transformation
        #rotational acceleration (always > 0)
        self.r_a_bounds = self.r_a_bounds
        self.r_a_range = self.r_a_bounds[1] - self.r_a_bounds[0]
        self.r_a = random.random() * self.r_a_range + self.r_a_bounds[0]
        #rotational velocity
        self.r_v_bounds = self.r_v_bounds
        self.r_v_range = self.r_v_bounds[1] - self.r_v_bounds[0]
        self.r_v = random.random() * self.r_v_range + self.r_v_bounds[0]
        #rotational position
        self.r_bounds = self.r_bounds
        self.r_range = self.r_bounds[1] - self.r_bounds[0]
        self.r = random.random() * self.r_range + self.r_bounds[0]
        #theta (determines velocity)
        self.theta_bounds = self.theta_bounds
        self.theta_range = self.theta_bounds[1] - self.theta_bounds[0]
        self.theta = math.radians(random.random() * self.theta_range + (180 - self.theta_range) / 2)

        
        #translational acceleration (y only)
        self.a_bounds = self.a_bounds
        self.a_range = self.a_bounds[1] - self.a_bounds[0]
        self.a = random.random() * self.a_range + self.a_bounds[0]
        #translational velocity
        self.v_bounds = self.v_bounds
        self.v_range = self.v_bounds[1] - self.v_bounds[0]
        self.v = random.random() * self.v_range + self.v_bounds[0]
        self.v_x = (self.v * math.cos(self.r)) / 2
        self.v_y = -abs(-self.v * math.sin(self.r))
        #translational y position
        self.y_bounds = self.p_y_bounds
        self.y_range = self.p_y_bounds[1] - self.p_y_bounds[0]
        self.y = random.random() * self.y_range + self.y_bounds[0]
        #translational x position
        self.x_bounds = self.p_x_bounds
        self.x_range = self.p_x_bounds[1] - self.p_x_bounds[0]
        self.x = random.random() * self.x_range + self.x_bounds[0]

        self.opacity_type = self.opacity_type

    def update_info(self, dt, tween):
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
        self.rotated_image = pygame.transform.rotate(self.image, dr)

        #update opacity
        fade_factor = tween.easeInOutQuart(tween)
        self.alpha = max(0, int(255 * (1 - fade_factor)))
        self.rotated_image_with_alpha = self.rotated_image.copy()
        self.rotated_image_with_alpha.set_alpha(self.alpha)

    def draw_particle(self, location_i):
        self.screen.blit(self.rotated_image_with_alpha, (location_i[0] + self.x, location_i[1] + self.y - 5))
import pygame

from laser import Laser
from points import PointsManager
from colors import *


class Robot:
    def __init__(self, main_surf: pygame.Surface, radius: int, init_position: tuple[int, int]):
        self.surface = main_surf
        self.radius = radius
        self.position = init_position
        self.target_position = init_position

        self.laser = Laser(self.surface, WHITE, self.position, 0, 250)
        self.points = PointsManager(2)
    
    def scan360(self):
        for _ in range(360 * 4):
            point, hit = self.laser.cast()
            if hit: self.points.add(point)
            
            self.laser.rotate(0.25)
        
        self.points.parse_lines()

    def draw(self):
        for point in self.points.points:
            pygame.draw.circle(self.surface, RED, point, 3)
        
        for line in self.points.lines:
            line.draw(self.surface)
        
        pygame.draw.circle(self.surface, YELLOW, self.position, self.radius, 1)
        pygame.draw.circle(self.surface, GREY, self.position, self.laser.max_dist, 1)
    
    def check_target(self):
        if self.position == self.target_position:
            self.target_position = None
            return True

        return False

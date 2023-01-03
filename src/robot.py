import pygame

from laser import Laser
from points import PointsManager
from colors import *


class Robot:
    def __init__(self, main_surf: pygame.Surface, radius: int, init_position: tuple[int, int], scans_per_deg: int, laser_max_dist: int):
        self.surface = main_surf
        self.radius = radius
        self.position = init_position
        self.target_position = init_position
        self.scans_per_deg = scans_per_deg

        self.laser = Laser(self.surface, WHITE, self.position, 0, laser_max_dist)
        self.points = PointsManager(2)
    
    def scan360(self):
        for _ in range(360 * self.scans_per_deg):
            point, hit = self.laser.cast()
            if hit: self.points.add(point)
            
            self.laser.rotate(1 / self.scans_per_deg)
        
        self.points.make_lines()

    def draw(self):
        for point in self.points.points:
            pygame.draw.circle(self.surface, RED, point, 3)
        
        for line in self.points.lines:
            line.draw(self.surface)
        
        for p in self.points.get_single_points():
            pygame.draw.circle(self.surface, YELLOW, p, 3)
        
        pygame.draw.circle(self.surface, YELLOW, self.position, self.radius, 1)
        pygame.draw.circle(self.surface, GREY, self.position, self.laser.max_dist, 1)
    
    def check_target(self):
        if self.position == self.target_position:
            self.target_position = None
            return True

        return False

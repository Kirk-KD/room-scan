import pygame
import math

from laser import Laser
from points import PointsManager
from colors import *
from util import euclidean_distance, angle_from_two_points
from config import POINTS_MINIMUM_DISTANCE


class Robot:
    def __init__(self, main_surf: pygame.Surface, radius: int, init_position: tuple[int, int], init_rotation: int, scans_per_deg: int, laser_max_dist: int, movement_speed: int):
        self.surface = main_surf
        self.radius = radius
        self.position = init_position
        self.rotation = init_rotation
        self.target_position = init_position
        self.scans_per_deg = scans_per_deg
        self.movement_speed = movement_speed

        self.laser = Laser(self.surface, WHITE, self.position, 0, laser_max_dist)
        self.points = PointsManager(POINTS_MINIMUM_DISTANCE)
    
    def rotate(self, deg):
        self.rotation += deg
        if self.rotation >= 360:
            self.rotation -= 360
        elif self.rotation < 0:
            self.rotation = 360 + self.rotation
    
    def move(self):
        self.set_position((
            int(self.position[0] + self.movement_speed * math.cos(math.radians(self.rotation))),
            int(self.position[1] + self.movement_speed * math.sin(math.radians(self.rotation)))
        ))
    
    def scan360(self):
        for _ in range(360 * self.scans_per_deg):
            point, hit = self.laser.cast()
            if hit: self.points.add_point(point)
            
            self.laser.rotate(1 / self.scans_per_deg)
        
        self.points.make_lines()

        self.set_next_target()
    
    def set_next_target(self):
        p = self.points.closest_point_on_lines(self.position)
        d = euclidean_distance(p, self.position)
        target = (p[0] + (self.radius / d) * (self.position[0] - p[0]),
            p[1] + (self.radius / d) * (self.position[1] - p[1]))

        self.target_position = target
    
    def move_toward_target(self):
        self.rotate(angle_from_two_points(self.position, self.target_position) - self.rotation)
        self.move()
    
    def check_target(self):
        if not self.target_position:
            return True

        if euclidean_distance(self.position, self.target_position) <= self.movement_speed:
            self.position = self.target_position
            self.target_position = None

            return True

        return False

    def set_position(self, new_pos):
        self.position = int(new_pos[0]), int(new_pos[1])
        self.laser.position = int(new_pos[0]), int(new_pos[1])

    def draw(self):
        for point in self.points.points:
            pygame.draw.circle(self.surface, RED, point, 3)
        
        for line in self.points.lines:
            line.draw(self.surface)
        
        for p in self.points.get_end_points():
            pygame.draw.circle(self.surface, YELLOW, p, 3)
        
        pygame.draw.circle(self.surface, YELLOW, self.position, self.radius, 1)
        pygame.draw.circle(self.surface, GREY, self.position, self.laser.max_dist, 1)
        pygame.draw.circle(self.surface, BLUE, self.target_position, 3)

        rotation_end = (
            int(self.position[0] + 10 * math.cos(math.radians(self.rotation))),
            int(self.position[1] + 10 * math.sin(math.radians(self.rotation)))
        )
        pygame.draw.line(self.surface, YELLOW, self.position, rotation_end)

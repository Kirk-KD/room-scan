import pygame
import math

from laser import Laser
from points import PointsManager
from colors import *
from util import euclidean_distance
from config import POINTS_MINIMUM_DISTANCE


class Robot:
    def __init__(self, main_surf: pygame.Surface, radius: int, init_position: tuple[int, int], scans_per_deg: int, laser_max_dist: int, movement_speed: int):
        self.surface = main_surf
        self.radius = radius
        self.position = init_position
        self.target_position = init_position
        self.scans_per_deg = scans_per_deg
        self.movement_speed = movement_speed

        self.laser = Laser(self.surface, WHITE, self.position, 0, laser_max_dist)
        self.points = PointsManager(POINTS_MINIMUM_DISTANCE)
    
    def scan360(self):
        for _ in range(360 * self.scans_per_deg):
            point, hit = self.laser.cast()
            if hit: self.points.add_point(point)
            
            self.laser.rotate(1 / self.scans_per_deg)
        
        self.points.make_lines()

        self.set_next_target()
    
    def set_next_target(self):
        if (openings := self.points.get_opening_targets()):
            self.target_position = openings[0]
        elif (end_points := self.points.get_end_points()):
            self.target_position = end_points[0]
    
    def check_target(self):
        if not self.target_position:
            return True

        if euclidean_distance(self.position, self.target_position) <= self.movement_speed:
            self.position = self.target_position
            self.target_position = None

            return True

        return False
    
    def move_toward_target(self):
        x1, y1 = self.position
        x2, y2 = self.target_position

        # Calculate the angle between the current position and the target position
        angle = math.atan2(y2 - y1, x2 - x1)

        # Calculate the new position based on the angle and the movement speed
        x_move = self.movement_speed * math.cos(angle)
        y_move = self.movement_speed * math.sin(angle)
        new_pos = (x1 + x_move, y1 + y_move)

        self.set_position(new_pos)

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

import pygame

from util import closest_distance, closest_point, get_all_points_on_line, farthest_two_points
from colors import *


class Line:
    def __init__(self, start: tuple[int, int], end: tuple[int, int], confirmed: bool):
        self.start = start
        self.end = end
        self.confirmed = confirmed

    def draw(self, surf: pygame.Surface):

        pygame.draw.line(surf, GREEN if self.confirmed else RED, self.start, self.end, 2)
        # pygame.draw.circle(surf, BLUE, self.start, 3)
        # pygame.draw.circle(surf, BLUE, self.end, 3)
    
    def __str__(self):
        return f"<Line from {self.start} to {self.end}>"
    
    def __repr__(self):
        return self.__str__()


class PointsManager:
    def __init__(self, min_dist: int):
        self.min_dist = min_dist

        self.points = []
        self.lines = []

    def count(self):
        return len(self.points)
    
    def add(self, point: tuple[int, int]):
        if len(self.points) == 0 or closest_distance(point, self.points, include_self=True) >= self.min_dist:
            self.points.append(point)
    
    def parse_lines(self):
        points = self.points.copy()
        checked_points = set()

        for point_1 in points:
            if point_1 in checked_points:
                continue
        
            point_2 = closest_point(point_1, points)
            if point_2 in checked_points:
                continue
            
            points_on_line = get_all_points_on_line(points, point_1, point_2, self.min_dist)
            start, end = farthest_two_points(points_on_line)

            [points.remove(p) for p in points_on_line if p in points and p != start and p != end]

            checked_points.update(set(points_on_line))

            self.lines.append(Line(start, end, True))

            for line in self.lines:
                if line.start not in points or line.end not in points:
                    self.lines.remove(line)
        
        self.points = points.copy()

    def __str__(self):
        return str(self.points)

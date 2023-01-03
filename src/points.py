import pygame

from util import closest_distance, closest_point, get_all_points_on_line, farthest_two_points
from colors import *


class Line:
    def __init__(self, start: tuple[int, int], end: tuple[int, int]):
        assert start != end

        self.start = start
        self.end = end

    def draw(self, surf: pygame.Surface):
        pygame.draw.line(surf, GREEN, self.start, self.end, 2)
        pygame.draw.circle(surf, BLUE, self.start, 3)
        pygame.draw.circle(surf, BLUE, self.end, 3)
    
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
    
    def make_lines(self):
        points = self.points.copy()
        checked_points = set()

        lines = []

        for point_1 in points:
            if point_1 in checked_points:
                continue
        
            point_2 = closest_point(point_1, points)
            if point_2 in checked_points:
                continue
            
            points_on_line = get_all_points_on_line(points, point_1, point_2, self.min_dist * 1.2)
            start, end = farthest_two_points(points_on_line)

            if start == end:
                continue

            [points.remove(p) for p in points_on_line if p in points and p != start and p != end]

            checked_points.update(set(points_on_line))

            lines.append(Line(start, end))

            for line in lines:
                if line.start not in points or line.end not in points:
                    lines.remove(line)

        self.lines = lines
        self.points = points

        return lines
    
    def get_single_points(self):
        points = self.lines_to_points(keep_duplicates=True)
        return set([p for p in points if points.count(p) == 1])

    def lines_to_points(self, keep_duplicates: bool=False):
        points = []
        for line in self.lines:
            points.append(line.start)
            points.append(line.end)
        return (list if keep_duplicates else set)(points)

    def __str__(self):
        return str(self.points)

import pygame
import math

from util import closest_distance, closest_point, get_all_points_on_line, farthest_two_points, mid_point, euclidean_distance
from config import LINE_WIDTH, MAX_LINE_DEGREES_DIFF, MAX_LINE_ENDPOINT_DIFF
from colors import *


class Line:
    def __init__(self, start: tuple[int, int], end: tuple[int, int]):
        assert start != end

        self.start = start
        self.end = end

        self.slope = (float("inf") if self.start[0] == self.end[0]
            else ((self.start[1] - self.end[1]) / (self.start[0] - self.end[0])))
        self.degrees = math.degrees(math.atan(self.slope)) if self.slope != float("inf") else 90

    def draw(self, surf: pygame.Surface):
        pygame.draw.line(surf, GREEN, self.start, self.end, 2)

    def should_merge(self, other):
        return abs(other.degrees - self.degrees) <= MAX_LINE_DEGREES_DIFF and self.is_close(other)
    
    def get_merged(self, other):
        start, end = farthest_two_points(list(set([self.start, self.end, other.start, other.end])))
        return Line(start, end)
    
    def is_connected(self, other):
        return set([self.start, self.end]) == set([other.start, other.end])
    
    def is_close(self, other):
        return (euclidean_distance(self.start, other.start) <= MAX_LINE_ENDPOINT_DIFF or
            euclidean_distance(self.start, other.end) <= MAX_LINE_ENDPOINT_DIFF or
            euclidean_distance(self.end, other.start) <= MAX_LINE_ENDPOINT_DIFF or
            euclidean_distance(self.end, other.end) <= MAX_LINE_ENDPOINT_DIFF)
    
    def __str__(self):
        return f"<Line from {self.start} to {self.end}>"
    
    def __repr__(self):
        return self.__str__()


class PointsManager:
    def __init__(self, min_dist: int):
        self.min_dist = min_dist

        self.points = []
        self.lines = []

    def count_points(self):
        return len(self.points)
    
    def add_point(self, point: tuple[int, int]):
        if self.count_points() == 0 or closest_distance(point, self.points, include_self=True) >= self.min_dist:
            self.points.append(point)
    
    def make_lines(self):
        points = self.points.copy()  # make a copy to not affect original points
        checked_points = set()  # prevent duplicates, set for speed

        lines = []

        # check every unchecked point
        for point_1 in points:
            if point_1 in checked_points:
                continue
        
            # take the closest point from `point_1` in `points` to construct a line
            point_2 = closest_point(point_1, points)
            if point_2 in checked_points:
                continue
            
            points_on_line = get_all_points_on_line(points, point_1, point_2, LINE_WIDTH)

            # the two points farthest away from each other should be the line's end points
            start, end = farthest_two_points(points_on_line)
            if start == end:
                continue

            # remove all points on the line except for the two end points
            [points.remove(p) for p in points_on_line if p in points and p != start and p != end]

            # add new checked points
            checked_points.update(set(points_on_line))

            # create line
            lines.append(Line(start, end))

        for _ in range(3):  # extremely bad, will find real solution later
            lines = self.merge_lines(lines)
        self.lines = lines
    
    def merge_lines(self, lines_orig):
        lines = lines_orig.copy()
        merged_lines = []

        while lines:
            line = lines.pop()
            merged = False

            for i, merged_line in enumerate(merged_lines):
                if line.should_merge(merged_line):
                    merged_lines[i] = line.get_merged(merged_line)
                    merged = True
                    break

            if not merged:
                merged_lines.append(line)

        return merged_lines

    def get_opening_targets(self):  # TODO fix having the points in walls
        groups = self.group_lines_by_connection()
        end_points = self.get_end_points()

        pairs = set()
        checked = set()

        def is_in_diff_groups(a, b):
            for group in groups:
                points = self.lines_to_points(lines=group)
                if a in points and b in points:
                    return False
            return True

        for point in end_points:
            if point in checked:
                continue

            others_sorted = sorted(end_points, key=lambda p: euclidean_distance(p, point))[1:]
            for other in others_sorted:
                if other in checked:
                    continue

                if is_in_diff_groups(point, other):
                    pairs.add((point, other))
                    checked.add(point)
                    checked.add(other)
                    break
        
        return [mid_point(p1, p2, is_int=True) for p1, p2 in pairs]

    def get_end_points(self):
        # convert all lines into points but keep the duplicates.
        # a point is an end point if it appeared only one time.
        points = self.lines_to_points(keep_duplicates=True)
        return list(set([p for p in points if points.count(p) == 1]))

    def lines_to_points(self, lines=None, keep_duplicates: bool=False):
        points = []
        for line in (lines if lines is not None else self.lines):
            points.append(line.start)
            points.append(line.end)
        return (list if keep_duplicates else set)(points)
    
    def group_lines_by_connection(self):
        """Split lines into "islands" by whether or not they are connected."""

        groups = []
        visited = set()

        def dfs(line, group):
            visited.add(line)
            group.append(line)
            for other in self.lines:
                if line.is_connected(other) and other not in visited:
                        dfs(other, group)
        
        for line in self.lines:
            if line not in visited:
                group = []
                dfs(line, group)
                groups.append(group)
        
        return groups

    def __str__(self):
        return str(self.points)

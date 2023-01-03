import numpy as np
import math
from sklearn.cluster import DBSCAN


def euclidean_distance(p1, p2):
    p1x, p1y = p1
    p2x, p2y = p2
    return np.sqrt((p2x - p1x) ** 2 + (p2y - p1y) ** 2)


def points_in_radius(points, center, radius):
    return list(filter(lambda p: euclidean_distance(p, center) <= radius and p != center, points))


def get_dest_by_angle(start, deg, length):
    xd = length * math.cos(math.radians(deg))
    yd = length * math.sin(math.radians(deg))

    return int(start[0] + xd), int(start[1] + yd)


def mid_point(p1, p2):
    return (p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2


def raycast(surf, collision_color, start, angle, max_dist):
    """Returns x, y, hit_or_not"""

    # ChatGPT wrote this btw.

    start_x, start_y = start
    end_x, end_y = get_dest_by_angle(start, angle, max_dist) if type(angle) is not tuple else angle

    dx = abs(end_x - start_x)
    dy = abs(end_y - start_y)

    sx = 1 if start_x < end_x else -1
    sy = 1 if start_y < end_y else -1

    err = 0

    if dx > dy:
        err = dx / 2
        while start_x != end_x and start_x < surf.get_width():
            try:
                if surf.get_at((start_x, start_y)) == collision_color:
                    return (start_x, start_y), True
            except IndexError: return (start_x, start_y), False
            
            err -= dy

            if err < 0:
                start_y += sy
                err += dx
            
            start_x += sx
        
        return (start_x, start_y), False
    else:
        err = dy / 2
        while start_y != end_y and start_y < surf.get_height():
            try:
                if surf.get_at((start_x, start_y)) == collision_color:
                    return (start_x, start_y), True
            except IndexError: return (start_x, start_y), False
            
            err -= dx

            if err < 0:
                start_x += sx
                err += dy
            
            start_y += sy
        
        return (start_x, start_y), False


def closest_distance(point: tuple[int, int], points: list[tuple[int, int]], include_self=False):
    return euclidean_distance(point, closest_point(point, points, include_self))


def closest_point(point, points, include_self=False):
    if include_self and point in points:
        return point

    return sorted(points, key=lambda p: euclidean_distance(p, point))[int(not include_self)]


def farthest_two_points(points):
    if len(points) < 2:
        return None

    two_points = None, None
    dist = 0

    for i, p1 in enumerate(points):
        for j in range(i + 1, len(points)):
            p2 = points[j]

            if (distance := euclidean_distance(p1, p2)) >= dist:
                dist = distance
                two_points = p1, p2
    
    return two_points


def get_all_points_on_line(points, p1, p2, width):
    on_line = []

    x1, y1 = p1
    x2, y2 = p2

    if x1 == x2:  # vertical
        on_line = [(x, y) for x, y in points if abs(x - x1) <= width]
    elif y1 == y2:  # horizontal
        on_line = [(x, y) for x, y in points if abs(y - y1) <= width]
    else:
        slope = (y1 - y2) / (x1 - x2)
        y_int = y1 - slope * x1

        for x, y in points:
            dist_to_line = abs(slope * x - y + y_int) / math.sqrt(slope ** 2 + 1)
            if dist_to_line <= width:
                on_line.append((x, y))
    
    clusters = points_to_clusters(on_line, 30)
    for cluster in clusters:
        if p1 in cluster or p2 in cluster:
            return list(set(cluster))

    raise Exception("Somehow p1 or p2 was deleted?")


def points_to_clusters(points, max_distance):
    points_array = np.array(points)
    clusters = DBSCAN(eps=max_distance).fit(points_array).labels_

    cluster_list = []
    for cluster_label in np.unique(clusters):
        # Get the indices of the points that belong to the current cluster
        indices = np.where(clusters == cluster_label)[0]
        # Get the points that belong to the current cluster
        points_in_cluster = points_array[indices]
        # Append the points to the list of clusters
        cluster_list.append([tuple(p) for p in points_in_cluster.tolist()])

    return cluster_list


def find_point_on_circumference(center, radius, pass_through):
    """Find a point on the circumference that, when a line is drawn from `center` to the point, it passes through `pass_through`."""

    angle = math.atan2(pass_through[1] - center[1], pass_through[0] - center[0])

    x = center[0] + radius * math.cos(angle)
    y = center[1] + radius * math.sin(angle)

    return x, y

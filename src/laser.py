from util import raycast


class Laser:
    def __init__(self, surface, collision_color, init_pos, init_deg, max_dist):
        self.surface = surface
        self.collision_color = collision_color
        self.position = init_pos
        self.degrees = init_deg
        self.max_dist = max_dist

    def cast(self):
        return raycast(self.surface, self.collision_color, self.position, self.degrees, self.max_dist)
    
    def set_positon(self, pos):
        self.position = pos

    def rotate(self, deg):
        self.degrees += deg

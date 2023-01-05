import pygame

from robot import Robot
from colors import *
from config import LASER_RANGE, ROBOT_INIT_POSITION, ROBOT_RADIUS, ROBOT_SPEED, SCANS_PER_DEGREE, WINDOW_SIZE, FPS


class Simulation:
    def __init__(self, room_number: int):
        self.running = True
        self.clock = pygame.time.Clock()

        self.main_surf = pygame.display.set_mode(WINDOW_SIZE)
        self.room_surf = pygame.image.load(f"rooms/{room_number}.png")

        self.robot = Robot(self.main_surf, ROBOT_RADIUS, ROBOT_INIT_POSITION, SCANS_PER_DEGREE, LASER_RANGE, ROBOT_SPEED)
    
    def main(self):
        if self.robot.check_target():
            self.robot.scan360()
        else:
            self.robot.move_toward_target()

        self.robot.draw()

        points = self.robot.points.get_opening_targets()
        for point in points:
            pygame.draw.circle(self.main_surf, GREEN, point, 3)
        
        for point in self.robot.points.lines_to_points():
            pygame.draw.circle(self.main_surf, BLUE, point, 3)

    def pull_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
    
    def fill(self):
        self.main_surf.fill(BLACK)
    
    def run(self):
        while self.running:
            self.pull_events()
            self.clock.tick(FPS)

            self.fill()
            self.main_surf.blit(self.room_surf, (0, 0))

            self.main()

            pygame.display.update()

import pygame

from robot import Robot
from colors import *


class Simulation:
    def __init__(self, room_number: int):
        self.FPS                        = 60
        self.ROBOT_RADIUS               = 10
        self.LASER_RANGE                = 150
        self.POINTS_MINIMUM_DISTANCE    = 1
        self.WINDOW_SIZE                = 700, 700
        self.SCANS_PER_DEGREE           = 4

        self.running = True
        self.clock = pygame.time.Clock()

        self.main_surf = pygame.display.set_mode(self.WINDOW_SIZE)
        self.room_surf = pygame.image.load(f"rooms/{room_number}.png")

        self.robot = Robot(self.main_surf, self.ROBOT_RADIUS, (350, 350), self.SCANS_PER_DEGREE, self.LASER_RANGE)
    
    def main(self):
        if self.robot.check_target():
            self.robot.scan360()
            self.robot.points.add(self.robot.position)

        self.robot.draw()

    def pull_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
    
    def fill(self):
        self.main_surf.fill(BLACK)
    
    def run(self):
        while self.running:
            self.pull_events()
            self.clock.tick(self.FPS)

            self.fill()
            self.main_surf.blit(self.room_surf, (0, 0))

            self.main()

            pygame.display.update()

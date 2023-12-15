import pygame
import numpy as np

def create_square(pos, r):
    return np.array([pos + r * np.array([np.cos(angle), np.sin(angle)]) for angle in map(np.deg2rad, [45, 135, 225, 315])], dtype=int)


def vector_angle(vector: np.ndarray) -> float:
    angle = np.rad2deg(np.arctan(vector[1] / vector[0]))
    if vector[0] < 0 and vector[1] < 0:
        return angle + 180
    elif vector[0] < 0:
        return 90 - angle
    elif vector[1] < 0:
        return 270 - angle
    return angle

class Object:
    def __init__(self, points, width=1, color=(0, 255, 0)):
        self.points = points.astype(np.float64)
        self.width = width
        self.color = color
        self.speed = np.array([0.0, 0.0])
        self.target = 0
        self.active = True


    def set_width(self, width):
        self.width = width

    def simulate(self, dt):
        self.points += self.speed * dt
    
    def get_middle_point(self):
        return self.points.mean(axis=0)
    
    def get_speed(self):
        return self.speed

    def set_color(self, color):
        self.color = color

    def set_speed(self, new_speed):
        if type(new_speed) != np.ndarray:
            self.speed = np.array(new_speed)
        else:
            self.speed = np.array(new_speed)
    
    def draw(self, screen):
        pygame.draw.polygon(surface=screen, color=self.color, points=self.points, width=self.width)


        
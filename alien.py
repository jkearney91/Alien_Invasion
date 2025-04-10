import pygame

class Alien:

    """A class to manage the Aliens"""

    def __init__(self, color, speed, points):
        self.color = color
        self.speed = speed
        self.points = points

    def __repr__(self):
        return f"Alien(color='{self.color}', speed='{self.speed}', points={self.points})"
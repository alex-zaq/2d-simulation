from random import random

from .entity import Entity


class Creature(Entity):
    def get_closest_random_coords(self, map):
        max_x, max_y = max(map.keys())
        new_x = max(0, min(self.x + random.randint(-1, 1), max_x))
        new_y = max(0, min(self.y + random.randint(-1, 1), max_y))
        return new_x, new_y

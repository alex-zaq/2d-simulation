import random

from .entities import Grass, Herbivore, Predator, Rock
from .map import Map


class Coord_generator:
    def __init__(self, x_count, y_count):
        self.x_count = x_count
        self.y_count = y_count
        self.coords = set()

    def get_non_rpt_coords_srs(self, coord_count):
        loc_coords = set()
        while len(loc_coords) < coord_count:
            coords = (
                random.randint(0, self.x_count - 1),
                random.randint(0, self.y_count - 1),
            )
            loc_coords.add(coords)
            self.coords.add(coords)
        return loc_coords

    def reset(self):
        self.coords = set()


class Spawner:
    def __init__(self, config):
        self.config = config

    def generate_map(self):
        predators_count = self.config.predators_start_count
        herbivore_count = self.config.herbivores_start_count
        grass_count = self.config.grass_count
        rock_count = self.config.rock_count

        x_count, y_count = self.config.map_size

        coord_generator = Coord_generator(x_count, y_count)
        rock_coords = coord_generator.get_non_rpt_coords_srs(rock_count)
        grass_coords = coord_generator.get_non_rpt_coords_srs(grass_count)
        predator_coords = coord_generator.get_non_rpt_coords_srs(predators_count)
        herbivore_coords = coord_generator.get_non_rpt_coords_srs(herbivore_count)

        map_data = {}

        for x, y in rock_coords:
            map_data[(x, y)] = Rock(x, y)

        for x, y in grass_coords:
            map_data[(x, y)] = Grass(x, y)

        for x, y in predator_coords:
            map_data[(x, y)] = Predator(x, y)

        for x, y in herbivore_coords:
            map_data[(x, y)] = Herbivore(x, y)

        game_map = Map(map_data, self.config)

        return game_map

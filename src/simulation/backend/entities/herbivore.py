from .creature import Creature
from .grass import Grass
from .ground import Ground


class Herbivore(Creature):
    energy = 0

    def move(self, map):
        search_algoritm = self.__class__.search_algoritm
        path_to_grass = search_algoritm.search(map, self, Grass)

        new_coords = path_to_grass[0]

        if len(path_to_grass) == 1:
            self.energy += 1
        elif len(path_to_grass) == 0:
            new_coords = self.get_closest_random_coords(map)

        old_x, old_y = self.x, self.y
        self.x, self.y = new_coords[0]
        map[(old_x, old_y)] = Ground(old_x, old_y)

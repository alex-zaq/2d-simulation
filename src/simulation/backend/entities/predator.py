from .entity import Creature
from .ground import Ground
from .herbivore import Herbivore


class Predator(Creature):
    energy = 0

    def move(self, map):
        search_algoritm = self.__class__.search_algoritm
        path_to_herbivore = search_algoritm.search(map, self, Herbivore)

        new_coords = path_to_herbivore[0]

        if len(path_to_herbivore) == 1:
            self.energy += 1
        elif len(path_to_herbivore) == 0:
            new_coords = self.get_closest_random_coords(map)

        old_x, old_y = self.x, self.y
        self.x, self.y = new_coords
        map[(old_x, old_y)] = Ground(old_x, old_y)

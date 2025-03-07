from copy import deepcopy

from ..behavior_algoritms import Creature_status
from .entity import Entity
from .objects import Grass


class Creature(Entity):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.energy = 0

    def get_energy_label(self):
        return str(self.energy)


class Herbivore(Creature):
    def move(self, game_map):
        search_alg = self.__class__.search_algoritm
        escaping_alg = self.__class__.escaping_algoritm
        breeding_alg = self.__class__.breeding_algoritm

        if escaping_coords := escaping_alg.search(game_map, self, Predator):
            old_x, old_y = self.x, self.y
            new_x, new_y = escaping_coords
            self.x, self.y = new_x, new_y
            game_map.map.pop((old_x, old_y))
            game_map.map[(new_x, new_y)] = self
            self.wait_move = False
            return

        if self.energy >= 3 and (
            breeding_coords := breeding_alg.free_coords(game_map, self)
        ):
            new_x, new_y = breeding_coords
            self.energy = 0
            self.wait_move = False
            new_herbivore = deepcopy(self)
            new_herbivore.x, new_herbivore.y = new_x, new_y
            game_map.map[(new_x, new_y)] = new_herbivore
            return

        new_coords, status = search_alg.search(game_map, self, Grass)

        if not new_coords:
            return

        if status == Creature_status.EATING:
            self.energy += 1
            game_map.add_target_to_random_free_cell(Grass)

        old_x, old_y = self.x, self.y
        new_x, new_y = new_coords

        self.x, self.y = new_x, new_y
        game_map.map.pop((old_x, old_y))
        game_map.map[(new_x, new_y)] = self
        self.wait_move = False


class Predator(Creature):
    def move(self, game_map):
        search_algoritm = self.__class__.search_algoritm
        breeding_algoritm = self.__class__.breeding_algoritm

        if self.energy >= 3 and (
            breeding_coords := breeding_algoritm.free_coords(game_map, self)
        ):
            new_x, new_y = breeding_coords
            self.energy = 0
            self.wait_move = False
            new_predator = deepcopy(self)
            new_predator.x, new_predator.y = new_x, new_y
            game_map.map[(new_x, new_y)] = new_predator
            return

        new_coords, status = search_algoritm.search(game_map, self, Herbivore)

        if not new_coords:
            return

        if status == Creature_status.EATING:
            self.energy += 1

        old_x, old_y = self.x, self.y
        new_x, new_y = new_coords

        self.x, self.y = new_x, new_y
        game_map.map.pop((old_x, old_y))
        game_map.map[(new_x, new_y)] = self
        self.wait_move = False

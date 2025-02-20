from dataclasses import dataclass

from .entities.predator import Herbivore, Predator
from .search_algoritms import BFS


@dataclass
class BackendState:
    pass


class Backend:
    def __init__(self, config):
        self.config = config
        self.history = []

    def map_init(self):
        self._set_search_stategy()
        x_count, y_count = self.config.map_size
        self.map = {
            (x, y): self.spawner.spawn(x, y)
            for x in range(x_count)
            for y in range(y_count)
        }

    def set_spawner(self, spawner):
        self.spawner = spawner

    def _set_search_stategy(self):
        self.set_search_algorithm(
            Predator, self.get_search_algorithm(self.config.predator_search_strategy)
        )
        self.set_search_algorithm(
            Herbivore, self.get_search_algorithm(self.config.predator_search_strategy)
        )

    def get_search_algorithm(self, name):
        match name:
            case "BFS":
                return BFS
            case "A*":
                raise NotImplementedError

    def set_search_algorithm(self, entity, search_algoritm):
        entity.search_algoritm = search_algoritm

    def do_move(self):
        entities = list(self.map.values())
        for entity in entities:
            entity.move(map)

    def next_step(self):
        self.history.append(self.map)
        self.do_move()

    def previous_step(self):
        self.map = self.history.pop()
        self.do_move()

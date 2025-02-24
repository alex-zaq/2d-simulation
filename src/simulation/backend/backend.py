from .entities import Herbivore, Predator
from .search_algoritms import BFS
from .spawner import Spawner


class Backend:
    def __init__(self, config):
        self.config = config
        self.set_spawner(Spawner(config))
        self.history = []

    def map_init(self):
        self._set_search_stategy()
        self.map = self.spawner.generate_map()
        
    def get_map(self):
        return self.map
        

    def set_spawner(self, spawner):
        self.spawner = spawner

    def _set_search_stategy(self):
        self.set_search_algorithm(
            Predator, self.get_search_alg(self.config.predator_search_algoritm)
        )
        self.set_search_algorithm(
            Herbivore, self.get_search_alg(self.config.herbivore_search_algoritm)
        )

    def get_search_alg(self, name):
        match name:
            case "BFS":
                return BFS
            case "A*":
                raise NotImplementedError

    def set_search_algorithm(self, entity_cls, search_algoritm):
        entity_cls.search_algoritm = search_algoritm

    def do_move(self):
        entities = list(self.map.values())
        for entity in entities:
            entity.move(self.map)

    def next_step(self):
        self.history.append(self.map)
        self.do_move()

    def previous_step(self):
        self.map = self.history.pop()
        self.do_move()

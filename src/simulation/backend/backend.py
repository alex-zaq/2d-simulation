from copy import deepcopy

from .behavior_algoritms import (
    BFS,
    BreedingAlgoritm,
    BreedingAlgoritmBase,
    EscapingAlgoritm,
    EscapingAlgoritmBase,
)
from .entities import Herbivore, Predator
from .spawner import Spawner


class Backend:
    def __init__(self, config):
        self.config = config
        self._set_spawner(Spawner(config))
        self._set_behavior_algoritms()
        
        self.history = []

    def generate_map(self):
        self.game_map = self.spawner.generate_map()
        self.history.append(deepcopy(self.game_map))

    def get_map(self):
        return self.game_map.map

    def next_step(self):
        self.history.append(deepcopy(self.game_map))
        self._do_move()

    def previous_step(self):
        if self.history:
            self.game_map = self.history.pop()

        
    def _set_spawner(self, spawner):
        self.spawner = spawner


    def _set_behavior_algoritms(self):
        self._set_search_stategy()
        self._set_escaping_strategy()
        self._set_breeding_strategy()


    def _set_search_stategy(self):
        self._set_algoritm("search_algoritm", Predator, self._get_search_alg(self.config.predator_search_algoritm))
        self._set_algoritm("search_algoritm", Herbivore, self._get_search_alg(self.config.herbivore_search_algoritm))
        
    def _set_escaping_strategy(self):
        self._set_algoritm("escaping_algoritm", Herbivore, self.get_escaping_alg(self.config.herbivore_escaping))
                
    def _set_breeding_strategy(self):
        self._set_algoritm("breeding_algoritm", Herbivore, self.get_breeding_alg(self.config.herbivore_breeding))
        self._set_algoritm("breeding_algoritm", Predator, self.get_breeding_alg(self.config.predator_breeding))
    
        
    def _get_search_alg(self, name):
        match name:
            case "bfs":
                return BFS
            case "A*":
                raise NotImplementedError
            
            
    def get_escaping_alg(self, name):
        if name:
            return EscapingAlgoritm
        else:
            return EscapingAlgoritmBase

    def get_breeding_alg(self, name):
        if name:
            return BreedingAlgoritm
        else:
            return BreedingAlgoritmBase
        

    def _set_algoritm(self, aatr, entity_cls, algoritm):
        if algoritm:
            setattr(entity_cls, aatr, algoritm)

    def _do_move(self):
        coords_lst = list(self.game_map.map)
        self._reset_move_status()
        for coords in coords_lst:
            if coords in self.game_map.map and self.game_map.map[coords].wait_move:
                self.game_map.map[coords].move(self.game_map)

    def _reset_move_status(self):
        for coords in self.game_map.map:
            self.game_map.map[coords].wait_move = True




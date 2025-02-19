from dataclasses import dataclass


@dataclass
class BackendState:
    ...

class Backend:
    def __init__(self, config):
        self.config = config

    def init(self):
        self.map_init()
        self.spawn_entites()


    def map_init(self): ...

    def spawn_entites(self): ...

    def next_step(self): ...
    
    def previous_step(self): ...
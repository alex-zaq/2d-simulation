from ..search_algoritms import Search
from .entity import Entity


class Creature(Entity):
    
    def __init__(self, x, y):
        super().__init__(x, y)
        
    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def search(
        self,
        map: dict,
        entity: Entity,
        target: Entity,
        search_algorithm: Search
    ): ...

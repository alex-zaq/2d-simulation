from abc import ABC, abstractmethod

from ..entities import Entity


class search(ABC):
    @abstractmethod
    def search(self, map: dict, entity: Entity, target: Entity): ...


class BFS(search):
    def search(self, map: dict, entity: Entity, target: Entity) -> list[(int, int)]: ...

from abc import ABC, abstractmethod

from ..entities import Entity


class Search(ABC):
    @abstractmethod
    def search(self, map: dict, entity: Entity, target: Entity): ...


class BFS(Search):
    def search(self, map: dict, entity: Entity, target: Entity) -> list[(int, int)]: ...

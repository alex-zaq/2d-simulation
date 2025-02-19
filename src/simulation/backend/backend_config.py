

from dataclasses import dataclass


@dataclass
class Backend_config:
    map_size: float
    creatures_count: int
    predators_ratio: float
    grass_count: int
    rock_count: int
    search_algoritm: "str"
    breeding: bool

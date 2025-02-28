

from dataclasses import dataclass


@dataclass
class Backend_config:
    map_size: tuple[int, int]
    herbivores_start_count: int
    predators_start_count: float
    grass_count: int 
    rock_count: int
    predator_search_algoritm: str
    herbivore_search_algoritm: str 
    predator_breeding: bool
    herbivore_breeding: bool
    herbivore_escaping: bool 
    herbivore_escaping_radius: int
    herbivore_through_wall: bool
    predator_through_wall: bool

from dataclasses import dataclass


@dataclass
class Gui_config:
    resolution:tuple[int, int]
    rock_pict: str
    predator_pict: str
    herbivore_pict: str
    grass_pict: str

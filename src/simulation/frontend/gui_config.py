from dataclasses import dataclass


@dataclass
class Gui_config:
    rock_pict: str
    predator_pict: str
    herbivore_pict: str
    ground_pict: str
    grass_pict: str
    grid_color: str
    delay_ms: int
    cell_size: int


@dataclass
class Console_config:
    rock_symbol: str
    predator_symbol: str
    herbivore_symbol: str
    ground_symbol: str
    grass_symbol: str
    border_symbol: str

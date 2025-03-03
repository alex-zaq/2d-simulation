from .interface import FrontendBase


class ConsoleFrontend(FrontendBase):
    def __init__(self, console_config):
        self.console_config = console_config

    def init(self):
        self.game_map = self.backend.generate_map()
        self.input_msg = (
            "( reset: generate new map,   n: next step,   p: previous step,   e: exit )"
        )
        self.ground_symbol = self.console_config.ground_symbol
        self.grass_symbol = self.console_config.grass_symbol
        self.rock_symbol = self.console_config.rock_symbol
        self.predator_symbol = self.console_config.predator_symbol
        self.herbivore_symbol = self.console_config.herbivore_symbol

    def run(self):
        # self._clear_screen()
        while (command := input(self.input_msg)) != "e":
            match command:
                case "n":
                    self.backend.next_step()
                    self.game_map = self.backend.get_map()
                    self._draw_map()
                case "p":
                    self.backend.previous_step()
                    if self.game_map is not None:
                        self.game_map = self.backend.get_map()
                        self._draw_map()
                case "reset":
                    self.backend.generate_map()
                    self.game_map = self.backend.get_map()
                    self._draw_map()
                case _:
                    print("Unknown command")

    def use_backend(self, backend):
        self.backend = backend

    def _get_cell_symbol(self, obj):
        if obj is None:
            return self.ground_symbol

        match type(obj).__name__:
            case "Grass":
                return self.grass_symbol
            case "Rock":
                return self.rock_symbol
            case "Herbivore":
                return self.herbivore_symbol
            case "Predator":
                return self.predator_symbol

    def _clear_screen(self):
        print("\033[H\033[J", end="")
        # os.system('cls')

    def _draw_map(self):
        x_max, y_max = self.backend.config.map_size

        # self._clear_screen()

        border = "+" + "-" * (x_max * 2 + 1) + "+"
        print(border)

        res = []
        for y in range(y_max):
            row_cells = [
                self._get_cell_symbol(self.game_map.get_entity_by_coords((x, y)))
                for x in range(x_max)
            ]
            res.append("| " + " ".join(row_cells) + " |")

        map_res = "\n".join(res)

        print(map_res)

        print(border)

        info_lines = [f"Шаг симуляции: {self.backend.step}"]
        print("\n".join(info_lines))

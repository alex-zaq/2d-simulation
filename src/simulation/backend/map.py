import random


class Map:
    def __init__(self, game_map, config):
        self.map = game_map
        self.config = config
        self.cells = set(
            (x, y)
            for x in range(self.config.map_size[0])
            for y in range(self.config.map_size[1])
        )

    def add_target_to_random_free_cell(self, target_cl):
        all_cells = self.cells
        occupied_cells = set(self.map.keys())
        free_cells = all_cells - occupied_cells
        if not free_cells:
            return None
        coords = random.choice(list(free_cells))
        self.map[coords] = target_cl(coords[0], coords[1])
        return coords

    def get_neighbors(self, coords, entity, target_cls):
        match type(entity).__name__:
            case "Predator":
                return self._get_neighbors(
                    coords, target_cls, self.config.predator_through_wall
                )
            case "Herbivore":
                return self._get_neighbors(
                    coords, target_cls, self.config.herbivore_through_wall
                )

    def get_free_cell_for_breeding(self, entity):
        match type(entity).__name__:
            case "Predator":
                if not self.config.predator_breeding:
                    return None
                coords = self.get_closest_coords_by_radius(
                    entity.get_coords(),
                    radius=1,
                    valid_coords=True,
                    through_walls=self.config.predator_through_wall,
                )
                if not coords:
                    return None
                return random.choice(coords)
            case "Herbivore":
                if not self.config.herbivore_breeding:
                    return None
                coords = self.get_closest_coords_by_radius(
                    entity.get_coords(),
                    radius=1,
                    valid_coords=True,
                    through_walls=self.config.herbivore_through_wall,
                )
                if not coords:
                    return None
                return random.choice(coords)

    def is_target(self, coords, target_cls):
        if coords not in self.map:
            return False
        return isinstance(self.map[coords], target_cls)

    def get_closest_random_valid_coords(self, coords, entity, target_cls):
        coords = self.get_neighbors(coords, entity, target_cls)
        if coords:
            return random.choice(coords)
        else:
            return coords

    def get_closest_coords_by_radius(
        self, coord, radius, valid_coords=False, through_walls=False
    ):
        max_x, max_y = self.config.map_size
        if not through_walls:
            max_x, max_y = max_x - 1, max_y - 1
        x, y = coord
        closest_coords = []
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                if through_walls:
                    nx, ny = (x + dx) % max_x, (y + dy) % max_y
                else:
                    nx, ny = x + dx, y + dy
                if nx < 0 or ny < 0 or nx > max_x or ny > max_y:
                    continue
                if not valid_coords:
                    closest_coords.append((nx, ny))
                else:
                    if (nx, ny) not in self.map:
                        closest_coords.append((nx, ny))
        return closest_coords

    def get_escaping_coords_from_target(self, coord, target_cls):
        radius = self.config.herbivore_escaping_radius
        through_walls = self.config.herbivore_through_wall

        coords_for_scanning = self.get_closest_coords_by_radius(
            coord, radius, valid_coords=False, through_walls=through_walls
        )
        coords_with_target = [
            coords
            for coords in coords_for_scanning
            if self.is_target(coords, target_cls)
        ]

        if not coords_with_target:
            return None

        target_coords = coords_with_target[0]
        valid_coords_for_step = self.get_closest_coords_by_radius(
            coord, radius=1, valid_coords=True, through_walls=through_walls
        )

        if not valid_coords_for_step:
            return None

        px, py = target_coords
        best_coord = max(
            valid_coords_for_step, key=lambda v: (v[0] - px) ** 2 + (v[1] - py) ** 2
        )
        return best_coord

    def get_entity_by_coords(self, coords):
        if coords in self.map:
            return self.map[coords]
        else:
            return None

    def distance_through_walls(self, start, goal):
        x_max, y_max = self.config.map_size
        dx = min(abs(start[0] - goal[0]), x_max - abs(start[0] - goal[0]))
        dy = min(abs(start[1] - goal[1]), y_max - abs(start[1] - goal[1]))
        return (dx**2 + dy**2) ** 0.5

    def distance(self, start, goal):
        return ((start[0] - goal[0]) ** 2 + (start[1] - goal[1])) ** 0.5

    def get_closest_target_by_coords(self, coords, target_cls):
        res = [target for target in self.map.values() if isinstance(target, target_cls)]

        if not res:
            return None

        x_max, y_max = self.config.map_size
        x, y = coords

        def wrapped_distance(target):
            dx = min(abs(target.x - x), x_max - abs(target.x - x))
            dy = min(abs(target.y - y), y_max - abs(target.y - y))
            return dx**2 + dy**2

        target = min(res, key=wrapped_distance)

        return target

    def _get_neighbors(self, coords, target_cls, through_walls=False):
        max_x, max_y = self.config.map_size
        if not through_walls:
            max_x, max_y = max_x - 1, max_y - 1
        x, y = coords
        neighbors = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                if through_walls:
                    nx, ny = (x + dx) % max_x, (y + dy) % max_y
                else:
                    nx, ny = x + dx, y + dy
                if nx < 0 or ny < 0 or nx > max_x or ny > max_y:
                    continue
                if self.is_target((nx, ny), target_cls):
                    neighbors.append((nx, ny))
                if (nx, ny) not in self.map:
                    neighbors.append((nx, ny))
        return neighbors

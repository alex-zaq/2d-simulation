



import random


class Map:
        
    def __init__(self, game_map, config):
        self.map = game_map
        self.config = config
        
        
    def get_neighbors(self, coords, entity_cls, target_cls):
    # def get_neighbors(self, coords, target_cls):
        match type(entity_cls).__name__:
        # match entity_cls.__name__:
            case "Predator":
                if self.config.predator_through_wall:
                    return self._get_neighbors_through_walls(coords, target_cls)
                else:
                    return self._get_neighbors(coords, target_cls)
            case "Herbivore":
                if self.config.herbivore_through_wall:
                    return self._get_neighbors_through_walls(coords, target_cls)
                else:
                    return self._get_neighbors(coords, target_cls)
        
        
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
        
        
    def get_closest_coords_by_radius(self, coord, radius):
        max_x, max_y = self.config.map_size
        max_x, max_y = max_x - 1, max_y - 1
        x, y = coord
        closest_coords = []
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                nx, ny = x + dx, y + dy
                if nx < 0 or ny < 0 or nx > max_x or ny > max_y:
                    continue
                closest_coords.append((nx, ny))
        return closest_coords
    
    
    def get_escaping_coords_from_target(self, coord, target_cls):
        radius = self.config.herbivore_escaping_radius
        coords_lst = self.get_closest_coords_by_radius(coord, radius)
        res = [coords for coords in coords_lst if self.is_target(coords, target_cls)]
        
        if res:
            x_predator, y_predator = res[0]
            x_herbivore, y_herbivore = coord
            dx, dy = x_predator - x_herbivore, y_predator - y_herbivore
            return (x_herbivore - dx, y_herbivore - dy)

        return None
    
        
    def _get_neighbors(self, coords, target_cls):
        max_x, max_y = self.config.map_size
        max_x, max_y = max_x - 1, max_y - 1
        x, y = coords
        neighbors = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if nx < 0 or ny < 0 or nx > max_x or ny > max_y:
                    continue
                if self.is_target((nx, ny), target_cls):
                    neighbors.append((nx, ny))
                if (nx, ny) not in self.map:
                    neighbors.append((nx, ny))
        return neighbors
    
    def _get_neighbors_through_walls(self, coords, target_cls):
        max_x, max_y = self.config.map_size
        x, y = coords
        neighbors = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = (x + dx) % max_x, (y + dy) % max_y
                if self.is_target((nx, ny), target_cls):
                    neighbors.append((nx, ny))
                if (nx, ny) not in self.map:
                    neighbors.append((nx, ny))
        return neighbors
    

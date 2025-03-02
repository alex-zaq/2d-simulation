from collections import deque
from enum import Enum, auto


class Creature_status(Enum):
    SEARCHING = auto()
    EATING = auto()
    BREADING = auto()
    WANDERING = auto()


class Search_result:
    def __init__(self, new_coords, status):
        self.path = new_coords
        self.status = status

    def __iter__(self):
        return iter([self.path, self.status])


class Search_base:
    @classmethod
    def _path_processor(cls, entity, path, game_map, target_cls):
        if path:
            if len(path) == 2:
                return Search_result(path[1], Creature_status.EATING)
            return Search_result(path[1], Creature_status.SEARCHING)
        else:
            random_coords = game_map.get_closest_random_valid_coords(
                (entity.x, entity.y), entity, target_cls
            )
            return Search_result(random_coords, Creature_status.WANDERING)


class BFS(Search_base):
    @classmethod
    def search(cls, game_map, entity, target_cls):
        parents = {}
        visited = set()
        path = []

        queue = deque([entity.get_coords()])
        visited.add(entity.get_coords())

        while queue:
            curr_coords = queue.popleft()

            if game_map.is_target(curr_coords, target_cls):
                finish_coords = curr_coords
                while curr_coords in parents:
                    curr_coords = parents[curr_coords]
                    path.append(curr_coords)
                path = path[::-1]
                path.append(finish_coords)
                return cls._path_processor(entity, path, game_map, target_cls)

            neighbors = game_map.get_neighbors(curr_coords, entity, target_cls)

            for neighbor in neighbors:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
                    parents[neighbor] = curr_coords

        return cls._path_processor(entity, path, game_map, target_cls)


class A_star(Search_base):
    @classmethod
    def search(cls, game_map, entity, target):
        pass

    # @classmethod
    # def _path_processor(cls, entity, path, game_map, target_cls):
    #     if path:
    #         if len(path) == 2:
    #             return cls.Search_result(path[1], Creature_status.EATING)
    #         return cls.Search_result(path[1], Creature_status.SEARCHING)
    #     else:
    #         random_coords = cls._get_closest_random_valid_coords((entity.x, entity.y), game_map, target_cls)
    #         return cls.Search_result(random_coords, Creature_status.WANDERING)

    # @classmethod
    # def _get_neighbors(cls, game_map, x_y_coords, target_cls):
    #     max_x, max_y = game_map.config.map_size
    #     max_x -= 1
    #     max_y -= 1
    #     x, y = x_y_coords
    #     neighbors = []
    #     for dx in [-1, 0, 1]:
    #         for dy in [-1, 0, 1]:
    #             if dx == 0 and dy == 0:
    #                 continue
    #             nx, ny = x + dx, y + dy
    #             if nx < 0 or ny < 0 or nx > max_x or ny > max_y:
    #                 continue
    #             if cls._is_target(game_map, (nx, ny), target_cls):
    #                 neighbors.append((nx, ny))
    #             if (nx, ny) not in game_map.map:
    #                 neighbors.append((nx, ny))
    #     return neighbors

    # @classmethod
    # def _is_target(cls, game_map, check_x_y_coords, target_cls):
    #     if check_x_y_coords not in game_map.map:
    #         return False
    #     return isinstance(game_map.map[check_x_y_coords], target_cls)

    # @classmethod
    # def _get_closest_random_valid_coords(cls, coord_pair, game_map, target_cls):
    #     coords = cls._get_neighbors(game_map, coord_pair, target_cls)
    #     if coords:
    #         return random.choice(coords)
    #     else:
    #         return coord_pair

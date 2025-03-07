import heapq
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
            return cls._get_random_move_results(game_map, entity, target_cls)

    @classmethod
    def _get_random_move_results(cls, game_map, entity, target_cls):
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
    class Node:
        def __init__(self, coords, g=0, h=0):
            self.coords = coords
            self.g = g
            self.h = h

        def __lt__(self, other):
            return self.g + self.h < other.g + other.h

        def __eq__(self, other):
            return self.coords == other.coords

    @classmethod
    def get_heuristic_func(cls, game_map, entity):
        match type(entity).__name__:
            case "Predator":
                if game_map.config.predator_through_wall:
                    return game_map.distance_through_walls
                else:
                    return game_map.distance
            case "Herbivore":
                if game_map.config.herbivore_through_wall:
                    return game_map.distance_through_walls
                else:
                    return game_map.distance

    @classmethod
    def search(cls, game_map, entity, target_cls):
        x, y = entity.get_coords()
        goal = game_map.get_closest_target_by_coords((x, y), target_cls)

        if goal is None:
            return cls._get_random_move_results(game_map, entity, target_cls)

        goal_coords = goal.get_coords()

        open_list = []
        closed_set = set()
        parents = {}
        heuristic_func = cls.get_heuristic_func(game_map, entity)
        path = []

        heapq.heappush(open_list, cls.Node((x, y)))

        while open_list:
            current_node = heapq.heappop(open_list)
            curr_coords = current_node.coords

            if game_map.is_target(curr_coords, target_cls):
                finish_coords = curr_coords
                while curr_coords in parents:
                    curr_coords = parents[curr_coords]
                    path.append(curr_coords)
                path = path[::-1]
                path.append(finish_coords)
                return cls._path_processor(entity, path, game_map, target_cls)

            closed_set.add(curr_coords)

            neighbors = game_map.get_neighbors(curr_coords, entity, target_cls)

            new_g = current_node.g + 1

            for n_coords in neighbors:
                if n_coords not in closed_set:
                    if node_to_update := next(
                        (n for n in open_list if n.coords == n_coords), None
                    ):
                        if new_g < current_node.g:
                            node_to_update.g = new_g
                            node_to_update.h = heuristic_func(
                                node_to_update.coords, goal_coords
                            )
                            parents[node_to_update.coords] = current_node.coords
                            heapq.heapify(open_list)
                    else:
                        new_node = cls.Node(
                            n_coords,
                            g=new_g,
                            h=heuristic_func(curr_coords, goal_coords),
                        )
                        heapq.heappush(open_list, new_node)
                        parents[n_coords] = current_node.coords

        return cls._path_processor(entity, path, game_map, target_cls)

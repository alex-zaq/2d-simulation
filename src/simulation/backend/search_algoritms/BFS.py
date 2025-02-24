from collections import deque

from ..entities import Ground


class BFS:
    @classmethod
    def search(cls, map, entity, target):
        parents = {}
        visited = set()

        queue = deque([entity])
        visited.add(entity)

        while queue:
            current = queue.popleft()

            if current == target:
                path = []
                while current in parents:
                    current = parents[current]
                    path.append(current)
                return path[::-1]

            neighbors = current.get_neighbors(map)
            filtered_neighbors = [n for n in neighbors if isinstance(n, (type(target), Ground))]

            for neighbor in filtered_neighbors:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
                    parents[neighbor] = current

        return None

from collections import deque


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

            for neighbor in current.get_neighbors(map):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
                    parents[neighbor] = current

        return None

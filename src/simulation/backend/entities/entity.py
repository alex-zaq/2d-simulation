class Entity:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, map):
        pass

    def get_neighbors(self, map):
        max_x, max_y = max(map.keys())
        x, y = self.x, self.y
        neighbors = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if nx < 0 or ny < 0 or nx > max_x or ny > max_y:
                    continue
                neighbors.append(map[(nx, ny)])
        return neighbors

    def __eq__(self, other):
        if isinstance(other, Entity):
            return self.x == other.x and self.y == other.y
        return False

    def __hash__(self):
        return hash((self.x, self.y))

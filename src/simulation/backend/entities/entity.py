

class Entity:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.move_status = False
        
    def get_coords(self):
        return self.x, self.y

    def move(self, game_map):
        pass

    def __eq__(self, other):
        if isinstance(other, Entity):
            return self.x == other.x and self.y == other.y
        return False

    def __hash__(self):
        return hash((self.x, self.y))

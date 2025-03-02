class BreedingAlgoritm:
    @classmethod
    def free_coords(cls, game_map, entity):
        breeding_coords = game_map.get_free_cell_for_breeding(entity)
        return breeding_coords


class BreedingAlgoritmBase:
    @classmethod
    def free_coords(self, game_map, entity):
        return None

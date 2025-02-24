import random

from .entities import Grass, Ground, Herbivore, Predator, Rock


class CoordGenerator:
    
    def __init__(self, x_count, y_count):
        self.x_count = x_count
        self.y_count = y_count
        self.coords = set()

    def get_non_repeating_coords_series(self, coord_count):
        
        loc_coords = set()
        while len(loc_coords) < coord_count:
            coords = (random.randint(0, self.x_count-1), random.randint(0, self.y_count-1))
            loc_coords.add(coords)
            self.coords.add(coords)
        return loc_coords
        
    def reset(self):
        self.coords = set()



class Spawner:
    def __init__(self, config):
        self.config = config



    def generate_map(self):
        
        predators_count = self.config.predators_start_count
        herbivore_count = self.config.herbivores_start_count
        grass_count = self.config.grass_count
        rock_count = self.config.rock_count
        
        x_count, y_count = self.config.map_size
        
        map = {(x, y): Ground(x, y) for x in range(x_count) for y in range(y_count)}
        
        coord_generator = CoordGenerator(x_count, y_count)
        rock_coords = coord_generator.get_non_repeating_coords_series(rock_count)
        grass_coords = coord_generator.get_non_repeating_coords_series(grass_count)
        predator_coords = coord_generator.get_non_repeating_coords_series(predators_count)
        herbivore_coords = coord_generator.get_non_repeating_coords_series(herbivore_count)
                    
        for x, y in rock_coords:
            map[(x, y)] = Rock(x, y)
            
        for x, y in grass_coords:
            map[(x, y)] = Grass(x, y)
            
        for x, y in predator_coords:
            map[(x, y)] = Predator(x, y)
            
        for x, y in herbivore_coords:
            map[(x, y)] = Herbivore(x, y)

        return map
    


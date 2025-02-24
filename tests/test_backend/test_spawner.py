from simulation.backend.spawner import CoordGenerator


def test_coord_generator():
    
    coord_generator = CoordGenerator(100, 100)
    
    res = coord_generator.get_non_repeating_coords_series(30)

    assert len(res) == 30

     



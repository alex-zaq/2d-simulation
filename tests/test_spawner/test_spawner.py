from simulation.backend.spawner import Coord_generator


def test_coord_generator():
    coord_generator = Coord_generator(100, 100)
    res = coord_generator.get_non_rpt_coords_srs(30)
    res = set(res)
    assert len(res) == 30

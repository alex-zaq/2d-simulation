from simulation.backend.spawner import CoordGenerator


def test_coord_generator():
    coord_generator = CoordGenerator(100, 100)
    res = coord_generator.get_non_rpt_coords_srs(30)
    res = set(res)
    assert len(res) == 30

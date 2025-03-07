class Escaping_algoritm:
    @classmethod
    def search(cls, game_map, entity, target_cls):
        escaping_coords = game_map.get_escaping_coords_from_target(
            entity.get_coords(), target_cls
        )
        return escaping_coords

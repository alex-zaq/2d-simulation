class EscapingAlgoritm:

    @classmethod
    def search(cls, game_map, entity, target_cls):
            
        escaping_coords = game_map.get_escaping_coords_from_target(
            entity.get_coords(), target_cls
        )

        return escaping_coords
    
    
    
class EscapingAlgoritmBase:
    @classmethod
    def search(cls, game_map, entity, target_cls):
        return None
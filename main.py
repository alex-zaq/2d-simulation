from src.simulation import Backend, Backend_config, Gui_config, GuiFrontend

if __name__ == "__main__":
    backend_config = Backend_config(
        map_size=(25, 15),
        grass_count=20,
        rock_count=5,
        predators_start_count=1,
        herbivores_start_count=4,


        herbivore_search_algoritm="bfs",
        herbivore_breeding=False,
        herbivore_escaping=False,
        herbivore_escaping_radius=2,
        herbivore_through_wall=True,

        predator_search_algoritm="bfs",
        predator_breeding=False,
        predator_through_wall=False,
    )

    gui_config = Gui_config(
        rock_pict="images/Obstacle.png",
        predator_pict="images/Predator.png",
        herbivore_pict="images/Herbivore.png",
        ground_pict="images/Ground.png",
        grass_pict="images/Grass.png",
        grid_color="gray",
        delay_ms=900,
    )

    b = Backend(backend_config)
    f = GuiFrontend(gui_config)
    f.use_backend(b)

    f.window_init()
    f.run()

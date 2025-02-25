from src.simulation import Backend, Backend_config, Gui_config, GuiFrontend, Simulation

if __name__ == "__main__":
    backend_config = Backend_config(
        map_size=(25, 15),
        herbivores_start_count=1,
        predators_start_count=0,
        grass_count=0,
        rock_count=0,
        predator_search_algoritm="bfs",
        herbivore_search_algoritm="bfs",
        predator_breeding=False,
        herbivore_breeding=False,
        herbivore_escaping_skill=False,
    )

    gui_config = Gui_config(
        rock_pict="images/Obstacle.png",
        predator_pict="images/Predator.png",
        herbivore_pict="images/Herbivore.png",
        grass_pict="images/Grass.png",
        grid_color = "gray",
    )

   
    b = Backend(backend_config)
    f = GuiFrontend(gui_config)
    f.use_backend(b)


    f.window_init()
    f.run()
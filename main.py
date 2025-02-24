from src.simulation import Backend, Backend_config, Gui_config, GuiFrontend, Simulation

if __name__ == "__main__":
    backend_config = Backend_config(
        map_size=(15, 15),
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
        resolution=(800, 600),
        rock_pict="images/Obstacle.png",
        predator_pict="images/Predator.png",
        herbivore_pict="images/Herbivore.png",
        grass_pict="images/Grass.png",
    )

    app = Simulation(
        backend=Backend(backend_config),
        frontend=GuiFrontend(gui_config),
    )

    app.run()
    
    print("end")

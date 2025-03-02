from src.simulation import Backend, Backend_config, Gui_config, GuiFrontend, Simulation

if __name__ == "__main__":
    backend_config = Backend_config(
        map_size=(25, 15),
        grass_count=20,
        rock_count=10,
        predators_start_count=1,
        herbivores_start_count=2,
        herbivore_search_algoritm="bfs",
        # herbivore_breeding=False,
        herbivore_breeding=True,
        herbivore_escaping=True,
        herbivore_escaping_radius=2,
        # herbivore_through_wall=False,
        herbivore_through_wall=True,
        predator_search_algoritm="bfs",
        # predator_breeding=False,
        predator_breeding=True,
        # predator_through_wall=False,
        predator_through_wall=True,
    )

    gui_config = Gui_config(
        rock_pict="images/Obstacle.png",
        predator_pict="images/Predator.png",
        herbivore_pict="images/Herbivore.png",
        ground_pict="images/Ground.png",
        grass_pict="images/Grass.png",
        grid_color="gray",
        delay_ms=600,
        cell_size=50,
    )

    simulation = Simulation(Backend(backend_config), GuiFrontend(gui_config))

    simulation.run()

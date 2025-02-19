from src.simulation import Backend, Backend_config, Gui_config, GuiFrontend, Simulation

if __name__ == "__main__":
    
    
    backend_config = Backend_config(
        map_size= (100, 100),
        creatures_count=10,
        predators_ratio=0.1,
        grass_count=30,
        rock_count=30,
        search_algoritm="bfs",
        breeding = False,
    )
    
    gui_config = Gui_config(
        resolution=(800, 600),
        rock_pict="images/rock.png",
        predator_pict="images/predator.png",
        herbivore_pict="images/herbivore.png",
        grass_pict="images/grass.png",
    )
            
    
    app = Simulation(
        backend = Backend(backend_config),
        frontend = GuiFrontend(gui_config),
    )
    
    app.run()

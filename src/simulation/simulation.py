class Simulation:
    def __init__(self, backend, frontend):
        self.backend = backend
        self.frontend = frontend
        self._simulation_init()

    def _simulation_init(self):
        self.frontend.use_backend(self.backend)

    def run(self):
        self.frontend.init()
        self.frontend.run()

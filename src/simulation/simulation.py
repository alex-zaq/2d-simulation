 
 
class Simulation:
    def __init__(self, backend, frontend):
        self.backend = backend
        self.frontend = frontend
        
    def run(self):
        self.init()
        while True:
            self.next_step()
            if self.frontend.get_stop_flag():
                break
        
        
    def init(self):
        self.backend.init()
        state = self.backend.get_state()
        self.frontend.set_state(state)
        
        
    def next_step(self):
        self.backend.next_step()
        state = self.backend.get_state()
        self.frontend.set_state(state)
        self.frontend.render()
        
    def previous_step(self):
        self.backend.previous_step()
        state = self.backend.get_state()
        self.frontend.set_state(state)
        self.frontend.render()
        
        

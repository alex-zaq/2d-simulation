import pygame


class GuiFrontend:
    def __init__(self, gui_config):
        self.gui_config = gui_config
        self.window_init()
        # self.draw_grid()
        # self.draw_btn_run()
        # self.draw_btn_stop()
        # self.draw_btn_next_step()
        # self.draw_btn_prev_step()
        
              

        
    def window_init(self):
        pygame.init()   
        WIDTH, HEIGHT = self.gui_config.resolution
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("2D Симуляция")
        self.clock = pygame.time.Clock()
        

    #     self.buttons = [
    #       {"rect": pygame.Rect(50, HEIGHT - 80, 100, 50), "text": "Старт", "active": False},
    #       {"rect": pygame.Rect(200, HEIGHT - 80, 100, 50), "text": "Стоп", "active": False},
    #       {"rect": pygame.Rect(350, HEIGHT - 80, 100, 50), "text": "Сброс", "active": False},
    #       {"rect": pygame.Rect(500, HEIGHT - 80, 100, 50), "text": "Настройки", "active": False}
    #   ]
      
        # self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]


        
    def update_map(self, map):
        self.map = map
        
        
    def render(self):
        pass
    
    def draw_grid(self):
       pass
   
    
    def draw_btn_run(self):
       pass
   
   
    def draw_btn_stop(self):
       pass
   
   
    def draw_btn_next_step(self):
       pass
   
   
    def draw_btn_prev_step(self):
       pass
   
       
    def stop(self):
        pygame.quit()
    
    
        
    

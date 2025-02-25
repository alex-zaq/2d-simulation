import sys

import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (150, 150, 150)
GRID_COLOR = (200, 200, 200)  # Light gray
BUTTON_COLOR = (150, 150, 150)
BUTTON_HOVER_COLOR = (180, 180, 180)
BUTTON_PANEL_COLOR = (220, 220, 220)


class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        FONT = pygame.font.SysFont("arial", 24)
        self.text_surface = FONT.render(text, True, BLACK)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

    def draw(self, surface):
        pygame.draw.rect(surface, GRAY, self.rect)
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 2)
        surface.blit(self.text_surface, self.text_rect)

    def is_hovered(self, pos):
        return self.rect.collidepoint(pos)


class GuiFrontend:
    def __init__(self, gui_config):
        self.gui_config = gui_config

    def use_backend(self, backend):
        self.backend = backend


    def _images_init(self):
        orig_predator_img = pygame.image.load(self.gui_config.predator_pict)
        orig_grass_img = pygame.image.load(self.gui_config.grass_pict)
        orig_rock_img = pygame.image.load(self.gui_config.rock_pict)    
        orig_herbivore_img = pygame.image.load(self.gui_config.herbivore_pict)

        self.predator_image = pygame.transform.scale(orig_predator_img, (self.CELL_SIZE, self.CELL_SIZE))
        self.grass_image = pygame.transform.scale(orig_grass_img, (self.CELL_SIZE, self.CELL_SIZE))
        self.rock_image = pygame.transform.scale(orig_rock_img, (self.CELL_SIZE, self.CELL_SIZE))
        self.herbivore_image = pygame.transform.scale(orig_herbivore_img, (self.CELL_SIZE, self.CELL_SIZE))

    

    def window_init(self):


        pygame.init()
        pygame.display.set_caption("2d simulation")
        GRID_WIDTH, GRID_HEIGHT = self.backend.config.map_size
        self.GRID_WIDTH = GRID_WIDTH
        self.GRID_HEIGHT = GRID_HEIGHT
        self.CELL_SIZE = 40
        self.GRID_AREA_WIDTH = self.GRID_WIDTH * self.CELL_SIZE
        self.GRID_AREA_HEIGHT = self.GRID_HEIGHT * self.CELL_SIZE

        self.BUTTON_PANEL_HEIGHT = 100
        self.SCREEN_WIDTH = self.GRID_AREA_WIDTH
        self.SCREEN_HEIGHT = self.GRID_AREA_HEIGHT + self.BUTTON_PANEL_HEIGHT
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.font.init()
        
        self._draw_grid()
        self._draw_btns()
        self._images_init()





    def run(self):
        active_cells = set()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False


                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in self.buttons.values():
                        if button.is_hovered(event.pos):
                            print(f"Нажата {button.text}")

                    if event.pos[1] < self.GRID_AREA_HEIGHT:
                        mouse_x, mouse_y = event.pos

                        cell_x = mouse_x // self.CELL_SIZE
                        cell_y = mouse_y // self.CELL_SIZE

                        self._draw_grid()  

                        active_cell = (cell_x, cell_y)
                        active_cells.clear()
                        active_cells.add(active_cell)

                        self.screen.blit(
                            self.predator_image,
                            (cell_x * self.CELL_SIZE + 1, cell_y * self.CELL_SIZE + 1),
                        )

                        pygame.draw.rect(
                            self.screen,
                            BUTTON_PANEL_COLOR,
                            (
                                0,
                                self.GRID_AREA_HEIGHT,
                                self.SCREEN_WIDTH,
                                self.BUTTON_PANEL_HEIGHT,
                            ),
                        )

                        for button in self.buttons.values():
                            button.draw(self.screen)

                        pygame.display.update()
                        
                        

    def _draw_grid(self):
        self.screen.fill((255, 255, 255))
        for x in range(0, self.GRID_AREA_WIDTH + 1, self.CELL_SIZE):
            pygame.draw.line(
                self.screen, self.gui_config.grid_color, (x, 0), (x, self.GRID_AREA_HEIGHT)
            )
        for y in range(0, self.GRID_AREA_HEIGHT + 1, self.CELL_SIZE):
            pygame.draw.line(
                self.screen, self.gui_config.grid_color, (0, y), (self.GRID_AREA_WIDTH, y)
            )
            
        pygame.display.update()

    def _draw_btns(self):
        # Параметры кнопок
        BUTTON_WIDTH = 180
        BUTTON_HEIGHT = 50
        BUTTON_SPACING = 20

        # Создание кнопок с центрированием
        total_buttons_width = 4 * BUTTON_WIDTH + 3 * BUTTON_SPACING
        start_x = (self.SCREEN_WIDTH - total_buttons_width) // 2

        button_names = ["Start", "Reset", "Next step", "Previous step"]

        self.buttons = {
            button_names[i]: Button(
                start_x + (BUTTON_WIDTH + BUTTON_SPACING) * i,
                self.GRID_AREA_HEIGHT + (self.BUTTON_PANEL_HEIGHT - BUTTON_HEIGHT) // 2,
                BUTTON_WIDTH,
                BUTTON_HEIGHT,
                button_names[i],
            )
            for i in range(4)
        }
        
        
        
        

        pygame.draw.rect(
            self.screen,
            BUTTON_PANEL_COLOR,
            (0, self.GRID_AREA_HEIGHT, self.SCREEN_WIDTH, self.BUTTON_PANEL_HEIGHT),
        )
        
        for button in self.buttons.values():
            button.draw(self.screen)
            
            
        pygame.display.update()
        
        
        

    def _stop(self):
        pygame.quit()
        sys.exit()

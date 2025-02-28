import sys

import pygame

from ..backend.entities import Grass, Herbivore, Predator, Rock

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
        # This line checks if the given position (mouse coordinates) is inside the button rectangle.
        # If it is, the button is considered "hovered".
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
        orig_ground_img = pygame.image.load(self.gui_config.ground_pict)

        self.predator_image = pygame.transform.scale(
            orig_predator_img, (self.CELL_SIZE, self.CELL_SIZE)
        )
        self.grass_image = pygame.transform.scale(
            orig_grass_img, (self.CELL_SIZE, self.CELL_SIZE)
        )
        self.rock_image = pygame.transform.scale(
            orig_rock_img, (self.CELL_SIZE, self.CELL_SIZE)
        )
        self.herbivore_image = pygame.transform.scale(
            orig_herbivore_img, (self.CELL_SIZE, self.CELL_SIZE)
        )
        self.ground_image = pygame.transform.scale(
            orig_ground_img, (self.CELL_SIZE, self.CELL_SIZE)
        )

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

        self.delay_ms = self.gui_config.delay_ms        
        self._draw_grid()
        self._draw_btns()
        self._images_init()

    def draw_map(self):
        self._draw_grid()

        for x, y in self.map:
            img = self.get_img_by_entity(self.map[(x, y)])
            self.screen.blit(img, (x * self.CELL_SIZE + 1, y * self.CELL_SIZE + 1))

        pygame.display.update()

    def get_img_by_entity(self, entity):
        if isinstance(entity, Grass):
            return self.grass_image
        elif isinstance(entity, Herbivore):
            return self.herbivore_image
        elif isinstance(entity, Predator):
            return self.predator_image
        elif isinstance(entity, Rock):
            return self.rock_image
        # elif isinstance(entity, Ground):
        #     return self.ground_image
        else:
            raise ValueError("Unknown entity type")

    def draw_img(self, image, x_grig, y_grid):
        self.screen.blit(
            image, (x_grig * self.CELL_SIZE + 1, y_grid * self.CELL_SIZE + 1)
        )
        pygame.display.update()

    def on_click_reset_btn(self, pos, auto_step_flag):
        btn = self.buttons["Reset"]

        if not btn.is_hovered(pos):
            return auto_step_flag

        # self.draw_img(self.predator_image, 5, 6)
        # self.draw_img(self.herbivore_image, 7, 8)

        self.backend.generate_map()
        self.map = self.backend.get_map()
        self.draw_map()

        return False

    def on_click_run(self, pos, auto_step_flag):
        btn = self.buttons["Run"]

        if not btn.is_hovered(pos):
            return auto_step_flag

        return True

    def on_click_next_btn(self, pos, auto_flag_status):
        btn = self.buttons["Next step"]

        if not btn.is_hovered(pos):
            return auto_flag_status

        self.backend.next_step()
        self.map = self.backend.get_map()
        self.draw_map()

        return False

    def on_click_previous_btn(self, pos, auto_flag_status):
        btn = self.buttons["Previous step"]

        if not btn.is_hovered(pos):
            return auto_flag_status

        self.backend.previous_step()
        self.map = self.backend.get_map()
        self.draw_map()

        return False

    def run(self):
        running = True
        auto_step_flag = False
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    auto_step_flag = self.on_click_reset_btn(event.pos, auto_step_flag)
                    auto_step_flag = self.on_click_next_btn(event.pos, auto_step_flag)
                    auto_step_flag = self.on_click_previous_btn(event.pos, auto_step_flag)
                    auto_step_flag = self.on_click_run(event.pos, auto_step_flag)

            if auto_step_flag:
                self.backend.next_step()
                self.map = self.backend.get_map()
                self.draw_map()
                print("next step")
                pygame.time.delay(self.delay_ms)

    def _draw_grid(self):
        self.clear_grid()
        for x in range(0, self.GRID_AREA_WIDTH + 1, self.CELL_SIZE):
            pygame.draw.line(
                self.screen,
                self.gui_config.grid_color,
                (x, 0),
                (x, self.GRID_AREA_HEIGHT),
            )
        for y in range(0, self.GRID_AREA_HEIGHT + 1, self.CELL_SIZE):
            pygame.draw.line(
                self.screen,
                self.gui_config.grid_color,
                (0, y),
                (self.GRID_AREA_WIDTH, y),
            )

    def clear_grid(self):
        for x in range(0, self.GRID_AREA_WIDTH, self.CELL_SIZE):
            for y in range(0, self.GRID_AREA_HEIGHT, self.CELL_SIZE):
                pygame.draw.rect(
                    self.screen, (255, 255, 255), (x, y, self.CELL_SIZE, self.CELL_SIZE)
                )

        # pygame.display.update()

    def _draw_btns(self):
        BUTTON_WIDTH = 180
        BUTTON_HEIGHT = 50
        BUTTON_SPACING = 20

        total_buttons_width = 4 * BUTTON_WIDTH + 3 * BUTTON_SPACING
        start_x = (self.SCREEN_WIDTH - total_buttons_width) // 2

        button_names = ["Run", "Reset", "Previous step", "Next step"]

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

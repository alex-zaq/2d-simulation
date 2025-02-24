import sys

import pygame


class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = (150, 150, 150)
        FONT = pygame.font.SysFont("arial", 24)
        self.text_surface = FONT.render(text, True, (0, 0, 0))
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 2)
        surface.blit(self.text_surface, self.text_rect)

    def is_hovered(self, pos):
        return self.rect.collidepoint(pos)


class GuiFrontend:
    def __init__(self, gui_config):
        self.gui_config = gui_config

    def use_backend(self, backend):
        self.backend = backend

    def window_init(self):
        pygame.init()

        # self.gui_config

        self.GRID_WIDTH = 20  # Изменено на 20
        self.GRID_HEIGHT = 20  # Изменено на 10
        self.CELL_SIZE = 40
        self.GRID_AREA_WIDTH = self.GRID_WIDTH * self.CELL_SIZE
        self.GRID_AREA_HEIGHT = self.GRID_HEIGHT * self.CELL_SIZE

        # Параметры кнопок
        BUTTON_PANEL_HEIGHT = 100
        self.SCREEN_WIDTH = self.GRID_AREA_WIDTH
        self.SCREEN_HEIGHT = self.GRID_AREA_HEIGHT + BUTTON_PANEL_HEIGHT

        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRID_COLOR = (200, 200, 200)
        self.BUTTON_COLOR = (150, 150, 150)
        self.BUTTON_HOVER_COLOR = (180, 180, 180)
        self.BUTTON_PANEL_COLOR = (220, 220, 220)

        pygame.font.init()

        original_image = pygame.image.load("images/Predator.png")
        self.image = pygame.transform.scale(
            original_image, (self.CELL_SIZE - 2, self.CELL_SIZE - 2)
        )

    def run(self):
        active_cells = set()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # Обработка движения мыши для эффекта наведения
                if event.type == pygame.MOUSEMOTION:
                    for button in self.buttons:
                        button.color = (
                            self.BUTTON_HOVER_COLOR
                            if button.is_hovered(event.pos)
                            else self.BUTTON_COLOR
                        )
                        button.draw(self.screen)
                        pygame.display.update(button.rect)

                # Обработка клика мыши
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Проверка клика по кнопкам
                    for button in self.buttons:
                        if button.is_hovered(event.pos):
                            print(f"Нажата {button.text}")

                    # Проверка клика по сетке
                    if event.pos[1] < self.GRID_AREA_HEIGHT:  # Только в пределах сетки
                        mouse_x, mouse_y = event.pos

                        # Определяем, в какой cell попал клик
                        cell_x = mouse_x // self.CELL_SIZE
                        cell_y = mouse_y // self.CELL_SIZE

                        # Очистка предыдущих активных ячеек
                        self.draw_grid()  # Перерисовка всей сетки

                        # Добавление новой активной ячейки
                        active_cell = (cell_x, cell_y)
                        active_cells.clear()
                        active_cells.add(active_cell)

                        # Отрисовка картинки в новой ячейке
                        self.screen.blit(
                            self.image,
                            (cell_x * self.CELL_SIZE + 1, cell_y * self.CELL_SIZE + 1),
                        )

                        # Отрисовка панели кнопок
                        pygame.draw.rect(
                            self.screen,
                            self.BUTTON_PANEL_COLOR,
                            (
                                0,
                                self.GRID_AREA_HEIGHT,
                                self.SCREEN_WIDTH,
                                self.BUTTON_PANEL_HEIGHT,
                            ),
                        )

                        # Переотрисовка кнопок
                        for button in self.buttons:
                            button.draw(self.screen)

                        # Обновление дисплея
                        pygame.display.update()

    def _draw_grid(self):
        self.screen.fill((255, 255, 255))
        for x in range(0, self.GRID_AREA_WIDTH + 1, self.CELL_SIZE):
            pygame.draw.line(
                self.screen, self.GRID_COLOR, (x, 0), (x, self.GRID_AREA_HEIGHT)
            )
        for y in range(0, self.GRID_AREA_HEIGHT + 1, self.CELL_SIZE):
            pygame.draw.line(
                self.screen, self.GRID_COLOR, (0, y), (self.GRID_AREA_WIDTH, y)
            )

    def _draw_btns(self):
        # Параметры кнопок
        BUTTON_WIDTH = 180
        BUTTON_HEIGHT = 50
        BUTTON_SPACING = 20

        # Создание кнопок с центрированием
        total_buttons_width = 4 * BUTTON_WIDTH + 3 * BUTTON_SPACING
        start_x = (self.SCREEN_WIDTH - total_buttons_width) // 2

        self.buttons = [
            Button(
                start_x + (BUTTON_WIDTH + BUTTON_SPACING) * i,
                self.GRID_AREA_HEIGHT + (self.BUTTON_PANEL_HEIGHT - BUTTON_HEIGHT) // 2,
                BUTTON_WIDTH,
                BUTTON_HEIGHT,
                f"Кнопка {i + 1}",
            )
            for i in range(4)
        ]

        pygame.draw.rect(
            self.screen,
            self.BUTTON_PANEL_COLOR,
            (0, self.GRID_AREA_HEIGHT, self.SCREEN_WIDTH, self.BUTTON_PANEL_HEIGHT),
        )

    def _stop(self):
        pygame.quit()
        sys.exit()

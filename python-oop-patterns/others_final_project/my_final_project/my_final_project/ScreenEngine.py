import pygame
import collections

colors = {
    "black": (0, 0, 0, 255),
    "white": (255, 255, 255, 255),
    "red": (255, 0, 0, 255),
    "green": (0, 255, 0, 255),
    "blue": (0, 0, 255, 255),
    "wooden": (153, 92, 0, 255),
}


class ScreenHandle(pygame.Surface):

    def __init__(self, *args, **kwargs):
        if len(args) > 1:
            self.successor = args[-1]
            self.next_coord = args[-2]
            args = args[:-2]
        else:
            self.successor = None
            self.next_coord = (0, 0)
        super().__init__(*args, **kwargs)
        self.fill(colors["wooden"])

    def draw(self, canvas):
        if self.successor is not None:
            canvas.blit(self.successor, self.next_coord)
            self.successor.draw(canvas)

    def connect_engine(self, engine):
        if self.successor is not None:
            return self.successor.connect_engine(engine)


class GameSurface(ScreenHandle):

    def connect_engine(self, engine):
        self.game_engine = engine
        if self.successor is not None:
            return self.successor.connect_engine(engine)

    def draw_hero(self):
        self.game_engine.hero.draw(self)

    def draw_map(self):
        size = self.game_engine.sprite_size

        screen_size = list(map(lambda x: x / size, self.get_size()))

        hero_pos = self.game_engine.hero.position
        min_x = int(max(0, hero_pos[0] - screen_size[0] + 5))
        min_y = int(max(0, hero_pos[1] - screen_size[1] + 5))

        if self.game_engine.map:
            for i in range(len(self.game_engine.map[0]) - min_x):
                for j in range(len(self.game_engine.map) - min_y):
                    self.blit(self.game_engine.map[min_y + j][min_x + i][0],
                              (i * self.game_engine.sprite_size, j * self.game_engine.sprite_size))
        else:
            self.fill(colors["white"])

    def draw_object(self, sprite, coord):
        size = self.game_engine.sprite_size

        screen_size = list(map(lambda x: x / size, self.get_size()))

        hero_pos = self.game_engine.hero.position
        min_x = int(max(0, hero_pos[0] - screen_size[0] + 5))
        min_y = int(max(0, hero_pos[1] - screen_size[1] + 5))

        self.blit(sprite, ((coord[0] - min_x) * self.game_engine.sprite_size,
                           (coord[1] - min_y) * self.game_engine.sprite_size))

    def draw(self, canvas):
        size = self.game_engine.sprite_size

        screen_size = list(map(lambda x: x / size, self.get_size()))

        hero_pos = self.game_engine.hero.position
        min_x = int(max(0, hero_pos[0] - screen_size[0] + 5))
        min_y = int(max(0, hero_pos[1] - screen_size[1] + 5))

        self.draw_map()
        for obj in self.game_engine.objects:
            self.blit(obj.sprite[0], ((obj.position[0] - min_x) * self.game_engine.sprite_size,
                                      (obj.position[1] - min_y) * self.game_engine.sprite_size))
        self.draw_hero()

        if self.successor is not None:
            canvas.blit(self.successor, self.next_coord)
            return self.successor.draw(canvas)


class ProgressBar(ScreenHandle):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fill(colors["wooden"])

    def connect_engine(self, engine):
        self.engine = engine
        if self.successor is not None:
            return self.successor.connect_engine(engine)

    def draw(self, canvas):
        self.fill(colors["wooden"])
        pygame.draw.rect(self, colors["black"], (50, 30, 200, 30), 2)
        pygame.draw.rect(self, colors["black"], (50, 70, 200, 30), 2)

        pygame.draw.rect(self, colors[
                         "red"], (50, 30, 200 * self.engine.hero.hp / self.engine.hero.max_hp, 30))
        pygame.draw.rect(self, colors["green"],
                         (50, 70, 200 * self.engine.hero.exp / (100 * (2**(self.engine.hero.level - 1))), 30))

        font = pygame.font.SysFont("comicsansms", 20)
        self.blit(font.render(f'Hero at {self.engine.hero.position}', True, colors["black"]),
                  (250, 0))

        self.blit(font.render(f'{self.engine.level} floor', True, colors["black"]),
                  (10, 0))

        self.blit(font.render(f'HP', True, colors["black"]),
                  (10, 30))
        self.blit(font.render(f'Exp', True, colors["black"]),
                  (10, 70))

        self.blit(font.render(f'{self.engine.hero.hp}/{self.engine.hero.max_hp}', True, colors["black"]),
                  (60, 30))
        self.blit(font.render(f'{self.engine.hero.exp}/{(100*(2**(self.engine.hero.level-1)))}', True, colors["black"]),
                  (60, 70))

        self.blit(font.render(f'Level', True, colors["black"]),
                  (300, 30))
        self.blit(font.render(f'Gold', True, colors["black"]),
                  (300, 70))

        self.blit(font.render(f'{self.engine.hero.level}', True, colors["black"]),
                  (360, 30))
        self.blit(font.render(f'{self.engine.hero.gold}', True, colors["black"]),
                  (360, 70))

        self.blit(font.render(f'Str', True, colors["black"]),
                  (420, 30))
        self.blit(font.render(f'Luck', True, colors["black"]),
                  (420, 70))

        self.blit(font.render(f'{self.engine.hero.stats["strength"]}', True, colors["black"]),
                  (480, 30))
        self.blit(font.render(f'{self.engine.hero.stats["luck"]}', True, colors["black"]),
                  (480, 70))

        self.blit(font.render(f'SCORE', True, colors["black"]),
                  (550, 30))
        self.blit(font.render(f'{self.engine.score:.4f}', True, colors["black"]),
                  (550, 70))

        if self.successor is not None:
            canvas.blit(self.successor, self.next_coord)
            return self.successor.draw(canvas)


class MiniMap(ScreenHandle):
    start_position = [3, 3]

    def connect_engine(self, engine):
        self.engine = engine
        if self.successor is not None:
            self.successor.connect_engine(engine)

    def draw_hero(self):
        min_x = self.start_position[0]
        min_y = self.start_position[1]
        pygame.draw.rect(self, colors["red"],
                         (min_x + 25, min_y + 25, min_x + 3, min_y + 3))

    def draw_map(self):
        min_x = - self.start_position[0] + self.engine.hero.position[0]
        min_y = - self.start_position[1] + self.engine.hero.position[1]

        if self.engine.map:
            for i in range(len(self.engine.map[0]) - min_x):
                for j in range(len(self.engine.map) - min_y):
                    self.blit(self.engine.map[min_y + j][min_x + i][0],
                              (i * 8, j * 8))
        else:
            self.fill(colors["white"])

    def draw_object(self, sprite, coord):
        min_x = - self.start_position[0] + self.engine.hero.position[0]
        min_y = - self.start_position[1] + self.engine.hero.position[1]

        pygame.draw.rect(self, colors["red"],
                         ((coord[0] - min_x) * 8, (coord[1] - min_y) * 8,
                          (coord[0] - min_x) * 8, (coord[1] - min_y) * 8))

    def draw(self, canvas):
        min_x = - self.start_position[0] + self.engine.hero.position[0]
        min_y = - self.start_position[1] + self.engine.hero.position[1]

        self.draw_map()
        for obj in self.engine.objects:
            pygame.draw.circle(self, colors["green"],
                               ((obj.position[0] - min_x) * 8,
                                (obj.position[1] - min_y) * 8), 5)

        self.draw_hero()
        pygame.draw.lines(self, (10, 10, 10, 10), True,
                          [(0, 0), (0, 148), (158, 148), (158, 0)], 4)

        if self.successor is not None:
            canvas.blit(self.successor, self.next_coord)
            return self.successor.draw(canvas)


class InfoWindow(ScreenHandle):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.len = 20
        clear = []
        self.data = collections.deque(clear, maxlen=self.len)

    def update(self, value):
        self.data.append(f"> {str(value)}")

    def draw(self, canvas):
        self.fill(colors["wooden"])

        font = pygame.font.SysFont("comicsansms", 14)
        for i, text in enumerate(self.data):
            self.blit(font.render(text, True, colors["black"]),
                      (5, 20 + 18 * i))

        if self.successor is not None:
            canvas.blit(self.successor, self.next_coord)
            return self.successor.draw(canvas)

    def connect_engine(self, engine):
        self.engine = engine
        engine.subscribe(self)
        if self.successor is not None:
            return self.successor.connect_engine(engine)


class HelpWindow(ScreenHandle):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.len = 30
        clear = []
        self.data = collections.deque(clear, maxlen=self.len)
        self.data.append([" →", "Move Right"])
        self.data.append([" ←", "Move Left"])
        self.data.append([" ↑ ", "Move Top"])
        self.data.append([" ↓ ", "Move Bottom"])
        self.data.append([" H ", "Show Help"])
        self.data.append(["Num+", "Zoom +"])
        self.data.append(["Num-", "Zoom -"])
        self.data.append([" R ", "Restart Game"])
        self.data.append(["Coursera", "OOP final project"])

    def connect_engine(self, engine):
        self.engine = engine
        if self.successor is not None:
            return self.successor.connect_engine(engine)

    def draw(self, canvas):
        alpha = 0
        if self.engine.show_help:
            alpha = 128
        self.fill((0, 0, 0, alpha))
        # size = self.get_size()
        font1 = pygame.font.SysFont("courier", 24)
        font2 = pygame.font.SysFont("serif", 24)
        if self.engine.show_help:
            pygame.draw.lines(self, (255, 0, 0, 255), True, [
                              (0, 0), (700, 0), (700, 500), (0, 500)], 5)
            for i, text in enumerate(self.data):
                self.blit(font1.render(text[0], True, ((128, 128, 255))),
                          (50, 50 + 30 * i))
                self.blit(font2.render(text[1], True, ((128, 128, 255))),
                          (150, 50 + 30 * i))

        if self.successor is not None:
            canvas.blit(self.successor, self.next_coord)
            return self.successor.draw(canvas)

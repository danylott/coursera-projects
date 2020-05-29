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
            self.successor.connect_engine(engine)

class GameSurface(ScreenHandle):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.engine = None

    def connect_engine(self, engine):
        self.engine = engine
        super().connect_engine(engine)

    def draw_hero(self):
        self.engine.hero.draw(self)

    def check_end_of_map(self, ideal_x, ideal_y, count_sprites_x, count_sprites_y, map_size_x, map_size_y):
        if ideal_x + count_sprites_x > map_size_x and ideal_y + count_sprites_y > map_size_y:
            return int(map_size_x - count_sprites_x), int(map_size_y - count_sprites_y)
        elif ideal_x + count_sprites_x > map_size_x:
            return int(map_size_x - count_sprites_x), ideal_y
        elif ideal_y + count_sprites_y > map_size_y:
            return ideal_x, int(map_size_y - count_sprites_y)
        else:
            return ideal_x, ideal_y

    def calculate_top_left_corner(self, min_x, min_y):
        map_size_x = len(self.engine.map[0])
        map_size_y = len(self.engine.map)
        hero_x = self.engine.hero.position[0]
        hero_y = self.engine.hero.position[1]
        window_w, window_h = self.get_size()
        sprite_size = self.engine.sprite_size
        count_sprites_x = window_w / sprite_size
        count_sprites_y = window_h / sprite_size
        ideal_x = int(hero_x - count_sprites_x/2)
        ideal_y = int(hero_y - count_sprites_y/2)

        if ideal_x > 0 and ideal_y > 0:
            return self.check_end_of_map(ideal_x, ideal_y, count_sprites_x, count_sprites_y, map_size_x, map_size_y)
        elif ideal_x > 0:
            return self.check_end_of_map(ideal_x, min_y, count_sprites_x, count_sprites_y, map_size_x, map_size_y)
        elif ideal_y > 0:
            return self.check_end_of_map(min_x, ideal_y, count_sprites_x, count_sprites_y, map_size_x, map_size_y)
        else:
            return self.check_end_of_map(min_x, min_y, count_sprites_x, count_sprites_y, map_size_x, map_size_y)

    def draw_map(self):
        min_x, min_y = self.calculate_top_left_corner(0, 0)

        if self.engine.map:
            for i in range(len(self.engine.map[0]) - min_x):
                for j in range(len(self.engine.map) - min_y):
                    self.blit(self.engine.map[min_y + j][min_x + i][
                              0], (i * self.engine.sprite_size, j * self.engine.sprite_size))
        else:
            self.fill(colors["white"])

    def draw_object(self, sprite, coord):
        size = self.engine.sprite_size
        min_x, min_y = self.calculate_top_left_corner(0, 0)

        self.blit(sprite, ((coord[0] - min_x) * size,
                           (coord[1] - min_y) * size))

    def draw(self, canvas):
        self.draw_map()
        for obj in self.engine.objects:
            self.draw_object(obj.sprite[0], obj.position)

        self.draw_hero()

        super().draw(canvas)


class ProgressBar(ScreenHandle):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.engine = None
        self.fill(colors["wooden"])

    def connect_engine(self, engine):
        self.engine = engine
        super().connect_engine(engine)

    def draw(self, canvas):
        self.fill(colors["wooden"])
        pygame.draw.rect(self, colors["black"], (50, 30, 200, 30), 2)
        pygame.draw.rect(self, colors["black"], (50, 70, 200, 30), 2)

        pygame.draw.rect(self, colors[
                         "red"], (50, 30, 200 * self.engine.hero.hp / self.engine.hero.max_hp, 30))
        pygame.draw.rect(self, colors["green"], (50, 70,
                                                 200 * self.engine.hero.exp / (100 * (2**(self.engine.hero.level - 1))), 30))

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

        self.blit(font.render(f'Endur', True, colors["black"]),
                  (420, 30))
        self.blit(font.render(f'Luck', True, colors["black"]),
                  (420, 70))

        self.blit(font.render(f'{self.engine.hero.stats["endurance"]}', True, colors["black"]),
                  (480, 30))
        self.blit(font.render(f'{self.engine.hero.stats["luck"]}', True, colors["black"]),
                  (480, 70))

        self.blit(font.render(f'SCORE', True, colors["black"]),
                  (550, 30))
        self.blit(font.render(f'{self.engine.score:.4f}', True, colors["black"]),
                  (550, 70))

        super().draw(canvas)


class InfoWindow(ScreenHandle):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.len = 30
        clear = []
        self.data = collections.deque(clear, maxlen=self.len)

    def update(self, value):
        self.data.append(f"> {str(value)}")

    def draw(self, canvas):
        self.fill(colors["wooden"])
        size = self.get_size()

        font = pygame.font.SysFont("comicsansms", 10)
        for i, text in enumerate(self.data):
            self.blit(font.render(text, True, colors["black"]),
                      (5, 20 + 18 * i))

        super().draw(canvas)

    def connect_engine(self, engine):
        engine.subscribe(self)
        super().connect_engine(engine)


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
        self.engine = None
    # FIXME You can add some help information

    def connect_engine(self, engine):
        self.engine = engine
        super().connect_engine(engine)

    def draw(self, canvas):
        alpha = 0
        if self.engine.show_help:
            alpha = 128
        self.fill((0, 0, 0, alpha))
        size = self.get_size()
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

        super().draw(canvas)

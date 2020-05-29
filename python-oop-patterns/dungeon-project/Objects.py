from abc import ABC, abstractmethod
import pygame
import random
import math


def create_sprite(img, sprite_size):
    icon = pygame.image.load(img).convert_alpha()
    icon = pygame.transform.scale(icon, (sprite_size, sprite_size))
    sprite = pygame.Surface((sprite_size, sprite_size), pygame.HWSURFACE)
    sprite.blit(icon, (0, 0))
    return sprite


class AbstractObject(ABC):
    def __init__(self):
        self.sprite = None
        self.position = None

    def draw(self, display):
        size = display.engine.sprite_size
        min_x, min_y = display.calculate_top_left_corner(0, 0)
        display.blit(self.sprite, ((self.position[0] - min_x) * size,
                                 (self.position[1] - min_y) * size))


class Interactive(ABC):

    @abstractmethod
    def interact(self, engine, hero):
        pass


class Ally(AbstractObject, Interactive):

    def __init__(self, icon, action, position):
        super().__init__()
        self.sprite = icon
        self.action = action
        self.position = position

    def interact(self, engine, hero):
        self.action(engine, hero)


class Creature(AbstractObject):

    def __init__(self, icon, stats, position):
        super().__init__()
        self.sprite = icon
        self.stats = stats.copy()
        self.position = position
        self.hp = 0
        self.max_hp = 0
        self.calc_max_hp_and_hp()

    def calc_max_hp_and_hp(self):
        prev_hp = self.max_hp
        self.max_hp = 5 + self.stats["strength"] * 2
        difference = self.max_hp - prev_hp
        self.hp = max(1, self.hp + difference)


class Enemy(Creature, Interactive):
    def __init__(self, icon, stats, xp, position):
        super().__init__(icon, stats, position)
        self.xp = xp

    def interact(self, engine, hero):
        for i in range(max(5, self.stats["intelligence"] - random.randint(0, max(1, hero.stats["intelligence"])))):
            hero_luck = random.randint(0, max(1, hero.stats["luck"]))

            enemy_luck = random.randint(0, self.stats["luck"])
            if enemy_luck > hero_luck:
                hero.hp -= math.ceil(self.stats["strength"] / max(hero.stats["endurance"] - self.stats["endurance"], 1))

        # before death punch from enemy
        hero.hp -= math.ceil(self.stats["strength"] / max(hero.stats["endurance"] - self.stats["endurance"], 1))

        # hero death
        if hero.hp <= 0:
            engine.notify("You were killed!")
            engine.notify("GAME OVER")
            engine.notify("Press R to restart")
            hero.hp = 0
            engine.game_process = False
            return

        # win
        engine.notify("Epic win!")
        hero.exp += self.xp
        messages = hero.level_up()
        engine.score += self.xp / hero.stats["strength"]
        for message in messages:
            engine.notify(message)


class Hero(Creature):

    def __init__(self, stats, icon):
        pos = [1, 1]
        self.level = 1
        self.exp = 0
        self.gold = 0
        super().__init__(icon, stats, pos)

    def level_up(self):
        while self.exp >= 100 * (2 ** (self.level - 1)):
            yield "level up!"
            self.exp = self.exp - 100 * (2 ** (self.level - 1))
            self.level += 1
            self.stats["strength"] += 2
            self.stats["endurance"] += 2
            self.calc_max_hp_and_hp()
            self.hp = self.max_hp


class Effect(Hero):

    def __init__(self, base):
        self.base = base
        self.stats = self.base.stats.copy()
        self.apply_effect()

    @property
    def position(self):
        return self.base.position

    @position.setter
    def position(self, value):
        self.base.position = value

    @property
    def level(self):
        return self.base.level

    @level.setter
    def level(self, value):
        self.base.level = value

    @property
    def gold(self):
        return self.base.gold

    @gold.setter
    def gold(self, value):
        self.base.gold = value

    @property
    def hp(self):
        return self.base.hp

    @hp.setter
    def hp(self, value):
        self.base.hp = value

    @property
    def max_hp(self):
        return self.base.max_hp

    @max_hp.setter
    def max_hp(self, value):
        self.base.max_hp = value

    @property
    def exp(self):
        return self.base.exp

    @exp.setter
    def exp(self, value):
        self.base.exp = value

    @property
    def sprite(self):
        return self.base.sprite

    @abstractmethod
    def apply_effect(self):
        pass


class Berserk(Effect):
    def apply_effect(self):
        new_stats = self.stats
        new_stats["strength"] += 7
        new_stats["endurance"] += 7
        new_stats["luck"] += 7

        new_stats["intelligence"] -= 3

        self.stats = new_stats

        self.calc_max_hp_and_hp()


class Blessing(Effect):
    def apply_effect(self):
        new_stats = self.stats
        new_stats["strength"] += 2
        new_stats["endurance"] += 2
        new_stats["luck"] += 2
        new_stats["intelligence"] += 2

        self.stats = new_stats

        self.calc_max_hp_and_hp()


class Weakness(Effect):
    def apply_effect(self):
        new_stats = self.stats
        new_stats["strength"] -= 4
        new_stats["endurance"] -= 4

        self.stats = new_stats
        self.calc_max_hp_and_hp()


class BrokenMind(Effect):
    def apply_effect(self):
        new_stats = self.stats
        new_stats["strength"] = 2
        new_stats["endurance"] = 200
        new_stats["intelligence"] -= 40
        new_stats["luck"] += 50

        self.stats = new_stats
        self.calc_max_hp_and_hp()


class DragonStrength(Effect):
    def apply_effect(self):
        new_stats = self.stats
        new_stats["strength"] += 50
        new_stats["endurance"] += 50
        new_stats["intelligence"] -= 50
        new_stats["luck"] -= 50

        self.stats = new_stats
        self.calc_max_hp_and_hp()

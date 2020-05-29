from abc import ABC, abstractmethod
import pygame
import random


def create_sprite(img, sprite_size):
    icon = pygame.image.load(img).convert_alpha()
    icon = pygame.transform.scale(icon, (sprite_size, sprite_size))
    sprite = pygame.Surface((sprite_size, sprite_size), pygame.HWSURFACE)
    sprite.blit(icon, (0, 0))
    return sprite


class Interactive(ABC):

    @abstractmethod
    def interact(self, engine, hero):
        pass


class AbstractObject(ABC):

    @abstractmethod
    def __init__(self):
        pass

    def draw(self, display):
        display.draw_object(self.sprite, self.position)


class Ally(AbstractObject, Interactive):

    def __init__(self, icon, action, position):
        self.sprite = icon
        self.action = action
        self.position = position

    def interact(self, engine, hero):
        self.action(engine, hero)


class Creature(AbstractObject):

    def __init__(self, icon, stats, position):
        self.sprite = icon
        self.stats = stats
        self.position = position
        self.hp_incr = []
        self.calc_max_HP()
        self.hp = self.max_hp

    def calc_max_HP(self):
        self.max_hp = 5 + self.stats["endurance"] * 2
        for value in self.hp_incr:
            self.max_hp += value


class Hero(Creature):

    def __init__(self, stats, icon):
        pos = [1, 1]
        self.level = 1
        self.exp = 0
        self.gold = 100
        self.hp_incr = []
        super().__init__(icon, stats, pos)

    def level_up(self):
        while self.exp >= 100 * (2 ** (self.level - 1)):
            yield "level up!"
            self.level += 1
            self.stats["strength"] += 2
            self.stats["endurance"] += 2
            self.calc_max_HP()
            self.hp = self.max_hp


class Enemy(Creature, Interactive):

    def __init__(self, icon, stats, xp, position):
        self.sprite = icon
        self.stats = stats
        self.position = position
        self.hp_incr = []
        self.calc_max_HP()
        self.hp = self.max_hp
        self.exp = xp

    def interact(self, engine, hero):
        hit = bool(random.getrandbits(1))
        if hit and not hero.stats['luck'] > 100:
            hero.hp -= self.stats['strength']
        if hero.hp <= 0:
            hero.hp = 0
            engine.notify("GAME OVER")
            engine.notify("Press R to restart")
            engine.game_process = False
        else:
            hero.exp += self.exp
            for m in hero.level_up():
                engine.notify(m)


class Effect(Hero):

    def __init__(self, base):
        self.base = base
        self.stats = self.base.stats.copy()
        self.hp_incr = self.base.hp_incr.copy()
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
        self.stats["strength"] += 7
        self.stats["endurance"] += 7
        self.stats["intelligence"] -= 3
        self.stats["luck"] += 7
        self.calc_max_HP()
        self.max_hp += 50
        self.hp += 50
        self.hp_incr.append(50)


class Blessing(Effect):

    def apply_effect(self):
        self.stats["strength"] += 2
        self.stats["endurance"] += 2
        self.stats["intelligence"] += 2
        self.stats["luck"] += 2
        self.calc_max_HP()


class Weakness(Effect):

    def apply_effect(self):
        self.stats["strength"] -= 4
        self.stats["endurance"] -= 4


class Concentration(Effect):

    def apply_effect(self):
        self.stats["intelligence"] += 50
        self.stats["luck"] += 50
        self.max_hp += 150
        self.hp = self.max_hp
        self.hp_incr.append(150)

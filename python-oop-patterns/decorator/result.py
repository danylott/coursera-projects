from abc import ABC, abstractmethod


class AbstractEffect(Hero, ABC):
    def __init__(self, base):
        self.base = base

    @abstractmethod
    def get_positive_effects(self):
        pass

    @abstractmethod
    def get_negative_effects(self):
        pass

    def get_stats(self):
        return self.base.get_stats()


class AbstractPositive(AbstractEffect):
    @abstractmethod
    def get_positive_effects(self):
        pass

    def get_negative_effects(self):
        return self.base.get_negative_effects()


class AbstractNegative(AbstractEffect):
    def get_positive_effects(self):
        return self.base.get_positive_effects()

    @abstractmethod
    def get_negative_effects(self):
        pass


class Berserk(AbstractPositive):
    def get_positive_effects(self):
        new_positive_effects = self.base.get_positive_effects()
        new_positive_effects.append('Berserk')
        return new_positive_effects.copy()

    def get_stats(self):
        new_stats = self.base.get_stats()
        new_stats["Strength"] += 7
        new_stats["Endurance"] += 7
        new_stats["Agility"] += 7
        new_stats["Luck"] += 7

        new_stats["Perception"] -= 3
        new_stats["Charisma"] -= 3
        new_stats["Intelligence"] -= 3

        new_stats["HP"] += 50

        return new_stats.copy()


class Blessing(AbstractPositive):
    def get_positive_effects(self):
        new_positive_effects = self.base.get_positive_effects()
        new_positive_effects.append('Blessing')
        return new_positive_effects

    def get_stats(self):
        new_stats = self.base.get_stats()
        new_stats["Strength"] += 2
        new_stats["Endurance"] += 2
        new_stats["Agility"] += 2
        new_stats["Luck"] += 2
        new_stats["Perception"] += 2
        new_stats["Charisma"] += 2
        new_stats["Intelligence"] += 2

        return new_stats


class Weakness(AbstractNegative):
    def get_negative_effects(self):
        new_negative_effects = self.base.get_negative_effects()
        new_negative_effects.append('Weakness')
        return new_negative_effects

    def get_stats(self):
        new_stats = self.base.get_stats()
        new_stats["Strength"] -= 4
        new_stats["Endurance"] -= 4
        new_stats["Agility"] -= 4

        return new_stats


class EvilEye(AbstractNegative):
    def get_negative_effects(self):
        new_negative_effects = self.base.get_negative_effects()
        new_negative_effects.append('EvilEye')
        return new_negative_effects

    def get_stats(self):
        new_stats = self.base.get_stats()
        new_stats["Luck"] -= 10

        return new_stats


class Curse(AbstractNegative):
    def get_negative_effects(self):
        new_negative_effects = self.base.get_negative_effects()
        new_negative_effects.append('Curse')
        return new_negative_effects

    def get_stats(self):
        new_stats = self.base.get_stats()
        new_stats["Strength"] -= 2
        new_stats["Endurance"] -= 2
        new_stats["Agility"] -= 2
        new_stats["Luck"] -= 2
        new_stats["Perception"] -= 2
        new_stats["Charisma"] -= 2
        new_stats["Intelligence"] -= 2

        return new_stats
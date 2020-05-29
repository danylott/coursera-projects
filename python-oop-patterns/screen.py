#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import random
import math

SCREEN_DIM = (800, 600)


# =======================================================================================
# Vector 2d class
# =======================================================================================

class Vec2d:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __sub__(self, other):
        """"simply return difference between them"""
        return Vec2d(self.x - other.x, self.y - other.y)

    def __add__(self, other):
        """vector 2d addition"""
        if type(other) == Vec2d:
            return Vec2d(self.x + other.x, self.y + other.y)
        elif type(other) == tuple:
            return Vec2d(self.x + other[0], self.y + other[1])
        else:
            return Vec2d(self.x + other, self.y + other)

    def __len__(self):
        """return vector length"""
        return math.sqrt(self.x * self.x + self.y * self.y)

    def __mul__(self, other):
        """return vector multiplication on number"""
        return Vec2d(self.x * other, self.y * other)

    __rmul__ = __mul__

    def int_pair(self):
        """return pair of vector coordinates"""
        return tuple((self.x, self.y))


# =======================================================================================
# Polyline class functions - to create line with basic points
# =======================================================================================

class Polyline:
    def __init__(self, point_color, line_color, hue, width, speed_coefficient=1.1):
        self.points = []
        self.speeds = []
        self.point_color = point_color
        self.line_color = line_color
        self.width = width
        self.hue = hue
        self.speed_coefficient = speed_coefficient  # multiply (or divide) on this coefficient when change_speed called

    def add_point(self, point, speed):
        self.points.append(point)
        self.speeds.append(speed)

    def pop_back_point(self):
        self.points = self.points[:-1]
        self.speeds = self.speeds[:-1]

    def decrease_speed(self):
        self.__change_speed(1 / self.speed_coefficient)

    def increase_speed(self):
        self.__change_speed(self.speed_coefficient)

    def __change_speed(self, coefficient):
        for i in range(len(self.speeds)):
            self.speeds[i] = (self.speeds[i][0] * coefficient, self.speeds[i][1] * coefficient)

    def draw_points(self):
        """function to draw points on screen"""
        for p in self.points:
            pygame.draw.circle(gameDisplay, self.point_color,
                               (int(p.int_pair()[0]), int(p.int_pair()[1])), self.width)

    def draw_lines(self, line_points):
        self.hue = (self.hue + 1) % 360
        self.line_color.hsla = (self.hue, 100, 50, 100)
        """function to draw lines on screen"""
        for p_n in range(-1, len(line_points) - 1):
            pygame.draw.line(gameDisplay, self.line_color,
                             (int(line_points[p_n].int_pair()[0]), int(line_points[p_n].int_pair()[1])),
                             (int(line_points[p_n + 1].int_pair()[0]),
                              int(line_points[p_n + 1].int_pair()[1])), self.width)

    def set_points(self):
        """function to recalculate coordinates of base points"""
        for p in range(len(self.points)):
            self.points[p] = self.points[p] + self.speeds[p]
            if self.points[p].int_pair()[0] > SCREEN_DIM[0] or self.points[p].int_pair()[0] < 0:
                self.speeds[p] = (- self.speeds[p][0], self.speeds[p][1])
            if self.points[p].int_pair()[1] > SCREEN_DIM[1] or self.points[p].int_pair()[1] < 0:
                self.speeds[p] = (self.speeds[p][0], -self.speeds[p][1])


# =======================================================================================
# Knot class functions for recalculating coordinates on adding new points
# =======================================================================================

class Knot(Polyline):
    def get_knot(self, count):
        """function to calculate coordinates of lines depend on basic points"""
        if len(self.points) < 3:
            return []
        res = []
        for i in range(-2, len(self.points) - 2):
            ptn = [(self.points[i] + self.points[i + 1]) * 0.5, self.points[i + 1],
                   (self.points[i + 1] + self.points[i + 2]) * 0.5]

            res.extend(self.get_points(ptn, count))
        return res

    def get_points(self, base_points, count):
        alpha = 1 / count
        res = []
        for i in range(count):
            res.append(self.get_point(base_points, i * alpha))
        return res

    def get_point(self, base_points, alpha, deg=None):
        if deg is None:
            deg = len(base_points) - 1
        if deg == 0:
            return base_points[0]
        return base_points[deg] * alpha + self.get_point(base_points, alpha, deg - 1) * (1 - alpha)


def draw_help():
    """function to draw help window"""
    gameDisplay.fill((50, 50, 50))
    font1 = pygame.font.SysFont("courier", 24)
    font2 = pygame.font.SysFont("serif", 24)
    data = [["F1", "Show Help"], ["R", "Restart"],
            ["P", "Pause/Play"], ["Num+", "More points"],
            ["Num-", "Less points"],
            ["", ""],
            ["Mouse Left", "Add point to left Polyphony"],
            ["Mouse Right", "Add point to right Polyphony"],
            ["ctrl + ML", "Delete last point from left Polyphony"],
            ["ctrl + MR", "Delete last point from right Polyphony"],
            ["", ""],
            ["Left Arrow", "Decrease speed for left Polyphony"],
            ["Right Arrow", "Increase speed for left Polyphony"],
            ["Down Arrow", "Decrease speed for right Polyphony"],
            ["Up Arrow", "Increase speed for right Polyphony"],
            ["", ""],
            [str(steps), "Current points"]]

    pygame.draw.lines(gameDisplay, (255, 50, 50, 255), True, [
        (0, 0), (800, 0), (800, 600), (0, 600)], 5)
    for i, text in enumerate(data):
        gameDisplay.blit(font1.render(
            text[0], True, (128, 128, 255)), (100, 50 + 30 * i))
        gameDisplay.blit(font2.render(
            text[1], True, (128, 128, 255)), (300, 50 + 30 * i))


def create_left_polyphony():
    return Knot(point_color=(255, 255, 255), line_color=pygame.Color(0), hue=0, width=3)


def create_right_polyphony():
    return Knot(point_color=(100, 100, 100), line_color=pygame.Color(0), hue=100, width=3)


# =======================================================================================
# Main program - visualizing PolyLines with PyGame library
# =======================================================================================
if __name__ == "__main__":
    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_DIM)
    pygame.display.set_caption("MyScreenSaver")

    steps = 35
    working = True
    show_help = False
    pause = True

    polyphony_left = create_left_polyphony()
    polyphony_right = create_right_polyphony()

    while working:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                working = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    working = False
                elif event.key == pygame.K_r:
                    polyphony_left = create_left_polyphony()
                    polyphony_right = create_right_polyphony()
                elif event.key == pygame.K_p:
                    pause = not pause
                elif event.key == pygame.K_KP_PLUS:
                    steps += 1
                elif event.key == pygame.K_F1:
                    show_help = not show_help
                elif event.key == pygame.K_KP_MINUS:
                    steps -= 1 if steps > 1 else 0
                elif event.key == pygame.K_LEFT:
                    polyphony_left.decrease_speed()
                elif event.key == pygame.K_RIGHT:
                    polyphony_left.increase_speed()
                elif event.key == pygame.K_DOWN:
                    polyphony_right.decrease_speed()
                elif event.key == pygame.K_UP:
                    polyphony_right.increase_speed()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # mouse left click
                if event.button == 1:
                    if pygame.key.get_mods() & pygame.KMOD_CTRL:
                        polyphony_left.pop_back_point()
                    else:
                        polyphony_left.add_point(Vec2d(event.pos[0], event.pos[1]),
                                                 (random.random() * 2, random.random() * 2))
                # mouse right click
                if event.button == 3:
                    if pygame.key.get_mods() & pygame.KMOD_CTRL:
                        polyphony_right.pop_back_point()
                    else:
                        polyphony_right.add_point(Vec2d(event.pos[0], event.pos[1]),
                                                  (random.random() * 2, random.random() * 2))

        gameDisplay.fill((0, 0, 0))
        polyphony_left.draw_points()
        polyphony_left.draw_lines(polyphony_left.get_knot(steps))

        polyphony_right.draw_points()
        polyphony_right.draw_lines(polyphony_right.get_knot(steps))
        if not pause:
            polyphony_left.set_points()
            polyphony_right.set_points()
        if show_help:
            draw_help()

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)

# from itertools import cycle
# from math import hypot
# from numpy import random
# import matplotlib.pyplot as plt
#
# def dbscan_naive(P, eps, m, distance):
#
#     NOISE = 0
#     C = 0
#
#     visited_points = set()
#     clustered_points = set()
#     clusters = {NOISE: []}
#
#     def region_query(p):
#         return [q for q in P if distance(p, q) < eps]
#
#     def expand_cluster(p, neighbours):
#         if C not in clusters:
#             clusters[C] = []
#         clusters[C].append(p)
#         clustered_points.add(p)
#         while neighbours:
#             q = neighbours.pop()
#             if q not in visited_points:
#                 visited_points.add(q)
#                 neighbourz = region_query(q)
#                 if len(neighbourz) > m:
#                     neighbours.extend(neighbourz)
#             if q not in clustered_points:
#                 clustered_points.add(q)
#                 clusters[C].append(q)
#                 if q in clusters[NOISE]:
#                     clusters[NOISE].remove(q)
#
#     for p in P:
#         if p in visited_points:
#             continue
#         visited_points.add(p)
#         neighbours = region_query(p)
#         if len(neighbours) < m:
#             clusters[NOISE].append(p)
#         else:
#             C += 1
#             expand_cluster(p, neighbours)
#
#     return clusters
#
# if __name__ == "__main__":
#     P = [(random.randn()/6, random.randn()/6) for i in range(150)]
#     P.extend([(random.randn()/4 + 2.5, random.randn()/5) for i in range(150)])
#     P.extend([(random.randn()/5 + 1, random.randn()/2 + 1) for i in range(150)])
#     P.extend([(i/25 - 1, + random.randn()/20 - 1) for i in range(100)])
#     P.extend([(i/25 - 2.5, 3 - (i/50 - 2)**2 + random.randn()/20) for i in range(150)])
#     clusters = dbscan_naive(P, 0.2, 4, lambda x, y: hypot(x[0] - y[0], x[1] - y[1]))
#     for c, points in zip(cycle('bgrcmykgrcmykgrcmykgrcmykgrcmykgrcmyk'), clusters.values()):
#         X = [p[0] for p in points]
#         Y = [p[1] for p in points]
#         plt.scatter(X, Y, c=c)
#     plt.show()


# import random
# import sys
#
# import pygame
#
# pygame.init()
#
# GREEN = (0, 255, 0)
# YELLOW = (255, 255, 0)
# RED = (255, 0, 0)
#
# width, height = 800, 600
# screen = pygame.display.set_mode((width, height))
# pygame.display.set_caption("DBSCAN Algorithm")
#
#
# points = []
#
# def draw_point(x, y, flag):
#     color = GREEN if flag == 0 else YELLOW if flag == 1 else RED
#     pygame.draw.circle(screen, color, (x, y), 5)
# def draw_points():
#     screen.fill((255, 255, 255))
#
#     for point in points:
#         x, y, flag = point
#         draw_point(x, y, flag)
#
#     pygame.display.flip()
#
#
# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit()
#
#         if event.type == pygame.MOUSEBUTTONDOWN:
#             x, y = pygame.mouse.get_pos()
#             flag = random.randint(0, 2)
#             points.append((x, y, flag))
#             draw_point(x, y, flag)
#     pygame.display.flip()


import pygame
import numpy as np

# Инициализация Pygame
pygame.init()

# Параметры экрана
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("DBSCAN Clustering")

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

# Переменные для хранения точек
points = []
labels = []


# Функция для отрисовки точек
def draw_points():
    SCREEN.fill(WHITE)
    for point, label in zip(points, labels):
        color = GREEN if label == 0 else (YELLOW if label == 1 else RED)
        pygame.draw.circle(SCREEN, color, point, 5)


# Функция для определения расстояния между двумя точками
def distance(p1, p2):
    return np.linalg.norm(np.array(p1) - np.array(p2))


# Основной цикл программы
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Левая кнопка мыши - добавление точки
                points.append(event.pos)
                labels.append(-1)  # Неопределенный кластер
            if event.button == 3:  # Правая кнопка мыши - выдача метки
                for i, (p, l) in enumerate(zip(points, labels)):
                    if distance(p, event.pos) < 50:
                        if pygame.key.get_mods() & pygame.KMOD_CTRL:
                            labels[i] = 0  # Зеленый цвет
                        elif pygame.key.get_mods() & pygame.KMOD_SHIFT:
                            labels[i] = 1  # Желтый цвет
                        else:
                            labels[i] = 2  # Красный цвет

    draw_points()
    pygame.display.flip()

pygame.quit()
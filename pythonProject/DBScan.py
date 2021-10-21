import numpy as np
import pygame


def near_by_points(points, idx, epsilon):
    near = []
    for point_idx in range(0, len(points)):
        if np.linalg.norm(points[idx] - points[point_idx]) < epsilon:
            near.append(point_idx)
    return near


def colors(list_col):
    if list_col == 1:
        return 255, 0, 0
    if list_col == 2:
        return 0, 255, 0
    if list_col == 3:
        return 0, 0, 255
    if list_col == 4:
        return 0, 0, 0
    return 125, 125, 125


def draw(list_col, clusters):
    for point, cluster in zip(list_col, clusters):
        color = colors(cluster)
        radius = 10
        pygame.draw.circle(screen, color, point, radius)


def algorithm(_points, _epsilon):
    labels = [0] * len(_points)
    cluster_idx = 0
    minimum_points = 1
    for i in range(0, len(_points)):
        if not (labels[i] == 0):
            continue
        near_points = near_by_points(_points, i, _epsilon)
        if len(near_points) < minimum_points:
            labels[i] = -1
        else:
            cluster_idx += 1
            labels[i] = cluster_idx
            i = 0
            while i < len(near_points):
                point = near_points[i]
                if labels[point] == -1:
                    labels[point] = cluster_idx

                elif labels[point] == 0:
                    labels[point] = cluster_idx
                    point_near = near_by_points(_points, point, _epsilon)
                    if len(point_near) >= minimum_points:
                        near_points = near_points + point_near
                i += 1
    return labels


pygame.init()
screen = pygame.display.set_mode((600, 400))
screen.fill('WHITE')
pygame.display.update()
FPS = 60
clock = pygame.time.Clock()
points = []

epsilon = 40

play = True
while play:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            points.append(pygame.mouse.get_pos())
            screen.fill('WHITE')
            prediction = algorithm(np.array(points), epsilon)
            draw(points, prediction)

    pygame.display.update()

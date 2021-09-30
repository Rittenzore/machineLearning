import matplotlib.pyplot as plt
import matplotlib.colors as clr
import numpy as np
import random
import sys
import math


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.centroid: Point
        self.color = 'black'


class Centroid(Point):
    def __init__(self, x, y, id):
        super().__init__(x, y)
        self.id = id
        self.cluster_points = list()

    def add_cluster_point(self, point):
        point.color = self.color
        self.cluster_points.append(point)

    def clear(self):
        self.cluster_points.clear()


saved_pos = list()
points = list()
centroids = list()
max_range = 100
min_range = 0
centroid_size = 10
centroids_list = list()
j_array = []
d_array = []


# Рисует все точки
def draw_points():
    for point in points:
        plt.scatter(point.x, point.y, c=point.color)


# Рисует центроиды
def draw_centroids():
    for _centroid in centroids:
        plt.scatter(_centroid.x, _centroid.y, c=_centroid.color, linewidths=centroid_size)


# Сохраняет точки центроидов
def backup():
    saved_pos.clear()
    for centroid in centroids:
        saved_pos.append(Point(centroid.x, centroid.y))


# Проверяет изменились позиции центроидов
def centroid_pos_changed():
    for i in range(len(centroids)):
        if saved_pos[i].x != centroids[i].x or saved_pos[i].y != centroids[i].y:
            return True
    return False


# Рисует точки и центроиды
def draw():
    draw_points()
    draw_centroids()


# Генерация точек
def generate_points(count) -> list:
    generated_points = list()
    for _i in range(count):
        point = Point(random.randrange(min_range, max_range), random.randrange(min_range, max_range))
        # print('Point ({index}): [{x}, {y}]'.format(index=_i, x=point.x, y=point.y))
        generated_points.append(point)
    return generated_points


# Поиск центра
def find_center(_points):
    average_x = 0
    average_y = 0

    for point in _points:
        average_x += point.x
        average_y += point.y

    average_x = average_x / len(_points)
    average_y = average_y / len(_points)

    return Point(average_x, average_y)


# Возвращает дистанцию между двумя точками
def get_dist(point_1, point_2):
    delta_x = point_1.x - point_2.x
    delta_y = point_1.y - point_2.y
    return math.sqrt(delta_x * delta_x + delta_y * delta_y)


# Поиск наиболее отдаленной точки от центра
def find_farthest_point(center):
    max_dist = 0
    found_point = None
    for point in points:
        found_dist = get_dist(center, point)
        if found_dist >= max_dist:
            max_dist = found_dist
            found_point = point
    return found_point, max_dist


# Поиск центроидов
def find_centroids(center, rad, _centroid_count):
    founded_centroid = list()
    for _i in range(_centroid_count):
        k = _i
        x = center.x + rad * math.cos(2 * math.pi / _centroid_count * k)
        y = center.y + rad * math.sin(2 * math.pi / _centroid_count * k)
        centroid = Centroid(x, y, _i)
        centroid.color = clr.to_hex(np.random.rand(3, ))
        founded_centroid.append(centroid)
    return founded_centroid


# Поиск ближайших точек для центроидов
def find_nearest_points_for_clusters():
    for point in points:
        min_dist = sys.maxsize
        found_centroid: Centroid = None
        for centroid in centroids:
            found_dist = get_dist(point, centroid)
            if found_dist < min_dist:
                min_dist = found_dist
                found_centroid = centroid
        found_centroid.add_cluster_point(point)
        centroids_list.append(found_centroid)
    return centroids_list


# Сумма квадратов расстояний от точек до центроидов кластеров
# k - количество элементов в centroid_list'e
def j_by_c(centroids_list):
    for centroid in centroids_list:
        sqr_distance = 0
        for cluster_point in centroid.cluster_points:
            sqr_distance += get_dist(cluster_point, centroid) ** 2
    j_array.append(sqr_distance)
    return j_array


# Поиск оптимального числа кластеров
def d_by_k(previous, current, next):
    d_by_k_var = math.fabs(current - next) / math.fabs(previous - current)
    return d_by_k_var


# Перерасчет позиций для центроидов
def recalculate_centroids():
    for centroid in centroids:
        center = find_center(centroid.cluster_points)
        centroid.x = center.x
        centroid.y = center.y


# Очистка точек кластеров
def clear_centroids_points():
    for _centroid in centroids:
        _centroid.clear()


# Отрисовка
def execute(centroid_count):
    # points.clear()
    # points.extend(generate_points(point_count))
    circle_center = find_center(points)
    print(len(points))

    farthest_point, radius = find_farthest_point(circle_center)

    centroids.extend(find_centroids(circle_center, radius, centroid_count))
    backup()

    find_nearest_points_for_clusters()

    draw()

    plt.ion()
    plt.pause(1)

    while True:
        plt.clf()
        recalculate_centroids()
        clear_centroids_points()
        find_nearest_points_for_clusters()
        plt.pause(1)
        print(len(points))
        draw()
        # print('Iteration: {index}'.format(index=_iter + 1))
        plt.pause(1)
        if centroid_pos_changed():
            backup()
        else:
            break

    plt.pause(1)
    return plt


def start(centroids_count, points_count):
    points.extend(generate_points(points_count))
    for i in range(centroids_count):
        execute(1)
        j_by_c(centroids_list)
    print(j_array)

    for i in range(1, len(j_array) - 1):
        d_array.append(d_by_k(j_array[i - 1], j_array[i], j_array[i + 1]))
    print(d_array)

    centroids.clear()
    clear_centroids_points()
    plt.clf()
    execute(d_array.index(min(d_array)) + 1)
    print("Finished.")


# Запуск
# Первое число - количество центроидов
# Второе число - количество точек
start(6, 100)
from matplotlib import pyplot as plt

import numpy as np
import random
import math


def generate_dataset(n, d, data_min, data_max):
    res = []
    for i in range(n):
        sub = []
        for j in range(d):
            sub.append(random.uniform(data_min, data_max))
        res.append(sub)
    return res


def plot_dataset(dataset, clusters=None, points=None):
    colors = ['r', 'k', 'y', 'g', 'b', 'w', 'm']
    if points is None:
        points = []
    if clusters is None:
        clusters = []

    for i in range(len(dataset)):
        point = dataset[i]
        plt.scatter(point[0], point[1], c=colors[points[i]])

    for cluster in clusters:
        plt.scatter(cluster[0], cluster[1], s=200, c=colors[clusters.index(cluster)])
    plt.show()


def plot_with_markers(clusters, dataset, membership):
    points = get_points(membership)
    plot_dataset(dataset, clusters=clusters, points=points)


# n - число точек
# c - число кластеров
def generate_random_membership_function(n, c):
    membership = np.random.rand(n, c)
    summation = [sum(center) for center in membership]
    normalized = []
    for i in range(len(membership)):
        tmp = []
        for d in membership[i]:
            tmp.append(d / summation[i])
        normalized.append(tmp)
    return normalized


# Рассчитывем средневзвешенное значение точек
# для каждого кластера i высчиытваем по формуле
# m - параметр нечеткости
# i - фискированное значение
def update_cluster_centers(dataset, membership_matrix, m):
    number_of_clusters = len(membership_matrix[0])
    cluster_centers = []
    for i in range(number_of_clusters):
        u_ik = list(zip(*membership_matrix))[i]
        u_ik_m = [x ** m for x in u_ik]
        sigma_u_ik_m = sum(u_ik_m)
        weighted_data = []
        for k in range(len(dataset)):
            weighted_vector = []
            for f in range(len(dataset[k])):
                weighted_vector.append(u_ik_m[k] * dataset[k][f])
            weighted_data.append(weighted_vector)
        sigma_data_u_ik_m = [sum(x) for x in list(zip(*weighted_data))]
        cluster_centers.append([sigma_data_u_ik_m[d] / sigma_u_ik_m for d in range(len(sigma_data_u_ik_m))])
    return cluster_centers


def distance(p, q):
    summ = 0
    for i in range(len(p)):
        summ += (p[i] - q[i]) ** 2
    return math.sqrt(summ)


def update_membership_matrix(dataset, clusters, m):
    membership_matrix = []
    fuzzy_power = float(2 / (m - 1))
    n = len(dataset)
    c = len(clusters)
    for i in range(n):
        var = sum([(1 / distance(dataset[i], clusters[x])) ** fuzzy_power for x in range(c)])
        membership = []
        for j in range(c):
            num = (1 / distance(dataset[i], clusters[j])) ** fuzzy_power
            membership.append(num / var)
        membership_matrix.append(membership)
    return membership_matrix


def get_points(membership_matrix):
    res = []
    for membership in membership_matrix:
        max_index = membership.index(max(membership))
        res.append(max_index)
    return res


def c_means(cluster_no, iterations, dataset, m=2):
    c = cluster_no
    n = len(dataset)
    membership = generate_random_membership_function(n, c)
    clusters = []
    for i in range(iterations):
        clusters = update_cluster_centers(dataset, membership, m)
        membership = update_membership_matrix(dataset, clusters, m)
    return clusters, membership


def start():
    features = 2
    number_of_data = 100  # количество точек
    number_of_clusters = 3  # количество кластеров
    iterations = 10  # количество итераций
    data_min = 0
    data_max = 1
    dataset = generate_dataset(number_of_data, features, data_min, data_max)
    # init_colors(number_of_clusters)
    cluster_centers, final_memberships = c_means(number_of_clusters, iterations, dataset)
    plot_with_markers(cluster_centers, dataset, final_memberships)
    print(cluster_centers)


start()

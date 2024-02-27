#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Есть словарь координат городов

sites = {
    'Moscow': (550, 370),
    'London': (510, 510),
    'Paris': (480, 480),
}

# Составим словарь словарей расстояний между ними
# расстояние на координатной сетке - ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

distances = {}
def rs(x,y):
    return ((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2) ** 0.5
# TODO здесь заполнение словаря
for k in sites.keys():
    distances[k] = {}
    for a in sites.keys():
        if a!=k:
            distances[k]
[a] = rs(sites[k], sites[a])
print(distances)





#!/usr/bin/python
# -*- coding: UTF-8 -*-
from kdbush import KDBush
import json
from geokdbush import around, distance

# read file
# f = open("cities.json", "r")
# f = open("./small.json", "r")


# parse file
# cities = json.load(f)
cities = [
    {"name": "Austin", "lat": 30.2672, "lon": 97.7431},
    {"name": "New York City", "lat": 40.7128, "lon": 74.006},
    {"name": "Santa Monica", "lat": 34.0195, "lon": 118.4912}
]

# print("CITIES", len(cities))

index = KDBush(cities)
'''
print('performs search according to maxResults')
# points = around(index, -119.7051, 34.4363, 5)
points = around(index, 118.4912, 34.0195, 2)

# t.same(points.map(p=> p.name).join(', '), 'Mission Canyon, Santa Barbara, Montecito, Summerland, Goleta')
for i in points:
    print(i["name"])
# print("RESULT", result)
# print("POINTS", points)
'''
# print('performs exhaustive search in correct order')
# LON = 118.4912  # Santa Monica
# LAT = 34.0195
# LON = 30.5  # kiev
# LAT = 50.5
# LON = 139.6503  # tokyo
# LAT = 35.6762
# LON = 74.006  # NYC
# LAT = 40.7128
LON = -104.68249  # Santa Rosa
LAT = 34.93867
points = around(index, LON, LAT)
# points = around(index, 30.5, 50.5)
# print("POINTS", points)

# for point in points:
# print("City", point["name"])

# c = {"lon": 30.5, "lat": 50.5}
c = {"lon": LON, "lat": LAT}
closestList = []
for city in cities:
    dist = distance(c["lon"], c["lat"], city["lon"], city["lat"])
    closestList.append((city["name"], dist))

# print("closestList", closestList)


def getKey(item):
    return item[1]


done = sorted(closestList, key=getKey)
print("DONE", done)

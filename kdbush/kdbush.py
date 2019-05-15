import math
from kbRange import kbRange
from kbSort import kbSort
from kbWithin import kbWithin


class KDBush:
    def __init__(self, points, nodeSize=64):
        self.nodeSize = nodeSize
        self.points = points

        self.ids = ids = [None] * len(points)
        self.coords = coords = [None] * len(points) * 2

        for i in range(0, len(points)):
            ids[i] = i
            coords[2 * i] = points[i][0]
            coords[2 * i + 1] = points[i][1]

        kbSort(ids, coords, nodeSize, 0, len(ids) - 1, 0)

    def range(self, minX, minY, maxX, maxY):
        return kbRange(self.ids, self.coords, minX, minY, maxX, maxY, self.nodeSize)

    def within(self, x, y, r):
        return kbWithin(self.ids, self.coords, x, y, r, self.nodeSize)

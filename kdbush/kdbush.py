import math


def kbRange(ids, coords, minX, minY, maxX, maxY, nodeSize):
    stack = [0, len(ids) - 1, 0]
    result = []

    # recursively search for items in range in the kd-sorted arrays
    while (len(stack) > 0):
        axis = stack.pop()
        right = stack.pop()
        left = stack.pop()

        # if we reached "tree node", search linearly
        if right - left <= nodeSize:
            for i in range(left, right + 1):
                x = coords[2 * i]
                y = coords[2 * i + 1]
                if (x >= minX and x <= maxX and y >= minY and y <= maxY):
                    result.append(ids[i])
            continue

        # otherwise find the middle index
        m = (left + right) >> 1

        # include the middle item if it is in range
        x = coords[2 * m]
        y = coords[2 * m + 1]
        if (x >= minX and x <= maxX and y >= minY and y <= maxY):
            result.append(ids[m])

        # queue search in halves that intersect the query
        if (axis == 0 if minX <= x else minY <= y):
            stack.append(left)
            stack.append(m - 1)
            stack.append(1 - axis)

        if (axis == 0 if maxX >= x else maxY >= y):
            stack.append(m + 1)
            stack.append(right)
            stack.append(1 - axis)

    return result


def kbSort(ids, coords, nodeSize, left, right, axis):
    if (right - left <= nodeSize):
        return

    m = (left + right) >> 1  # middle index

    # sort ids and coords around the middle index so that the halves lie
    # either left/right or top/bottom correspondingly(taking turns)
    select(ids, coords, m, left, right, axis)

    # recursively kd-sort first half and second half on the opposite axis
    kbSort(ids, coords, nodeSize, left, m - 1, 1 - axis)
    kbSort(ids, coords, nodeSize, m + 1, right, 1 - axis)


def select(ids, coords, k, left, right, axis):
    while (right > left):
        if (right - left > 600):
            n = right - left + 1
            m = k - left + 1
            z = math.log(n)
            s = 0.5 * math.exp(2 * z / 3)
            sd = 0.5 * math.sqrt(z * s * (n - s) / n) * \
                (m - n / 2 < 0 if - 1 else 1)
            newLeft = math.max(left, math.floor(k - m * s / n + sd))
            newRight = math.min(right, math.floor(k + (n - m) * s / n + sd))
            select(ids, coords, k, newLeft, newRight, axis)

        t = coords[2 * k + axis]
        i = left
        j = right

        swapItem(ids, coords, left, k)
        if (coords[2 * right + axis] > t):
            swapItem(ids, coords, left, right)

        while (i < j):
            swapItem(ids, coords, i, j)
            i += 1
            j -= 1
            while (coords[2 * i + axis] < t):
                i += 1
            while (coords[2 * j + axis] > t):
                j -= 1

        if (coords[2 * left + axis] == t):
            swapItem(ids, coords, left, j)
        else:
            j += 1
            swapItem(ids, coords, j, right)

        if (j <= k):
            left = j + 1
        if (k <= j):
            right = j - 1


def swapItem(ids, coords, i, j):
    swap(ids, i, j)
    swap(coords, 2 * i, 2 * j)
    swap(coords, 2 * i + 1, 2 * j + 1)


def swap(arr, i, j):
    tmp = arr[i]
    arr[i] = arr[j]
    arr[j] = tmp


def within(ids, coords, qx, qy, r, nodeSize):
    stack = [0, len(ids) - 1, 0]
    result = []
    r2 = r * r

    # recursively search for items within radius in the kd-sorted arrays
    while (len(stack)):
        axis = stack.pop()
        right = stack.pop()
        left = stack.pop()

        # if we reached "tree node", search linearly
        if (right - left <= nodeSize):
            for i in range(left, right + 1):
                if (sqDist(coords[2 * i], coords[2 * i + 1], qx, qy) <= r2):
                    result.append(ids[i])
            continue

        # otherwise find the middle index
        m = (left + right) >> 1

        # include the middle item if it's in range
        x = coords[2 * m]
        y = coords[2 * m + 1]
        if (sqDist(x, y, qx, qy) <= r2):
            result.append(ids[m])

        # queue search in halves that intersect the query
        if (axis == 0 if qx - r <= x else qy - r <= y):
            stack.append(left)
            stack.append(m - 1)
            stack.append(1 - axis)

        if (axis == 0 if qx + r >= x else qy + r >= y):
            stack.append(m + 1)
            stack.append(right)
            stack.append(1 - axis)

    return result


def sqDist(ax, ay, bx, by):
    dx = ax - bx
    dy = ay - by
    return dx * dx + dy * dy


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
        return within(self.ids, self.coords, x, y, r, self.nodeSize)

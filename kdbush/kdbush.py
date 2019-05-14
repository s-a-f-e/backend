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

'''
# test data
points = [
    [54,1],[97,21],[65,35],[33,54],[95,39],[54,3],[53,54],[84,72],[33,34],[43,15],[52,83],[81,23],[1,61],[38,74],
    [11,91],[24,56],[90,31],[25,57],[46,61],[29,69],[49,60],[4,98],[71,15],[60,25],[38,84],[52,38],[94,51],[13,25],
    [77,73],[88,87],[6,27],[58,22],[53,28],[27,91],[96,98],[93,14],[22,93],[45,94],[18,28],[35,15],[19,81],[20,81],
    [67,53],[43,3],[47,66],[48,34],[46,12],[32,38],[43,12],[39,94],[88,62],[66,14],[84,30],[72,81],[41,92],[26,4],
    [6,76],[47,21],[57,70],[71,82],[50,68],[96,18],[40,31],[78,53],[71,90],[32,14],[55,6],[32,88],[62,32],[21,67],
    [73,81],[44,64],[29,50],[70,5],[6,22],[68,3],[11,23],[20,42],[21,73],[63,86],[9,40],[99,2],[99,76],[56,77],
    [83,6],[21,72],[78,30],[75,53],[41,11],[95,20],[30,38],[96,82],[65,48],[33,18],[87,28],[10,10],[40,34],
    [10,20],[47,29],[46,78]]
  
ids = [
    97, 74, 95, 30, 77, 38, 76, 27, 80, 55, 72, 90, 88, 48, 43, 46, 65, 39, 62, 93, 9, 96, 47, 8, 3, 12, 15, 14, 21, 41, 36, 40, 69, 56, 85, 78, 17, 71, 44,
    19, 18, 13, 99, 24, 67, 33, 37, 49, 54, 57, 98, 45, 23, 31, 66, 68, 0, 32, 5, 51, 75, 73, 84, 35, 81, 22, 61, 89, 1, 11, 86, 52, 94, 16, 2, 6, 25, 92,
    42, 20, 60, 58, 83, 79, 64, 10, 59, 53, 26, 87, 4, 63, 50, 7, 28, 82, 70, 29, 34, 91]

coords = [
    10,20,6,22,10,10,6,27,20,42,18,28,11,23,13,25,9,40,26,4,29,50,30,38,41,11,43,12,43,3,46,12,32,14,35,15,40,31,33,18,
    43,15,40,34,32,38,33,34,33,54,1,61,24,56,11,91,4,98,20,81,22,93,19,81,21,67,6,76,21,72,21,73,25,57,44,64,47,66,29,
    69,46,61,38,74,46,78,38,84,32,88,27,91,45,94,39,94,41,92,47,21,47,29,48,34,60,25,58,22,55,6,62,32,54,1,53,28,54,3,
    66,14,68,3,70,5,83,6,93,14,99,2,71,15,96,18,95,20,97,21,81,23,78,30,84,30,87,28,90,31,65,35,53,54,52,38,65,48,67,
    53,49,60,50,68,57,70,56,77,63,86,71,90,52,83,71,82,72,81,94,51,75,53,95,39,78,53,88,62,84,72,77,73,99,76,73,81,88,
    87,96,98,96,82]

index = KDBush(points)
result = index.range(20, 30, 50, 70)
print(result) # [60, 20, 45, 3, 17, 71, 44, 19, 18, 15, 69, 90, 62, 96, 47, 8, 77, 72]

for id in result:
  p = points[id]
  if p[0] < 20 or p[0] > 50 or p[1] < 30 or p[1] > 70:
    print("FAIL")

for id in result:
  p = points[id]
  if id not in result and p[0] >= 20 and p[0] <= 50 and p[1] >= 30 and p[1] <= 70:
    print("FAIL: outside point not in range")


def sqDist2(a, b): 
  dx = a[0] - b[0]
  dy = a[1] - b[1]
  return dx * dx + dy * dy;

index2 = KDBush(points)
qp = [50, 50]
r = 20
r2 = 20 * 20
result = index.within(qp[0], qp[1], r)
print(result)  # [60, 6, 25, 92, 42, 20, 45, 3, 71, 44, 18, 96]

for id in result:
  p = points[id]
  if (sqDist2(p, qp) > r2): print('FAIL: result point in range')

for id in result:
  p = points[id]
  if (id not in result and sqDist2(p, qp) <= r2):
      print('FAIL: result point not in range')
'''
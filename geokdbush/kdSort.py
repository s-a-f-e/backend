
import math


def kdSort(ids, coords, nodeSize, left, right, axis):
    if (right - left <= nodeSize):
        return

    m = (left + right) >> 1  # middle index

    # sort ids and coords around the middle index so that the halves lie
    # either left/right or top/bottom correspondingly(taking turns)
    select(ids, coords, m, left, right, axis)

    # recursively kd-sort first half and second half on the opposite axis
    kdSort(ids, coords, nodeSize, left, m - 1, 1 - axis)
    kdSort(ids, coords, nodeSize, m + 1, right, 1 - axis)


def select(ids, coords, k, left, right, axis):
    while (right > left):
        if (right - left > 600):
            n = right - left + 1
            m = k - left + 1
            z = math.log(n)
            s = 0.5 * math.exp(2 * z / 3)
            sd = 0.5 * math.sqrt(z * s * (n - s) / n) * \
                (m - n / 2 < 0 if - 1 else 1)
            newLeft = max(left, math.floor(k - m * s / n + sd))
            newRight = min(right, math.floor(k + (n - m) * s / n + sd))
            select(ids, coords, k, newLeft, newRight, axis)

        t = coords[2 * k + axis]
        i = int(left)
        j = int(right)

        swapItem(ids, coords, left, k)
        if (coords[2 * int(right) + int(axis)] > t):
            swapItem(ids, coords, left, right)

        while (i < j):
            swapItem(ids, coords, i, j)
            i += 1
            j -= 1
            while (coords[2 * i + axis] < t):
                i += 1
            while (coords[2 * j + axis] > t):
                j -= 1

        if (coords[2 * int(left) + int(axis)] == t):
            swapItem(ids, coords, left, j)
        else:
            j += 1
            swapItem(ids, coords, j, right)

        if (j <= k):
            left = j + 1
        if (k <= j):
            right = j - 1


def swapItem(ids, coords, i, j):
    i = int(i)
    j = int(j)
    swap(ids, i, j)
    swap(coords, 2 * i, 2 * j)
    swap(coords, 2 * i + 1, 2 * j + 1)


def swap(arr, i, j):
    i = int(i)
    j = int(j)
    tmp = arr[i]
    arr[i] = arr[j]
    arr[j] = tmp


def kbWithin(ids, coords, qx, qy, r, nodeSize):
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

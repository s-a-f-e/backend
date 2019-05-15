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

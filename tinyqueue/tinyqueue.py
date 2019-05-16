def defaultCompare(a, b):
    if a < b:
        return -1
    if a > b:
        return 1
    return 0


class TinyQueue:
    def __init__(self, data=[], compare=defaultCompare):
        self.data = data
        self.length = len(data)
        self.compare = compare

        if (self.length > 0):
            for i in range((self.length >> 1) - 1, -1, -1):
                self._down(i)

    def length(self):
        return self.length

    def push(self, item):
        self.data.append(item)
        self.length += 1
        self._up(self.length - 1)

    def pop(self):
        if self.length == 0:
            return None
        top = self.data[0]
        bottom = self.data.pop()
        self.length -= 1

        if self.length > 0:
            self.data[0] = bottom
            self._down(0)

        return top

    def peek(self):
        return self.data[0]

    def _up(self, pos):
        data = self.data
        compare = self.compare
        item = data[pos]

        while (pos > 0):
            parent = (pos - 1) >> 1
            current = data[parent]
            if compare(item, current) >= 0:
                break
            data[pos] = current
            pos = parent

        data[pos] = item

    def _down(self, pos):
        data = self.data
        compare = self.compare
        halfLength = self.length >> 1
        item = data[pos]

        while (pos < halfLength):
            left = (pos << 1) + 1
            best = data[left]
            right = left + 1

            if right < self.length and compare(data[right], best) < 0:
                left = right
                best = data[right]

            if compare(best, item) >= 0:
                break

            data[pos] = best
            pos = left

        data[pos] = item

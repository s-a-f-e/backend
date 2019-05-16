import random
from tinyqueue import TinyQueue

# test
data = []
for i in range(0, 50):
    data.append(random.randint(0, 101))

sorted = sorted(data)

print("maintains priority queue")
queue = TinyQueue()
for i in range(0, len(data)):
    queue.push(data[i])

print(queue.peek() == sorted[0])

result = []
while queue.length > 0:
    result.append(queue.pop())

print(result == sorted)

print("accepts data in constructor")
queue = TinyQueue(data)

result = []
while (queue.length > 0):
    result.append(queue.pop())

print(result == sorted)

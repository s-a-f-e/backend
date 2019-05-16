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

if queue.peek() == sorted[0]:
    print("PASSED")
else:
    print("FAILED")

result = []
while queue.length > 0:
    result.append(queue.pop())

if result == sorted:
    print("PASSED")
else:
    print("FAILED")

print("accepts data in constructor")
queue = TinyQueue(data)

result = []
while (queue.length > 0):
    result.append(queue.pop())

if result == sorted:
    print("PASSED")
else:
    print("FAILED")


print('handles edge cases with few elements')
queue = TinyQueue()

queue.push(2)
queue.push(1)
queue.pop()
queue.pop()
queue.pop()
queue.push(2)
queue.push(1)
if queue.pop() == 1 and queue.pop() == 2 and queue.pop() == None:
    print("PASSED")
else:
    print("FAILED")

print('handles init with empty array')
queue = TinyQueue([])

if queue.data == []:
    print("PASSED")
else:
    print("FAILED")

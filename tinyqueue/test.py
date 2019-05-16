import random
from tinyqueue import TinyQueue
# test data

data = []
for i in range(0, 50):
    data.append(random.randint(0, 101))

sorted = sorted(data)
print(data)
print(sorted)

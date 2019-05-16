import json

# read file
f = open("./cities.json", "r")
# parse file
print("F", f)
cities = json.load(f)

print("# of cities", len(cities))
print(cities[0]["name"], "is at lat:", cities[0]
      ["lat"], "lon:", cities[0]["lon"])

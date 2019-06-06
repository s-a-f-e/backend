import random
import math
from .tinyqueue import TinyQueue

earthRadius = 6371.
rad = math.pi / 180.
# lower bound for distance from a location to points inside a bounding box


def boxDist(lng, lat, cosLat, node):
    minLng = node["minLng"]
    maxLng = node["maxLng"]
    minLat = node["minLat"]
    maxLat = node["maxLat"]
    # print("LNG", lng)
    # print("minLng", minLng)

    # query point is between minimum and maximum longitudes
    if (lng >= minLng and lng <= maxLng):
        if (lat < minLat):
            return haverSin((lat - minLat) * rad)
        if (lat > maxLat):
            return haverSin((lat - maxLat) * rad)
        return 0

    # query point is west or east of the bounding box
    # calculate the extremum for great circle distance from query point to the closest longitude
    haverSinDLng = min(haverSin((lng - minLng) * rad),
                       haverSin((lng - maxLng) * rad))
    extremumLat = vertexLat(lat, haverSinDLng)

    # if extremum is inside the box, return the distance to it
    if (extremumLat > minLat and extremumLat < maxLat):
        return haverSinDistPartial(haverSinDLng, cosLat, lat, extremumLat)

    # otherwise return the distan e to one of the bbox corners(whichever is closest)
    return min(
        haverSinDistPartial(haverSinDLng, cosLat, lat, minLat),
        haverSinDistPartial(haverSinDLng, cosLat, lat, maxLat)
    )


def compareDist(a, b):
    return a["dist"] - b["dist"]


def haverSin(theta):
    s = math.sin(theta / 2)
    return s * s


def haverSinDistPartial(haverSinDLng, cosLat1, lat1, lat2):
    return cosLat1 * math.cos(lat2 * rad) * haverSinDLng + haverSin((lat1 - lat2) * rad)


def haverSinDist(lng1, lat1, lng2, lat2, cosLat1):
    haverSinDLng = haverSin((lng1 - lng2) * rad)
    return haverSinDistPartial(haverSinDLng, cosLat1, lat1, lat2)


def distance(lng1, lat1, lng2, lat2):
    h = haverSinDist(lng1, lat1, lng2, lat2, math.cos(lat1 * rad))
    return 2 * earthRadius * math.asin(math.sqrt(h))


def vertexLat(lat, haverSinDLng):
    cosDLng = 1 - 2 * haverSinDLng
    if (cosDLng <= 0):
        # return lat > 0 if 90 else -90
        if lat > 0:
            return 90
        return -90
    return math.atan(math.tan(lat * rad) / cosDLng) / rad


def around(index, lng, lat, maxResults=None, maxDistance=None, predicate=None):
    maxHaverSinDist = 1
    result = []

    if (maxResults == None):
        maxResults = 999
    if (maxDistance != None):
        maxHaverSinDist = haverSin(maxDistance / earthRadius)

    # a distance-sorted priority queue that will contain both points and kd-tree nodes
    q = TinyQueue([], compareDist)

    # an object that represents the top kd-tree node(the whole Earth)
    node = {
        "left": 0,  # left index in the kd-tree array
        "right": len(index.ids) - 1,  # right index TODO
        "axis": 0,  # 0 for longitude axis and 1 for latitude axis
        "dist": 0,  # will hold the lower bound of children's distances to the query point
        "minLng": -180,  # bounding box of the node
        "minLat": -90,
        "maxLng": 180,
        "maxLat": 90
    }

    cosLat = math.cos(lat * rad)

    while (node):
        right = node["right"]
        left = node["left"]

        if (right - left <= index.nodeSize):  # leaf node
            # add all points of the leaf node to the queue
            for i in range(left, right + 1):
                item = index.points[index.ids[i]]
                if predicate == None or predicate(item):
                    q.push({"item": item, "dist": haverSinDist(
                        lng, lat, index.coords[2 * i], index.coords[2 * i + 1], cosLat)})
        else:  # not a leaf node (has child nodes)
            m = (left + right) >> 1  # middle index
            midLng = index.coords[2 * m]
            midLat = index.coords[2 * m + 1]

            # add middle point to the queue
            item = index.points[index.ids[m]]
            if predicate == None or predicate(item):
                q.push({"item": item, "dist": haverSinDist(
                    lng, lat, midLng, midLat, cosLat)})

            nextAxis = (node["axis"] + 1) % 2

            # first half of the node
            leftNode = {
                "left": left,
                "right": m - 1,
                "axis": nextAxis,
                "minLng": node["minLng"],
                "minLat": node["minLat"],
                # "maxLng": node["axis"] == 0 if midLng else node["maxLng"],
                # "maxLat": node["axis"] == 1 if midLat else node["maxLat"],
                "dist": 0
            }
            if node["axis"] == 0:
                leftNode["maxLng"] = midLng
            else:
                leftNode["maxLng"] = node["maxLng"]

            if node["axis"] == 1:
                leftNode["maxLat"] = midLat
            else:
                leftNode["maxLat"] = node["maxLat"]

            # second half of the node
            rightNode = {
                "left": m + 1,
                "right": right,
                "axis": nextAxis,
                # "minLng": node["axis"] == 0 if midLng else node["minLng"],
                # "minLat": node["axis"] == 1 if midLat else node["minLat"],
                "maxLng": node["maxLng"],
                "maxLat": node["maxLat"],
                "dist": 0
            }

            if node["axis"] == 0:
                rightNode["minLng"] = midLng
            else:
                rightNode["minLng"] = node["minLng"]

            if node["axis"] == 1:
                rightNode["minLat"] = midLat
            else:
                rightNode["minLat"] = node["minLat"]

            leftNode["dist"] = boxDist(lng, lat, cosLat, leftNode)
            rightNode["dist"] = boxDist(lng, lat, cosLat, rightNode)

            # add child nodes to the queue
            q.push(leftNode)
            q.push(rightNode)

        # fetch closest points from the queue; they're guaranteed to be closer
        # than all remaining points(both individual and those in kd-tree nodes),
        # since each node's distance is a lower bound of distances to its children
        while (q.length and q.peek()["item"]):
            # while (q.length > 0):
            candidate = q.pop()
            if (candidate["dist"] > maxHaverSinDist):
                print("RESULT", result)
                return result
            # try:
            result.append(candidate["item"])
            # except:
            # print("ERROR", len(result))
            if (len(result) == maxResults):
                print("RESULT", result)
                return result
        # while (q.length and q.peek()["item"]):
        #     candidate = q.pop()
        #     if (candidate["dist"] > maxHaverSinDist):
        #         return result
        #     result.append(candidate["item"])
        #     if (len(result) == maxResults):
        #         return result

        # the next closest kd-tree node
        node = q.pop()

    return result

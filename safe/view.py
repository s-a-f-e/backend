from people.models import Village, Mother, Driver
from django.http import JsonResponse, Http404
from decouple import config
from .geokdbush.geokdbush import around, distance
import requests
import json

FRONTLINE_KEY = config('FRONTLINESMS_SECRET')


def village(request, id):
    try:
        v_obj = Village.objects.get(pk=id)
        data = {
            'name': v_obj.name,
            'latitude': v_obj.latitude,
            'longitude': v_obj.longitude,
        }
    except Village.DoesNotExist:
        raise Http404("Village does not exist")
    return JsonResponse(data)


def mother(request, id):
    try:
        v_obj = Mother.objects.get(phone=id)
        mom_lat = v_obj.latitude
        mom_lon = v_obj.longitude
        # get all the drivers registered
        drivers = Driver.objects.values()
        # build the list of drivers
        driversLocList = []
        for d in drivers:
            if d["available"]:
                driversLocList.append({
                    "name": d["name"],
                    "phone": d["phone"],
                    "lat": d["latitude"],
                    "lon": d["longitude"]
                })

        momloc = {"lon": mom_lon, "lat": mom_lat}
        driversList = []
        for d in driversLocList:
            dist = distance(momloc["lon"], momloc["lat"], d["lon"], d["lat"])
            driversList.append((d["name"], d["phone"], dist))

        # time to sort the list - sort by 3rd item (distance)
        def getKey(item):
            return item[2]

        closestList = sorted(driversList, key=getKey)
        print("DONE", closestList)

        data = {
            'name': v_obj.name,
            'phone': v_obj.phone,
            'village': v_obj.village,
            'latitude': v_obj.latitude,
            'longitude': v_obj.longitude,
            "Drivers": closestList
        }

    except Mother.DoesNotExist:
        register_msg = "No entry found for " + id + \
            "\nPlease reply with 'village' and your village name.\nFor example, 'village Iganga'"
        url = 'https://cloud.frontlinesms.com/api/1/webhook'
        payload = {"apiKey": FRONTLINE_KEY, "payload": {
            "message": register_msg, "recipients": [{"type": "mobile", "value": id}]}}
        r = requests.post(url, data=json.dumps(payload))
        return JsonResponse({"data": register_msg})
        # raise Http404("Mother does not exist")

    # ping the SMS server with closest driver
    url = 'https://cloud.frontlinesms.com/api/1/webhook'
    pickup_msg = "Please pick up " + \
        data["name"] + " at " + data["village"] + \
        " village.\nReply with 'yes' if you are going."
    payload = {"apiKey": FRONTLINE_KEY, "payload": {"message": pickup_msg,
                                                    "recipients": [{"type": "mobile", "value": closestList[0][1]}]}}
    r = requests.post(url, data=json.dumps(payload))
    return JsonResponse(data)


def regMother(request, id):
    parsed = id.split('&')
    # see if village send via SMS is in the database
    try:
        villages = Village.objects.values()
        village = list(
            filter(lambda v: v["name"].lower() == parsed[1].lower(), villages))
    except:
        return JsonResponse({"msg": "village " + parsed[1] + " not found."})

    momObject = {
        "name": "entered via SMS",
        "phone": parsed[0],
        "village": village[0]["name"],
        "latitude": village[0]["latitude"],
        "longitude": village[0]["longitude"],
    }

    # enter this mom into database
    # try:
    query = Mother(name="entered via SMS", phone=parsed[0],
                   village=village[0]["name"],
                   latitude=village[0]["latitude"],
                   longitude=village[0]["longitude"],)
    query.save()
    # m_obj = Mother.objects.create(momObject)
    # print("Looks to have added mom", m_obj)
    # except:
    #     print("FAIL! adding mom to database")

    return JsonResponse(momObject)

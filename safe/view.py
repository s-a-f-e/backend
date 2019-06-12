from people.models import Village, Mother, Driver
from django.http import JsonResponse, Http404
from decouple import config
from .geokdbush.geokdbush import around, distance
import requests, json

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
        drivers =  Driver.objects.values()
        # build the list of drivers
        driversLocList = []
        for d in drivers:
            if d["available"]:
                driversLocList.append({
                    "name":d["name"],
                    "phone":d["phone"],
                    "lat":d["latitude"],
                    "lon":d["longitude"]
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
        msg = "No entry found for " + id
        data = {
            "msg": msg,
            "message": "Please text 11 to register"
        }
        return JsonResponse(data)
        # raise Http404("Mother does not exist")



    # ping the SMS server with closest driver
    url = 'https://cloud.frontlinesms.com/api/1/webhook'
    pickup_msg = "Please pick up " + data["name"] + " at " + data["village"] + " village.\nReply with 'yes' if you are going."
    payload = {"apiKey":FRONTLINE_KEY, "payload":{"message":pickup_msg, "recipients":[{ "type":"mobile", "value":closestList[0][1] }]}}
    r = requests.post(url, data=json.dumps(payload))
    return JsonResponse(data)

from people.models import Village, Mother, Driver, HealthCenter, MotherDriverConnection
from django.http import JsonResponse, Http404
from django.core import serializers
from decouple import config
from .geokdbush.geokdbush import around, distance
import requests
import json
import time

FRONTLINE_KEY = config('FRONTLINESMS_SECRET')
MASTER_PHONE = config('MASTER_PHONE')


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


def healthcenter(request, id):
    try:
        v_obj = HealthCenter.objects.get(pk=id)
        data = {
            'name': v_obj.name,
            'latitude': v_obj.latitude,
            'longitude': v_obj.longitude,
        }
    except HealthCenter.DoesNotExist:
        raise Http404("HealthCenter does not exist")
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
    print("MOTHER phone number", v_obj.phone)
    # Populate many-to-many table (MotherDriverConnection)
    MotherDriverConnection.objects.create(motherPhoneNumber=v_obj.phone, motherName=v_obj.name, motherVillage=v_obj.village, driverPhoneNumber=closestList[0][1], driverIsComing=False)

    # ping the SMS server with closest driver
    url = 'https://cloud.frontlinesms.com/api/1/webhook'
    pickup_msg = "Can you pick up a mother at "+ data["village"] + " village. " \
        "\nIf yes, reply with '1', if no, reply with '2'."
    payload = {"apiKey": FRONTLINE_KEY, "payload": {"message": pickup_msg,
                                                    "recipients": [{"type": "mobile", "value": closestList[0][1]}]}}
    r = requests.post(url, data=json.dumps(payload))
    return JsonResponse(data)


def regMother(request, id):
    parsed = id.split('&', 1)
    momPhone = parsed[0]
    momVillage = parsed[1]
    # see if village send via SMS is in the database
    villages = Village.objects.values()
    listVillages = list(villages)
    try:
        village = list(
            filter(lambda v: v["name"].lower() == momVillage.lower(), listVillages))
    except:
        print("NOT FOUND VILLAGE")
        return JsonResponse({"msg": "village " + momVillage + " not found."})

    momObject = {
        "name": "a mother",
        "phone": momPhone,
        "village": village[0]["name"],
        "latitude": village[0]["latitude"],
        "longitude": village[0]["longitude"],
    }

    # enter this mom into database
    try:
        query = Mother(name="mom", phone=momPhone,
                       village=village[0]["name"],
                       latitude=village[0]["latitude"],
                       longitude=village[0]["longitude"],)
        query.save()
    except:
        # ToDo: send a text to person monitoring the system
        return JsonResponse({"msg": "Error adding new mom to db"})

    url = 'https://cloud.frontlinesms.com/api/1/webhook'
    mom_msg = "You are registered. Please text 'driver' to request a pickup."
    payload = {"apiKey": FRONTLINE_KEY, "payload": {"message": mom_msg,
                                                    "recipients": [{"type": "mobile", "value": momPhone}]}}
    r = requests.post(url, data=json.dumps(payload))

    return JsonResponse(momObject)

def driverOnOffDuty(request, id, onDutyFlag):
    try:
        m_obj = MotherDriverConnection.objects.filter(driverPhoneNumber=id).values()
        json_res = []
        for key in m_obj:
            m_json = dict(key)
            json_res.append(m_json)

        if onDutyFlag == 1:
            Driver.objects.filter(phone=id).update(available = False)
            # build YES url to
            url = 'https://cloud.frontlinesms.com/api/1/webhook'
            pickup_msg = "Please pick up " + \
                json_res[0]["motherName"] + " at " + json_res[0]["motherVillage"] + \
                " village. Her number is " + \
                json_res[0]["motherPhoneNumber"] + "\nPlease text her to let her know you are on the way."
            payload = {"apiKey": FRONTLINE_KEY, "payload": {"message": pickup_msg,
                                                    "recipients": [{"type": "mobile", "value": json_res[0]["driverPhoneNumber"]}]}}
            r = requests.post(url, data=json.dumps(payload))
            # delete connection
            MotherDriverConnection.objects.filter(driverPhoneNumber=id).delete()
            return JsonResponse({"data": pickup_msg})

        if onDutyFlag == 2:
            flag = False
            Driver.objects.filter(phone=id).update(available = flag)
            # delete this connection
            MotherDriverConnection.objects.filter(driverPhoneNumber=id).delete()
            # API call here to get next driver/make new connection
            mother(request, json_res[0]["motherPhoneNumber"])

    except Driver.DoesNotExist:
        raise Http404("Driver does not exist")
    return JsonResponse({"Driver":"Successfully updated"})


def driverOnline(request, id, onlineFlag):
    try:
        if onlineFlag == "online":
            Driver.objects.filter(phone=id).update(available = True)
            # build online url
            url = 'https://cloud.frontlinesms.com/api/1/webhook'
            online_msg = "You are now online. Reply with 'offline' to go offline."
            payload = {"apiKey": FRONTLINE_KEY, "payload": {"message": online_msg,
                                                    "recipients": [{"type": "mobile", "value": id}]}}
            r = requests.post(url, data=json.dumps(payload))
            return JsonResponse({"data": online_msg})
        if onlineFlag == "offline":
            Driver.objects.filter(phone=id).update(available = False)
            #  build offline url
            url = 'https://cloud.frontlinesms.com/api/1/webhook'
            online_msg = "You are now offline. Reply with 'online' to go online."
            payload = {"apiKey": FRONTLINE_KEY, "payload": {"message": online_msg,
                                                    "recipients": [{"type": "mobile", "value": id}]}}
            r = requests.post(url, data=json.dumps(payload))
            return JsonResponse({"data": online_msg})
    except Driver.DoesNotExist:
        raise Http404("Driver does not exist")
        
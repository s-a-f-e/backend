from people.models import Village, Mother, Driver
from django.http import JsonResponse, Http404
# from kdBush.kdbush import KDBush
from .geokdbush.geokdbush import around, distance

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
        raise Http404("Mother does not exist")
    return JsonResponse(data)

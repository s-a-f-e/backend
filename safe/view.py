from people.models import Village, Mother, Driver
from django.http import JsonResponse, Http404

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
        data = {
            'name': v_obj.name,
            'phone': v_obj.phone,
            'village': v_obj.village,
            'latitude': v_obj.latitude,
            'longitude': v_obj.longitude,
        }
        mom_lat = v_obj.latitude
        mom_long = v_obj.longitude
        drivers =  Driver.objects.values()
        driversLocList = []
        for d in drivers:
            driversLocList.append({
                "name":d["name"],
                "lat":d["latitude"],
                "lon":d["longitude"]
            })
        print("driversLocList", driversLocList)

    except Mother.DoesNotExist:
        raise Http404("Mother does not exist")
    return JsonResponse(data)

from people.models import Village
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

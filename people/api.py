from rest_framework import serializers  # for which fields
from rest_framework import viewsets  # for which rows
from .models import Driver, Mother


# get our model and fields
class DriverSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Driver
        fields = ('name', 'phone', 'homebase',
                  'latitude', 'longitude', 'available')


class DriverViewSet(viewsets.ModelViewSet):
    serializer_class = DriverSerializer
    queryset = Driver.objects.none()

    def get_queryset(self):
        user = self.request.user

        if user.is_anonymous:
            return Driver.objects.none()  # is none, but of PersonalNote `type`
        else:
            return Driver.objects.all()


class MotherSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Mother
        fields = ('name', 'phone', 'village', 'latitude', 'longitude')


class MotherViewSet(viewsets.ModelViewSet):
    serializer_class = MotherSerializer
    queryset = Driver.objects.none()

    def get_queryset(self):
        user = self.request.user

        if user.is_anonymous:
            return Mother.objects.none()  # is none, but of PersonalNote `type`
        else:
            return Mother.objects.all()

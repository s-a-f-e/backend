from rest_framework import serializers  # for which fields
from rest_framework import viewsets  # for which rows
from .models import Driver, Mother, Village, Midwife, HealthCenter


# get our model and fields
class DriverSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Driver
        fields = ('id', 'name', 'phone', 'latitude', 'longitude', 'available')


class DriverViewSet(viewsets.ModelViewSet):
    serializer_class = DriverSerializer
    queryset = Driver.objects.none()

    def get_queryset(self):
        """
        This view returns a list of all the drivers registered
        """
        user = self.request.user

        if user.is_anonymous:  # that is, not logged in
            return Driver.objects.none()
        else:
            return Driver.objects.all()


class MotherSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Mother
        fields = ('id', 'name', 'phone', 'village', 'hasComplications', 'dueMonth',
                  'dueYear', 'latitude', 'longitude')


class MotherViewSet(viewsets.ModelViewSet):
    serializer_class = MotherSerializer
    queryset = Mother.objects.none()

    def get_queryset(self):
        """
        This view returns a list of all the mothers registered
        """
        user = self.request.user

        if user.is_anonymous:  # that is, not logged in
            return Mother.objects.none()
        else:
            return Mother.objects.all()


class VillageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Village
        fields = ('id', 'name', 'latitude', 'longitude')


class VillagesViewSet(viewsets.ModelViewSet):
    serializer_class = VillageSerializer
    queryset = Village.objects.none()

    def get_queryset(self):
        """
        This view returns a list of all the villages entered
        """
        user = self.request.user

        if user.is_anonymous:  # that is, not logged in
            return Village.objects.none()
        else:
            return Village.objects.all()


class HealthCenterSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = HealthCenter
        fields = ('id', 'name', 'latitude', 'longitude')


class HealthCentersViewSet(viewsets.ModelViewSet):
    serializer_class = HealthCenterSerializer
    queryset = HealthCenter.objects.none()

    def get_queryset(self):
        """
        This view returns a list of all the HealthCenters entered
        """
        user = self.request.user

        if user.is_anonymous:  # that is, not logged in
            return HealthCenter.objects.none()
        else:
            return HealthCenter.objects.all()


class MidwifeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Midwife
        fields = ('id', 'name', 'healthcenter', 'latitude', 'longitude')


class MidwifeViewSet(viewsets.ModelViewSet):
    serializer_class = MidwifeSerializer
    queryset = Midwife.objects.none()

    def get_queryset(self):
        """
        This view returns a list of all the HealthCenters entered
        """
        user = self.request.user

        if user.is_anonymous:  # that is, not logged in
            return Midwife.objects.none()
        else:
            return Midwife.objects.all()

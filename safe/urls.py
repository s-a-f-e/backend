"""safe URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from rest_framework import routers
from people.api import DriverViewSet, MotherViewSet, VillagesViewSet, HealthCentersViewSet, MidwifeViewSet

from rest_framework.authtoken import views
from django.views.generic import TemplateView
from . import view

router = routers.DefaultRouter()
router.register('drivers', DriverViewSet)
router.register('mothers', MotherViewSet)
router.register('midwives', MidwifeViewSet)
router.register('villages', VillagesViewSet)
router.register('healthcenters', HealthCentersViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-token-auth/', views.obtain_auth_token),
    path('api/village/<int:id>/', view.village),
    path('api/healthcenter/<int:id>/', view.healthcenter),
    path('api/mother/<str:id>/', view.mother),
    path('api/toggledriveroff/<str:id>/<int:onDutyFlag>/', view.driverOnOffDuty),
    path('api/driveronline/<str:id>/<str:onlineFlag>/', view.driverOnline),
    path('api/registermother/<str:id>/', view.regMother),
    path('', TemplateView.as_view(template_name="index.html")),
]

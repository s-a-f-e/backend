from django.db import models
# from uuid import uuid4
# from phonenumber_field.modelfields import PhoneNumberField
# from phonenumber_field.phonenumber import PhoneNumber

from django.contrib.auth.models import User


class Person(models.Model):
    # id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=50, blank=False)
    phone = models.CharField(max_length=20, blank=False, unique=True)
    # phone = PhoneNumberField(null=False, blank=False, unique=True)
    # phone = PhoneNumber.from_string(phone_number=raw_phone, region='RU').as_e164

    longitude = models.FloatField()
    latitude = models.FloatField()

    # when added
    created_at = models.DateTimeField(auto_now_add=True)
    # when added or modified
    last_modified = models.DateTimeField(auto_now=True)


class Driver(Person):
    available = models.BooleanField()


class Mother(Person):
    village = models.CharField(max_length=50, blank=False)


class Village(models.Model):
    name = models.CharField(max_length=50, blank=False)
    longitude = models.FloatField()
    latitude = models.FloatField()


class HealthCenter(models.Model):
    name = models.CharField(max_length=50, blank=False)
    longitude = models.FloatField()
    latitude = models.FloatField()

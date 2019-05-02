from django.contrib import admin
from .models import Driver, Mother


class PersonAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'last_modified')


# Register your models here.
admin.site.register(Mother)
admin.site.register(Driver)

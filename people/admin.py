from django.contrib import admin
from .models import Driver, Mother, Village


class PersonAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'last_modified')


# Register your models here.
admin.site.register(Mother, PersonAdmin)
admin.site.register(Driver, PersonAdmin)
admin.site.register(Village)

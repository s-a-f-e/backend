from django.contrib import admin
from .models import Driver, Mother, Village, HealthCenter
from django.http import HttpResponse
import csv


class PersonAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'last_modified')
    actions = ["export_as_csv"]

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(
            meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field)
                                   for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"


# Register your models here.
admin.site.register(Mother, PersonAdmin)
admin.site.register(Driver, PersonAdmin)
admin.site.register(Village)
admin.site.register(HealthCenter)

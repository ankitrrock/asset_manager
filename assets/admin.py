from django.contrib import admin
from .models import Asset, Notification, Violation


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ("name", "service_time", "expiration_time", "is_serviced")
    list_filter = ("is_serviced",)
    search_fields = ("name",)


admin.site.register(Notification)
admin.site.register(Violation)

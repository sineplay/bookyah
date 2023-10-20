from django.contrib import admin
from .models import AssetType, Asset, Reservation

# Register your models here.
admin.site.register(AssetType)
admin.site.register(Asset)
admin.site.register(Reservation)

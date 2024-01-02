from django.contrib import admin
from .models import AssetType, Asset, Reservation

@admin.register(AssetType)
class AssetTypeAdmin(admin.ModelAdmin):
	list_display = ('name', 'fa_icon')
	search_fields = ('name',)

# Register your models here.
admin.site.register(Asset)
admin.site.register(Reservation)

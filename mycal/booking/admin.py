from django.contrib import admin
from .models import AssetType, Asset, Reservation
from django.urls import reverse
from django.utils.html import format_html

@admin.register(AssetType)
class AssetTypeAdmin(admin.ModelAdmin):
	list_display = ('name', 'fa_icon')
	search_fields = ('name',)

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
	list_display = ('asset', 'start_time', 'end_time', 'user', 'series_actions')
	
	def series_actions(self, obj):
		if obj.series_id:
			return format_html(
				'<a href="{}">View Series</a>',
				reverse('view_series', args=[obj.series_id])
			)
		return "N/A"
	series_actions.short_description = 'Series Actions'

# Register your models here.
admin.site.register(Asset)
#admin.site.register(Reservation)

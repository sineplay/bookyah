from typing import Any
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import AssetType, Asset, CustomUser, Reservation
from .resources import AssetTypeResource, AssetResource, ReservationResource
from django.urls import reverse
from django.utils import timezone
from django.utils.html import format_html
from .utils import send_reservation_notification

@admin.register(AssetType)
class AssetTypeAdmin(ImportExportModelAdmin, admin.ModelAdmin):
	list_display = ('name', 'fa_icon')
	search_fields = ('name',)
	resource_class = AssetTypeResource

@admin.register(Asset)
class AssetAdmin(ImportExportModelAdmin):
	resource_class = AssetResource

@admin.register(Reservation)
class ReservationAdmin(ImportExportModelAdmin, admin.ModelAdmin):
	list_display = ('asset', 'start_time', 'end_time', 'user', 'series_actions')
	resource_class = ReservationResource
	
	def series_actions(self, obj):
		if obj.series_id:
			return format_html(
				'<a href="{}">View Series</a>',
				reverse('view_series', args=[obj.series_id])
			)
		return "N/A"
	series_actions.short_description = 'Series Actions'

	def save_model(self, request, obj, form, change):
		super().save_model(request, obj, form, change)
		print("Was the reservation changed? ", change)
		if change:
			send_reservation_notification(request, obj.user, obj, 'modified')
	
	def delete_model(self, request, obj):
		if obj.start_time > timezone.now():
			send_reservation_notification(request, obj.user, obj, 'deleted')
		super().delete_model(request, obj)

# Register your models here.
# admin.site.register(Asset)
# admin.site.register(Reservation)

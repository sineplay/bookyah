from import_export import widgets, resources, fields
from import_export.admin import ImportExportModelAdmin
from .models import AssetType, Asset, Reservation

class AssetTypeResource(resources.ModelResource):
	class Meta:
		model = AssetType

class AssetResource(resources.ModelResource):
	class Meta:
		model = Asset

class NullableUUIDWidget(widgets.UUIDWidget):
	def clean(self, value, row=None, *args, **kwargs):
		if value in ('None', ''):
			return None
		return super().clean(value, row=row, *args, **kwargs)

class ReservationResource(resources.ModelResource):
    series_id = fields.Field(
		column_name='series_id',
		attribute='series_id',
		widget=NullableUUIDWidget(),
    )
	
    class Meta:
        model = Reservation
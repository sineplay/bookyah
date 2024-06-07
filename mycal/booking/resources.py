from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import AssetType, Asset, Reservation

class AssetTypeResource(resources.ModelResource):
	class Meta:
		model = AssetType

class AssetResource(resources.ModelResource):
	class Meta:
		model = Asset

class ReservationResource(resources.ModelResource):
    class Meta:
        model = Reservation
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import CustomUser

class CustomUserResource(resources.ModelResource):
	class Meta:
		model = CustomUser
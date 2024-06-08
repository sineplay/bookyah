# BOOKYAH - Asset Reservation Application
# Copyright (C) 2024 Sineplay Studio, LLC
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# The LICENSE file describes the conditions under which this software
# may be distributed.

from import_export import widgets, resources, fields
from import_export.admin import ImportExportModelAdmin
from .models import AssetType, Asset, Reservation

class AssetTypeResource(resources.ModelResource):
	class Meta:
		model = AssetType

class AssetResource(resources.ModelResource):
	class Meta:
		model = Asset

class NullableUUIDWidget(widgets.CharWidget):
	def clean(self, value, row=None, *args, **kwargs):
		if value in ('None', '', 'null'):
			return None
		return value

class ReservationResource(resources.ModelResource):
    series_id = fields.Field(
		column_name='series_id',
		attribute='series_id',
		widget=NullableUUIDWidget(),
    )
	
    class Meta:
        model = Reservation
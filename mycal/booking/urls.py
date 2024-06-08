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

from django.urls import path
from . import views

urlpatterns = [
	path('select-asset-type/', views.select_asset_type, name='select-asset-type'),
	path('reserve/asset/<int:asset_type_id>/', views.create_reservation, name='create-reservation'),
	path('reserve/success/', views.reserve_success, name='reserve-success'),
	path('admin-calendar/', views.admin_calendar_view, name='admin_calendar'),
	path('admin/reservation_series/<uuid:series_id>/', views.view_series, name='view_series'),
	path('admin/delete_series/<uuid:series_id>/', views.delete_series, name='delete_series'),
]
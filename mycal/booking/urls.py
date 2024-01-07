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
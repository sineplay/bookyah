from django.urls import path
from . import views

urlpatterns = [
	path('select-asset-type/', views.select_asset_type, name='select-asset-type'),
	path('reserve/asset/<int:asset_type_id>/', views.create_reservation, name='create-reservation'),
	path('reserve/success/', views.reserve_success, name='reserve-success'),
]
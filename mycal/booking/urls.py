from django.urls import path
from . import views

urlpatterns = [
	path('reserve/', views.create_reservation, name='create-reservation'),
	path('reserve/success/', views.reserve_success, name='reserve-success'),
]
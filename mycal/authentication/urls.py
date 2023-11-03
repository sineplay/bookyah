from django.urls import path, include
from .views import RegisterView, profile_view, update_profile, archived_reservations_view, modify_reservation_view, cancel_reservation_view

urlpatterns = [
	path('register/', RegisterView.as_view(), name='register'),
	path('profile/', profile_view, name='profile'),
	path('profile/archived/', archived_reservations_view, name='archived_reservations'),
	path('profile/update/', update_profile, name='update_profile'),
	path('accounts/', include('django.contrib.auth.urls')),
	path('reservation/modify/<int:pk>/', modify_reservation_view, name='modify_reservation'),
	path('reservation/cancel/<int:pk>/', cancel_reservation_view, name='cancel_reservation'),
]
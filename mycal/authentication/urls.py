from django.urls import path, include
from .views import RegisterView, profile_view, update_profile

urlpatterns = [
	path('register/', RegisterView.as_view(), name='register'),
	path('profile/', profile_view, name='profile'),
	path('profile/update/', update_profile, name='update_profile'),
	path('accounts/', include('django.contrib.auth.urls')),
]
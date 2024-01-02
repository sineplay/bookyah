"""
URL configuration for mycal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic.base import RedirectView
from authentication.views import root_redirect
from booking import views


urlpatterns = [

	# Redirect /auth/ to /auth/profile/
	re_path(r'^auth/$', RedirectView.as_view(url='/auth/profile/', permanent=True)),
	
	# Redirect /auth/ to /auth/profile/
	re_path(r'^booking/$', RedirectView.as_view(url='/booking/select-asset-type/', permanent=True)),
    
	path('', root_redirect, name='root_redirect'),
    path('admin/', admin.site.urls),
	path('booking/', include('booking.urls')),
	path('accounts/', include('django.contrib.auth.urls')),
	path('auth/', include('authentication.urls')),
	path('reservation-data/', views.reservation_data, name='reservation_data'),
	path('admin-reservation-data/', views.admin_reservation_data, name='admin_reservation_data'),
]

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

from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import RegisterView, profile_view, update_profile, archived_reservations_view, modify_reservation_view, cancel_reservation_view, cancel_series_view, verify_email, resend_verification_email, verify_email_reminder

urlpatterns = [
	path('register/', RegisterView.as_view(), name='register'),
	path('profile/', profile_view, name='profile'),
	path('profile/archived/', archived_reservations_view, name='archived_reservations'),
	path('profile/update/', update_profile, name='update_profile'),
	# path('accounts/', include('django.contrib.auth.urls')),
	path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
	path('accounts/logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
	path('reservation/modify/<int:pk>/', modify_reservation_view, name='modify_reservation'),
	path('reservation/cancel/<int:pk>/', cancel_reservation_view, name='cancel_reservation'),
	path('reservation/cancel_series/<uuid:series_id>/', cancel_series_view, name='cancel_series'),
	path('resend-verification-email/', resend_verification_email, name='resend_verification_email'),
	path('verify-email/', verify_email, name='verify_email'),
	path('verify-email-reminder/', verify_email_reminder, name='verify_email_reminder'),
]
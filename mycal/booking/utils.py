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

from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse

def send_reservation_notification(request, user, reservation, action):
    profile_path = reverse('profile')
    profile_url = request.build_absolute_uri(profile_path)
    subject = f'Your reservation has been {action} - BOOKYAH'
    message = f'Dear {user.first_name},\n\n'
    message += f'Your reservation for {reservation.asset.name} starting at '
    message += f'{reservation.start_time.strftime("%Y-%m-%d %H:%M")} has been {action} by an admin.\n\n'
    message += f'Please contact us with any concerns.\n\n'
    message += f'To view your current reservations, visit your profile: {profile_url}'
    
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )
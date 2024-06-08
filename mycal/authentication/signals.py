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

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.core.signing import Signer
from django.conf import settings
from .models import CustomUser
signer = Signer()

@receiver(post_save, sender=CustomUser)
def send_welcome_email(sender, instance, created, **kwargs):
	if created: # Only send emails upon creation, not every save
		token = signer.sign(instance.pk)
		verification_url = f"http://localhost:8000/auth/verify-email/?token={token}"
		message = (
			f"Hello {instance.first_name}, welcome to BOOKYAH! Your"
			f"account has been created successfully.\n\n"
			f"Please verify your email using the link below:\n"
			f"{verification_url}\n\n"
			f"Regards,\n"
			f"BOOKYAH"
		)
		send_mail(
			'Welcome to BOOKYAH - Verify your email',
			message,
			settings.DEFAULT_FROM_EMAIL,
			[instance.email],
			fail_silently=False,
		)
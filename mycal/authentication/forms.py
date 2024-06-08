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

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from .models import AllowedEmailDomain, AppSetting, CustomUser

class CustomUserCreationForm(UserCreationForm):
	email = forms.EmailField(max_length=255, help_text='Required. Add a valid email address.')
	class Meta(UserCreationForm.Meta):
		model = CustomUser
		fields = ('email', 'first_name', 'last_name') # Specifying fields from CustomUser
	
	def clean_email(self):
		email = self.cleaned_data.get('email')
		try:
			settings = AppSetting.objects.get()
			if settings.restrict_email_domain:
				domain = email.split('@')[-1]
				if not AllowedEmailDomain.objects.filter(domain=domain).exists():
					raise ValidationError(f"Registration with the domain '{domain}' is not allowed.")
		except AppSetting.DoesNotExist:
			pass
		return email
	
class CustomUserChangeForm(UserChangeForm):
	class Meta(UserChangeForm.Meta):
		model = CustomUser
		fields = ('first_name', 'last_name', 'email')
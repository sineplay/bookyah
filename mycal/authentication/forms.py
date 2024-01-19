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
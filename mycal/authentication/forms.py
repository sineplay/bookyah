from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
	class Meta(UserCreationForm.Meta):
		model = CustomUser
		fields = ('email', 'first_name', 'last_name') # Specifying fields from CustomUser
	
	email = forms.EmailField(max_length=255, help_text='Required. Add a valid email address.')
	
class CustomUserChangeForm(UserChangeForm):
	class Meta(UserChangeForm.Meta):
		model = CustomUser
		fields = ('first_name', 'last_name', 'email')
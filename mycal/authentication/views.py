from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from .forms import CustomUserCreationForm, CustomUserChangeForm
from booking.models import Reservation

# Create your views here.
class RegisterView(generic.CreateView):
	form_class = CustomUserCreationForm
	success_url = reverse_lazy('login')
	template_name = 'registration/register.html'
	
@login_required
def profile_view(request):
	# Get the current user's reservations
	reservations = Reservation.objects.filter(user=request.user)
	
	context = {
		'reservations': reservations,
	}
	
	return render(request, 'authentication/profile.html', context)
	
@login_required
def update_profile(request):
	if request.method == 'POST':
		form = CustomUserChangeForm(request.POST, instance=request.user)
		
		if form.is_valid():
			form.save()
			messages.success(request, 'Your profile was successfully updated!')
			return redirect('profile')
	else:
		form = CustomUserChangeForm(instance=request.user)
	
	return render(request, 'authentication/update_profile.html', {'form': form})
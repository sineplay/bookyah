from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.utils import timezone
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
	current_time = timezone.now()
	
	# Get the current user's reservations
	active_reservations = Reservation.objects.filter(
		user=request.user, end_time__gte=current_time, start_time__lte=current_time
	)
	
	upcoming_reservations = Reservation.objects.filter(
		user=request.user, start_time__gt=current_time
	)
	# Archived reservations will be handled in a separate view
	
	context = {
		'active_reservations': active_reservations,
		'upcoming_reservations': upcoming_reservations,
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
	
@login_required
def modify_reservation_view(request, pk):
	# Placeholder view function; you will need to implement the logic to modify a reservation
	return HttpResponse("This will be the reservation modification page.")

@login_required
def cancel_reservation_view(request, pk):
	reservation = get_object_or_404(Reservation, pk=pk, user=request.user)
	if reservation.can_be_cancelled():
		reservation.cancel()
		messages.success(request, "Your reservation has been cancelled.")
		return redirect('profile')
	else:
		messages.error(request, "This reservation cannot be cancelled.")
		return redirect('profile')

@login_required
def archived_reservations_view(request):
	current_time = timezone.now()
	archived_reservations = Reservation.objects.filter(
		user=request.user, end_time__lt=current_time
	)
	
	return render(request, 'authentication/archived_reservations.html', {'archived_reservations': archived_reservations})
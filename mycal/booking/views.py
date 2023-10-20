from django.shortcuts import render, redirect
from .forms import ReservationForm
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def create_reservation(request):
	if request.method == 'POST':
		form = ReservationForm(request.POST)
		if form.is_valid():
			reservation = form.save(commit=False)
			reservation.user = request.user
			reservation.save()
			return redirect('reserve-success')
	else:
		form = ReservationForm()
		
	return render(request, 'reserve_template.html', {'form': form})

def reserve_success(request):
	return render(request, 'reserve_success.html', {})
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import ReservationForm
from django.contrib.auth.decorators import login_required
from .models import Asset, Reservation

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
		form.fields['asset'].queryset = Asset.objects.none()
		
	return render(request, 'booking/reserve_template.html', {'form': form})

def reserve_success(request):
	return render(request, 'booking/reserve_success.html', {})
	
def get_assets_for_type(reqeust, type_id):
	assets = Asset.objects.filter(asset_type_id=type_id).values('id', 'name')
	return JsonResponse({'assets': list(assets)})
	
def reservation_data(request):
	asset_id = request.GET.get('asset_id')
	
	if asset_id:
		reservations = Reservation.objects.filter(asset_id=asset_id)
	else:
		reservations = Reservation.objects.all()
	
	reservation_data = [{
		'title': reservation.asset.name,
		'start': reservation.start_time.isoformat(),
		'end': reservation.end_time.isoformat(),
		# More fields as required by FullCalendar
	} for reservation in reservations]

	return JsonResponse(reservation_data, safe=False)

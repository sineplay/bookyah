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
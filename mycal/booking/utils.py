from django.core.mail import send_mail
from django.conf import settings

def send_reservation_notification(user, reservation, action):
    subject = 'Reservation Update Notification - BOOKYAH'
    message = f'Dear {user.first_name},\n\n'
    message += f'Your reservation for {reservation.asset.name} has been {action} by an admin.\n\n'
    message += f'Please contact us with any concerns.'
    
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )
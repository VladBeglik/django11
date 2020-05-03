from django.core.mail import send_mail


def send(user_email):
    send_mail('notes',
              'hi',
              'vladbeglik@gmail.com',
              [user_email],
              fail_silently=False,
    )
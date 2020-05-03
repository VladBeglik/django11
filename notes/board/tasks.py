from django.core.mail import send_mail
from notes.celery import app
from .service import send
from django.contrib.auth import models


@app.task
def send_spam_email(user_email):
    send(user_email)


@app.task
def send_beat_email():
    for user in models.User.objects.all():
        send_mail(
            'уведомление',
            'вам будут приходить уведомления',
            'vladbeglik@gmail.com',
            [user.email],
            fail_silently=False,
        )

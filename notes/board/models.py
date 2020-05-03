from django import urls
from django.db import models
from django.conf import settings


class Note(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    created = models.DateField(auto_now=True)
    deadline = models.DateField(blank=True)
    user_notes = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='users_project',
        on_delete=models.CASCADE,
    )

    # def get_absolute_url(self):
    #     return urls.reverse('note-list', args=[str(self.id)])

    def __str__(self):
        return self.name
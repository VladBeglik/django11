import json
from django import urls
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from webpush import send_user_notification
from django.contrib.auth import models as auth_model
from board import models, forms
from board.service import send
from .tasks import send_spam_email

class NoteList(LoginRequiredMixin, generic.ListView):
    model = models.Note
    template_name = 'products.html'

    def get_queryset(self):
        user = self.request.user
        return user.users_project.all()


class NoteCreateView(LoginRequiredMixin, generic.CreateView):
    model = models.Note
    fields = [
        'name',
        'description',
        'deadline',
        'user_notes'
    ]
    template_name = 'create.html'
    success_url = '/notes'


class NoteDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = models.Note
    template_name = 'delete.html'
    success_url = urls.reverse_lazy('note-list')


class NoteUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = models.Note
    fields = [
        'name',
        'description',
        'deadline',
    ]
    template_name = 'order_form.html'
    success_url = '/notes'


class NotificationView(generic.CreateView):
    form_class = forms.ContactForm
    template_name = 'email.html'
    success_url = '/notes'

    def form_valid(self, form):
        form.save()
        send_spam_email.delay(form.instance.email)
        return super().form_valid(form)

@require_GET
def webpush(request):
   webpush_settings = getattr(settings, 'WEBPUSH_SETTINGS', {})
   vapid_key = webpush_settings.get('VAPID_PUBLIC_KEY')
   user = request.user
   return render(request, 'webpush.html', {user: user, 'vapid_key': vapid_key})


@require_POST
@csrf_exempt
def send_push(request):
    try:
        body = request.body
        data = json.loads(body)

        if 'head' not in data or 'body' not in data or 'id' not in data:
            return JsonResponse(status=400, data={"message": "Invalid data format"})

        user_id = data['id']
        user = get_object_or_404(User, pk=user_id)
        payload = {'head': data['head'], 'body': data['body']}
        send_user_notification(user=user, payload=payload, ttl=1000)

        return JsonResponse(status=200, data={"message": "Web push successful"})
    except TypeError:
        return JsonResponse(status=500, data={"message": "An error occurred"})





from django.contrib import admin
from django.urls import path, include
from board import views
from authentication import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path(
        'admin/',
        admin.site.urls
    ),
    #authentication
    path(
        'login/',
        auth_views.LoginView.as_view(),
        name='login',
    ),
    path(
        'logout/',
        auth_views.LogoutView.as_view(),
        name='logout',
    ),
    path(
        'signup/',
        auth_views.UserCreate.as_view(),
        name='sign-up'
    ),
    #notes
    path(
        'notes/',
        views.NoteList.as_view(),
        name='note-list'

    ),
    path(
        'notes/<str:pk>/update',
        views.NoteUpdateView.as_view(),
        name='note-update'
    ),
    path(
        'notes/<str:pk>/delete',
        views.NoteDeleteView.as_view(),
        name='note-delete'
    ),
    path(
        'notes/create',
        views.NoteCreateView.as_view(),
        name='create'
    ),
    path(
        'notes/email',
        views.NotificationView.as_view(),
        name='email'
    ),
    #wedpush
    path(
        'send_push',
        views.send_push,
    ),
    path(
        'webpush/',
        include('webpush.urls')
    ),
    path(
        'web',
        views.webpush,
    ),
    path(
        'sw.js',
        TemplateView.as_view(template_name='sv.js', content_type='application/x-javascript')
    )
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

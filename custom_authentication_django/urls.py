from django.contrib import admin
from django.urls import path

from user import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        'signin/',
        views.SigninView.as_view(),
        name='signin'
    ),
    path(
        'signup/',
        views.SignupView.as_view(),
        name='signup'
    ),
    path(
        'me/',
        views.MeView.as_view(),
        name='me'
    )
]

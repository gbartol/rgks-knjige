from django.urls import path

from . import views


urlpatterns = [
    # Ovdje dodajemo url-ove kada napravimo neku rutu
    path('profile/me/', views.my_profile, name='my-profile'),
]

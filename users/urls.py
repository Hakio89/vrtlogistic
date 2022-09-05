from django.urls import path
from . import views

urlpatterns = [
    path("users/login/", views.user_login, name="user_login"),
    path("users/registration/", views.user_registration, name="user_registration"),
    path("users/logout/", views.user_logout, name="user_logout"),
    path("users/profile/", views.user_profile, name="user_profile"),
]
from django.urls import path
from . import views

urlpatterns = [
    path("xiaomi/", views.xiaomi, name="xiaomi"),
    path("xiaomi/delivery/", views.delivery, name="delivery"),
    path("xiaomi/deliveries/", views.deliveries, name="deliveries"),
    path("xiaomi/parts/", views.parts, name="parts"),
    path("xiaomi/claims/", views.claims, name="claims"),
    path("xiaomi/waiting/", views.waiting, name="waiting"),
]
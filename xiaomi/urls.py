from django.urls import path
from . import views

urlpatterns = [
    path("xiaomi/", views.xiaomi, name="xiaomi"),
    path("xiaomi/delivery/", views.delivery, name="xiaomi-delivery"),
    path("xiaomi/deliveries", views.deliveries, name="xiaomi-deliveries"),
    path("xiaomi/parts/", views.parts, name="xiaomi-parts"),
    path("xiaomi/claims", views.claims, name="xiaomi-claims"),
    path("xiaomi/waiting", views.waiting, name="xiaomi-waiting"),
    path("xiaomi/prices", views.prices, name="xiaomi-prices"),
]
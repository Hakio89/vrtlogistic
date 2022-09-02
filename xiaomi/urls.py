from django.urls import path
from . import views

urlpatterns = [
    path("xiaomi/", views.xiaomi, name="xiaomi"),
    path("xiaomi/delivery/", views.delivery, name="xiaomi_delivery"),
    path("xiaomi/deliveries", views.deliveries, name="xiaomi_deliveries"),
    path("xiaomi/parts/", views.parts, name="xiaomi_parts"),
    path("xiaomi/claims", views.claims, name="xiaomi_claims"),
    path("xiaomi/waiting", views.waiting, name="xiaomi_waiting"),
    path("xiaomi/prices", views.prices, name="xiaomi_prices"),
]
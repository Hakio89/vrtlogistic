from urllib import request
from django.urls import path
from . import views

urlpatterns = [
    path("alcatel/", views.alcatel, name="alcatel"),
    path("alcatel/delivery/", views.delivery, name="alcatel_delivery"),
    path("alcatel/deliveries/", views.deliveries, name="alcatel_deliveries"),
    path("alcatel/parts/", views.parts, name="alcatel_parts"),
    path("alcatel/claims/", views.claims, name="alcatel_claims"),
    path("alcatel/waiting/", views.waiting, name="alcatel_waiting"),
    path("alcatel/prices/", views.prices, name="alcatel_prices"),
  ]
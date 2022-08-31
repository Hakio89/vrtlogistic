from urllib import request
from django.urls import path
from . import views

urlpatterns = [
    path("alcatel/", views.alcatel, name="alcatel"),
    path("alcatel/delivery/", views.delivery, name="alcatel-delivery"),
    path("alcatel/deliveries/", views.deliveries, name="alcatel-deliveries"),
    path("alcatel/parts/", views.parts, name="alcatel-parts"),
    path("alcatel/claims/", views.claims, name="alcatel-claims"),
    path("alcatel/waiting/", views.waiting, name="alcatel-waiting"),
    path("alcatel/prices/", views.prices, name="alcatel-prices"),
  ]
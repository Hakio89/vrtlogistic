from urllib import request
from django.urls import path
from . import views

urlpatterns = [
    path("alcatel/", views.AlcatelView.as_view(), name="alcatel"),
    path("alcatel/delivery/", views.AlcatelView.as_view(), name="alcatel_delivery"),
    path("alcatel/deliveries/", views.AlcatelView.as_view(), name="alcatel_deliveries"),
    path("alcatel/parts/", views.AlcatelView.as_view(), name="alcatel_parts"),
    path("alcatel/claims/", views.AlcatelView.as_view(), name="alcatel_claims"),
    path("alcatel/waiting/", views.AlcatelView.as_view(), name="alcatel_waiting"),
    path("alcatel/prices/", views.AlcatelView.as_view(), name="alcatel_prices"),
  ]
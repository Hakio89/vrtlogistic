from django.urls import path
from . import views

urlpatterns = [
  path("cat/", views.cat, name="cat"),
  path("cat/delivery/", views.delivery, name="cat_delivery"),
  path("cat/deliveries/", views.deliveries, name="cat_deliveries"),
  path("cat/parts/", views.parts, name="cat_parts"),
  path("cat/claims/", views.claims, name="cat_claims"),
  path("cat/waiting/", views.waiting, name="cat_waiting"),
  path("cat/prices/", views.prices, name="cat_prices"),
  
]
from django.urls import path
from . import views

urlpatterns = [
  path("cat/", views.cat, name="cat"),
  path("cat/delivery/", views.delivery, name="cat-delivery"),
  path("cat/deliveries/", views.deliveries, name="cat-deliveries"),
  path("cat/parts/", views.parts, name="cat-parts"),
  path("cat/claims/", views.claims, name="cat-claims"),
  path("cat/waiting/", views.waiting, name="cat-waiting"),
  path("cat/prices/", views.prices, name="cat-prices"),
  
]
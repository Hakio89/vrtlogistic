from django.urls import path
from . import views

urlpatterns = [
  path("cat/", views.CatView.as_view(), name="cat"),
  path("cat/delivery/", views.CatView.as_view(), name="cat_delivery"),
  path("cat/deliveries/", views.CatView.as_view(), name="cat_deliveries"),
  path("cat/parts/", views.CatView.as_view(), name="cat_parts"),
  path("cat/claims/", views.CatView.as_view(), name="cat_claims"),
  path("cat/waiting/", views.CatView.as_view(), name="cat_waiting"),
  path("cat/prices/", views.CatView.as_view(), name="cat_prices"),
  
]
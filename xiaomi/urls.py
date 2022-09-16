from django.urls import path
from . import views

urlpatterns = [
    path("xiaomi/", views.xiaomi, name="xiaomi"),
    path("xiaomi/delivery/<str:pk>/", views.delivery, name="xiaomi_delivery"),
    path("xiaomi/deliveries/", views.deliveries, name="xiaomi_deliveries"),
    path("xiaomi/deliveries/new/", views.new, name="xiaomi_new"),
    
    path("xiaomi/parts/", views.parts, name="xiaomi_parts"),
    path("xiaomi/parts/update/", views.xiaomi_parts_update, name="xiaomi_parts_update"),
    
    path("xiaomi/claims/", views.claims, name="xiaomi_claims"),
    path("xiaomi/claims/new/", views.xiaomi_claims_new, name="xiaomi_claims_new"),
    
    path("xiaomi/waiting/", views.waiting, name="xiaomi_waiting"),
    path("xiaomi/waiting/update/", views.xiaomi_waiting_update, name="xiaomi_waiting_update"),
    
    path("xiaomi/prices/", views.prices, name="xiaomi_prices"),
    
]
from django.urls import path
from . import views

urlpatterns = [
    path("xiaomi/", views.XiaomiView.as_view(),
         name="xiaomi"),
    path("xiaomi/delivery/<str:pk>/", views.xiaomi_delivery, 
         name="xiaomi_delivery"),
    path("xiaomi/deliveries/", views.xiaomi_deliveries, 
         name="xiaomi_deliveries"),
    path("xiaomi/deliveries/new/", views.xiaomi_delivery_new, 
         name="xiaomi_delivery_new"),
    path("xiaomi/delivery/update/<str:pk>/", views.xiaomi_delivery_update, 
         name="xiaomi_delivery_update"),
    path("xiaomi/delivery/file/update/<str:pk>/", views.xiaomi_delivery_file_update,
         name="xiaomi_delivery_file_update"),
    path("xiaomi/delivery/delete/<str:pk>/", views.xiaomi_delivery_delete,
         name="xiaomi_delivery_delete"),
    path("xiaomi/deliveries/report/", views.xiaomi_delivery_report,
         name="xiaomi_delivery_report"),

    path("xiaomi/parts/all", views.xiaomi_parts_all, 
         name="xiaomi_parts_all"),    
    path("xiaomi/parts/", views.xiaomi_parts,
         name="xiaomi_parts"),
    path("xiaomi/parts/update/<str:pk>/", views.xiaomi_parts_update,
         name="xiaomi_parts_update"),
    
    path("xiaomi/claims/", views.xiaomi_claims,
         name="xiaomi_claims"),
    path("xiaomi/claims/new/", views.xiaomi_claims_new,
         name="xiaomi_claims_new"),
    path("xiaomi/claims/update/<str:pk>/", views.xiaomi_claims_update,
         name="xiaomi_claims_update"),
    path("xiaomi/claims/delete/<str:pk>/", views.xiaomi_claims_delete,
         name="xiaomi_claims_delete"),
    
    path("xiaomi/waiting/all", views.xiaomi_waiting_all, 
        name="xiaomi_waiting_all"),
    path("xiaomi/waiting/", views.xiaomi_waiting, 
        name="xiaomi_waiting"),
    path("xiaomi/waiting/update/<str:pk>/", views.xiaomi_waiting_update,
         name="xiaomi_waiting_update"),
    
    path("xiaomi/prices/", views.xiaomi_prices,
         name="xiaomi_prices"),
    
]
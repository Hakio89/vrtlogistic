from django.urls import path
from . import views

urlpatterns = [
    path("maitrox/", views.MaitroxView.as_view(),
         name="maitrox"),
    path("maitrox/delivery/<str:pk>/", views.maitrox_delivery, 
         name="maitrox_delivery"),
    path("maitrox/deliveries/", views.MaitroxDeliveries.as_view(), 
         name="maitrox_deliveries"),
     path("maitrox/deliveries/create/", views.MaitroxDeliveryCreate.as_view(), 
         name="maitrox_delivery_create"),
    path("maitrox/delivery/update/<str:pk>/", views.MaitroxDeliveryUpdate.as_view(), 
         name="maitrox_delivery_update"),
    path("maitrox/delivery/file/update/<str:pk>/", views.MaitroxFileUpdate.as_view(),
         name="maitrox_delivery_file_update"),
    path("maitrox/delivery/delete/<str:pk>/", views.MaitroxDeliveryDelete.as_view(),
         name="maitrox_delivery_delete"),
    path("maitrox/deliveries/report/", views.maitrox_delivery_report,
         name="maitrox_delivery_report"),
    
    path("maitrox/parts/new", views.MaitroxPartsNew.as_view(), 
         name="maitrox_parts_new"),
    path("maitrox/parts/all", views.MaitroxPartsAll.as_view(), 
         name="maitrox_parts_all"),    
    path("maitrox/parts/", views.MaitroxParts.as_view(),
         name="maitrox_parts"),
    path("maitrox/parts/update/<str:pk>/", views.MaitroxPartsUpdate.as_view(),
         name="maitrox_parts_update"),
    
    path("maitrox/claims/", views.MaitroxClaims.as_view(),
         name="maitrox_claims"),
    path("maitrox/claims/new/", views.MaitroxClaimsCreate.as_view(),
         name="maitrox_claims_new"),
    path("maitrox/claims/update/<str:pk>/", views.MaitroxClaimsUpdate.as_view(),
         name="maitrox_claims_update"),
    path("maitrox/claims/delete/<str:pk>/", views.MaitroxClaimsDelete.as_view(),
         name="maitrox_claims_delete"),
    
    path("maitrox/waiting/new", views.MaitroxWaitingCreate.as_view(), 
        name="maitrox_waiting_new"),
    path("maitrox/waiting/all", views.MaitroxWaitingsAll.as_view(), 
        name="maitrox_waiting_all"),
    path("maitrox/waiting/", views.MaitroxWaitings.as_view(), 
        name="maitrox_waiting"),
    path("maitrox/waiting/update/<str:pk>/", views.MaitroxWaitingsUpdate.as_view(),
         name="maitrox_waiting_update"),
    
    path("maitrox/prices/", views.MaitroxPrises.as_view(),
         name="maitrox_prices"),
    
]
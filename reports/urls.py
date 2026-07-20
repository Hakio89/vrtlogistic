from django.urls import path
from . import views

urlpatterns = [
    path("panel-raportow/", views.CCSReportsView.as_view(), name="reports_ccs"),
    path("raport-dostepne-dostawy/", views.DeliveriesReport.as_view(), name="deliveries_report"),    
    path("raport-naprawy-czekajace/", views.LogisticWaitingReport.as_view(), name="logistic_waiting_report"),        
    path("raport-potencjalne-naprawy-do-zwolnienia/", views.PotencialRepairsToReleaseReport.as_view() , name="potencial_repairs_to_release_report"),
    path("raport-naprawy-do-zwolnienia/", views.ProspectiveRepairsToReleaseReport.as_view() , name="prospective_repairs_to_release_report"),
    path("raport-czekajace-w-dostawie/", views.WaitingPartsInBatches.as_view() , name="waiting_in_delivered_batches"),
    path("raport-czesci-w-transporcie/", views.WaitingPartsInTransport.as_view() , name="all-parts-in-transport"),
]
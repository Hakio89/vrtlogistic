from django.urls import path
from . import views

urlpatterns = [
    path("reports/ccs", views.CCSReportsView.as_view(), name="reports_ccs"),
    path("reports/deliveries-report", views.DeliveriesReport.as_view(), name="deliveries_report"),    
    path("reports/logistic-waiting-report", views.LogisticWaitingReport.as_view(), name="logistic_waiting_report"),        
    path("reports/buying-order-report", views.BuyingOrderReport.as_view(), name="buying_order_report"),
    path("reports/available-stock-report", views.run_procedure , name="available_stock_report"),
    path("reports/potencial-repairs-to-release-report", views.PotencialRepairsToReleaseReport.as_view() , name="potencial_repairs_to_release_report"),
    path("reports/prospective-repairs-to-release-report", views.ProspectiveRepairsToReleaseReport.as_view() , name="prospective_repairs_to_release_report"),
    path("reports/replacements", views.ReplacementReport.as_view() , name="replacement_report"),
    path("reports/waiting-parts-in-delivered-batches", views.WaitingPartsInBatches.as_view() , name="waiting_in_delivered_batches"),
]
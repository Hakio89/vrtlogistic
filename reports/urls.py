from django.urls import path
from . import views

urlpatterns = [
    path("reports/ccs", views.CCSReportsView.as_view(), name="reports_ccs"),
    path("reports/deliveries-report", views.DeliveriesReport.as_view(), name="deliveries_report"),    
    path("reports/logistic-waiting-report", views.LogisticWaitingReport.as_view(), name="logistic_waiting_report"),
]
from django.urls import path
from . import views

urlpatterns = [
    path("reports/ccs", views.CCSReportsView.as_view(), name="reports_ccs"),
]
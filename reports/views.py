from django.shortcuts import render
from django.views.generic import ListView

# Create your views here.

class CCSReportsView(ListView):
    template_name = 'reports/ccsreports.html'
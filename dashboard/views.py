from django.shortcuts import render

from xiaomi.models import Xiaomi

# Create your views here.
def dashboard(request):
    deliveries = Xiaomi.objects.all()
    
    ctx = {
        "title" : "Dashboard",
        "deliveries" : deliveries,
        }
    return render(request, "dashboard.html", ctx)
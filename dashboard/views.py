from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from xiaomi.models import Xiaomi

# Create your views here.
@login_required
def dashboard(request):
    deliveries = Xiaomi.objects.all()
    
    ctx = {
        "title" : "Dashboard",
        "deliveries" : deliveries,
        }
    return render(request, "dashboard.html", ctx)
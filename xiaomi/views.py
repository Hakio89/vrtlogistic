from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import XiaomiNew
from .utils.tables import Table
# Create your views here.

@login_required
def xiaomi(request):
    xiao = "XIAOMI"
    title = "Xiaomi Default"
    ctx = {"page_name" : xiao,
           "title" : title}
    return render(request, "xiaomi/xiaomi.html", ctx)

@login_required
def delivery(request, pk):
    single_delivery = Xiaomi.objects.get(delivery=pk)
    parts = XiaomiPartsCatalog.objects.get()
    claim = XiaomiClaimParts.objects.all()
    waiting = XiaomiWaitingParts.objects.get()
    
    table = Table(single_delivery.file, parts=parts.file, claim=claim,
                  waiting=waiting.file)
    
    ctx = {"title" : "Xiaomi Delivery",
           "delivery" : single_delivery,
           "table" : table,
        }
    return render(request, "xiaomi/xiaomi-delivery.html", ctx)

@login_required
def deliveries(request):
    xiaomi_deliveriers_all = Xiaomi.objects.all()
    title = "Xiaomi Deliveries"
    ctx = {"title" : title,
           "xiaomi" : xiaomi_deliveriers_all
    }
    return render(request, "xiaomi/xiaomi-deliveries.html", ctx)

@login_required
def parts(request):
    title = "Xiaomi Parts"
    ctx = {"title" : title}
    return render(request, "xiaomi/xiaomi-parts.html", ctx)

@login_required
def claims(request):
    title = "Xiaomi Claims"
    ctx = {"title" : title}
    return render(request, "xiaomi/xiaomi-claims.html", ctx)

@login_required
def waiting(request):
    title = "Xiaomi Waiting"
    ctx = {"title" : title}
    return render(request, "xiaomi/xiaomi-waiting.html", ctx)

@login_required
def prices(request):
    title = "Xiaomi Prices"
    ctx = {"title" : title}
    return render(request, "xiaomi/xiaomi-prices.html", ctx)

@login_required
def new(request):
    title = "Xiaomi New"
    user = request.user
    form = XiaomiNew()
    
    if request.method == "POST":
        form = XiaomiNew(request.POST, request.FILES)
        
        if form.is_valid():
            delivery = form.save(commit=False)
            delivery.creator = user
            delivery.save()
            return redirect('xiaomi_deliveries')
    
    ctx = {
        "title" : title,
        "form" : form,
           }
    return render(request, "xiaomi/xiaomi-new.html", ctx)
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
    
    table = Table(delivery=single_delivery.file, 
                  parts=parts.file, claim=claim,
                  waiting=waiting.file)
    pmgp_len, pmgh_len, pmgp_sum, pmgh_sum, pmgp_html, pmgh_html \
        = table.delivery_joining()
    
    
    ctx = {"title" : "Xiaomi Delivery",
           "delivery" : single_delivery,
           "pmgp_to_html" : pmgp_html,
            "pmgh_to_html" : pmgh_html,
            "pmgp_len" : pmgp_len,
            "pmgh_len" : pmgh_len,
           "pmgp_sum" : pmgp_sum,
            "pmgh_sum" : pmgh_sum,
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
    parts = XiaomiPartsCatalog.objects.get()
    table = Table(parts=parts.file)
    parts_table = table.parts_to_html()
    
    ctx = {"title" : "Xiaomi Parts",
           "parts" : parts_table,          
           }
    return render(request, "xiaomi/xiaomi-parts.html", ctx)

@login_required
def claims(request):
    claims = XiaomiClaimParts.objects.all()
    table = Table(claim=claims)
    claim_table = table.claim_to_html()
    ctx = {"title" : "Xiaomi Claims",
           "claim" : claim_table,
           }
    return render(request, "xiaomi/xiaomi-claims.html", ctx)

@login_required
def waiting(request):
    waiting  = XiaomiWaitingParts.objects.get()
    table = Table(waiting=waiting.file)
    waiting_table = table.waiting_to_html()
    ctx = {"title" : "Xiaomi Waiting",
           "waiting" : waiting_table,
           }
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

@login_required
def xiaomi_claims_new(request):
    ctx = {"title" : "Xiaomi Claims New"}
    return render(request, "xiaomi/xiaomi-claims-new.html", ctx)

@login_required
def xiaomi_waiting_update(request):
    ctx = {"title" : "Xiaomi Waiting Update"}
    return render(request, "xiaomi/xiaomi-waiting-update.html", ctx)

@login_required
def xiaomi_parts_update(request):
    ctx = {"title" : "Xiaomi Parts Update"}
    return render(request, "xiaomi/xiaomi-parts-update.html", ctx)
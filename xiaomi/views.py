from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import *
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
def xiaomi_delivery_new(request):
    title = "Xiaomi New"
    user = request.user
    form = XiaomiNewForm()
    
    if request.method == "POST":
        form = XiaomiNewForm(request.POST, request.FILES)
        
        if form.is_valid():
            delivery = form.save(commit=False)
            delivery.creator = user
            delivery.save()
            return redirect('xiaomi_deliveries')
    
    ctx = {
        "title" : title,
        "form" : form,
           }
    return render(request, "xiaomi/xiaomi-delivery-new.html", ctx)

@login_required
def xiaomi_delivery_update(request, pk):
    delivery_update = Xiaomi.objects.get(delivery=pk)
    form = XiaomiDeliveryForm(instance=delivery_update)
    
    if request.method == "POST":
        form = XiaomiDeliveryForm(request.POST, instance=delivery_update)
        
        if form.is_valid():
            form.save()
            return redirect('xiaomi_deliveries')
    
    ctx = {
        'form' : form,        
        'xiaomi' : delivery_update,
    }
    
    return render(request, "xiaomi/xiaomi-delivery-update.html", ctx)

@login_required
def xiaomi_delivery_file_update(request, pk):
    delivery_update = Xiaomi.objects.get(delivery=pk)
    form = XiaomiDeliveryFileForm(instance=delivery_update)
    
    if request.method == "POST":
        delivery_update.file.delete()
        form = XiaomiDeliveryFileForm(request.POST, request.FILES, instance=delivery_update)
        
        if form.is_valid():
            form.save()
            return redirect('xiaomi_deliveries')
    
    ctx = {
        'form' : form,
        'xiaomi' : delivery_update,
    }
    
    return render(request, "xiaomi/xiaomi-delivery-file-update.html", ctx)
    

@login_required
def xiaomi_delivery(request, pk):
    single_delivery = Xiaomi.objects.get(delivery=pk)
    parts = XiaomiPartsCatalog.objects.get()
    claim = XiaomiClaimParts.objects.all()
    waiting = XiaomiWaitingParts.objects.get()
    form_pmgp = PmgpDeliveryForm(instance=single_delivery)
    form_pmgh = PmghDeliveryForm(instance=single_delivery)
    
    table = Table(delivery=single_delivery.file, 
                  parts=parts.file, claim=claim,
                  waiting=waiting.file)
    pmgp_len, pmgh_len, pmgp_sum, pmgh_sum, pmgp_html, pmgh_html,\
        del_nan, del_empty = table.delivery_joining()
    
    if request.method == "POST":
        form_p = PmgpDeliveryForm(request.POST, instance=single_delivery)
        form_h = PmghDeliveryForm(request.POST, instance=single_delivery)
        
        if "pmgp" in request.POST:       
            if form_p.is_valid():
                form_p.save()
            
        if "pmgh" in request.POST:
            if form_h.is_valid():
                form_h.save()
            
            
    
    ctx = {"title" : "Xiaomi Delivery",
           "delivery" : single_delivery,
           "pmgp_to_html" : pmgp_html,
            "pmgh_to_html" : pmgh_html,
            "pmgp_len" : pmgp_len,
            "pmgh_len" : pmgh_len,
           "pmgp_sum" : pmgp_sum,
            "pmgh_sum" : pmgh_sum,
            "del_nan" : del_nan,
            "del_empty" : del_empty,
            "form_pmgp" : form_pmgp,
            "form_pmgh" : form_pmgh,
         }
    return render(request, "xiaomi/xiaomi-delivery.html", ctx)

@login_required
def xiaomi_delivery_delete(request, pk):
    single_delivery = Xiaomi.objects.get(delivery=pk)
    single_delivery_file = single_delivery.file
    
    if request.method == 'POST':
        single_delivery_file.delete()
        if request.method == 'POST':
            single_delivery.delete()
            return redirect('xiaomi_deliveries')
    
    
    ctx = {
        "delivery" : single_delivery,
    }
        
    return render(request, "xiaomi/xiaomi-delivery-delete.html", ctx)

@login_required
def xiaomi_deliveries(request):
    xiaomi_deliveriers_all = Xiaomi.objects.all()
    title = "Xiaomi Deliveries"
    ctx = {"title" : title,
           "xiaomi" : xiaomi_deliveriers_all
    }
    return render(request, "xiaomi/xiaomi-deliveries.html", ctx)

@login_required
def xiaomi_claims(request):
    claims = XiaomiClaimParts.objects.all()
    ctx = {"title" : "Xiaomi Claims",
           "claims" : claims,
           }
    return render(request, "xiaomi/xiaomi-claims.html", ctx)

@login_required
def xiaomi_claims_new(request):
    form = XiaomiClaimForm()
    
    if request.method == "POST":
        form = XiaomiClaimForm(request.POST)
        
        if form.is_valid():
            form.save()
            return redirect('xiaomi_claims')
    
    ctx = {"title" : "Xiaomi Claims New",
           "form" : form,
           }
    return render(request, "xiaomi/xiaomi-claims-new.html", ctx)

@login_required
def xiaomi_claims_update(request, pk):
    claim = XiaomiClaimParts.objects.get(id=pk)
    form = XiaomiClaimForm(instance=claim)
    
    if request.method == "POST":
        form = XiaomiClaimForm(request.POST, instance=claim)
        
        if form.is_valid():
            form.save()
            return redirect('xiaomi_claims')
    
    ctx = {"title" : "Xiaomi Claims Update",
           "form" : form,
           "claim" : claim,
           }
    return render(request, "xiaomi/xiaomi-claims-update.html", ctx)

@login_required
def xiaomi_claims_delete(request, pk):
    claim = XiaomiClaimParts.objects.get(id=pk)
    
    if request.method == "POST":
        claim.delete()
        return redirect('xiaomi_claims')
    
    ctx = {"title" : "Xiaomi Claims Update",
           "claim" : claim,
           }
    return render(request, "xiaomi/xiaomi-claims-delete.html", ctx)

@login_required
def xiaomi_waiting(request):
    waiting  = XiaomiWaitingParts.objects.get()
    waiting_all = XiaomiWaitingParts.objects.all()
    table = Table(waiting=waiting.file)
    waiting_table = table.waiting_to_html()
    ctx = {"title" : "Xiaomi Waiting",
           "waiting" : waiting_table,
           "waiting_all" : waiting_all,
           }
    return render(request, "xiaomi/xiaomi-waiting.html", ctx)

@login_required
def xiaomi_prices(request):
    title = "Xiaomi Prices"
    ctx = {"title" : title}
    return render(request, "xiaomi/xiaomi-prices.html", ctx)


@login_required
def xiaomi_waiting_update(request, pk):
    waiting = XiaomiWaitingParts.objects.get(id=pk)
    form = XiaomiWaitingForm(instance=waiting)
    
    if request.method == "POST":
        waiting.file.delete()
        form = XiaomiWaitingForm(request.POST, request.FILES, instance=waiting)       
        
        if form.is_valid():
            waiting_file = form.save(commit=False)
            waiting_file.save()
            return redirect('xiaomi_waiting')
        
    ctx = {"title" : "Xiaomi Waiting Update",
           "form" : form,
           }
    return render(request, "xiaomi/xiaomi-waiting-update.html", ctx)

@login_required
def xiaomi_parts(request):
    parts = XiaomiPartsCatalog.objects.get()
    parts_all = XiaomiPartsCatalog.objects.all()
    table = Table(parts=parts.file)
    parts_table = table.parts_to_html()
    
    ctx = {"title" : "Xiaomi Parts",
           "parts" : parts_table,  
            "parts_all" : parts_all, 
           }
    return render(request, "xiaomi/xiaomi-parts.html", ctx)

@login_required
def xiaomi_parts_update(request, pk):
    parts = XiaomiPartsCatalog.objects.get(id=pk)
    form = XiaomiPartsForm(instance=parts)
    
    if request.method == "POST":
        parts.file.delete()
        form = XiaomiPartsForm(request.POST, request.FILES, instance=parts)       
        
        if form.is_valid():
            parts_file = form.save(commit=False)
            parts_file.save()
            return redirect('xiaomi_parts')
    
    ctx = {"title" : "Xiaomi Parts Update",           
        "form" : form,}
    return render(request, "xiaomi/xiaomi-parts-update.html", ctx)
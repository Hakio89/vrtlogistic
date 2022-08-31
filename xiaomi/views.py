from django.shortcuts import render

from xiaomi.models import Xiaomi
# Create your views here.

def xiaomi(request):
    xiao = "XIAOMI"
    title = "Xiaomi Default"
    ctx = {"page_name" : xiao,
           "title" : title}
    return render(request, "xiaomi/xiaomi.html", ctx)

def delivery(request):
    title = "Xiaomi Delivery"
    ctx = {"title" : title}
    return render(request, "xiaomi/xiaomi-delivery.html", ctx)

def deliveries(request):
    xiaomi_deliveriers_all = Xiaomi.objects.all()
    title = "Xiaomi Deliveries"
    ctx = {"title" : title,
           "xiaomi" : xiaomi_deliveriers_all
    }
    return render(request, "xiaomi/xiaomi-deliveries.html", ctx)

def parts(request):
    title = "Xiaomi Parts"
    ctx = {"title" : title}
    return render(request, "xiaomi/xiaomi-parts.html", ctx)

def claims(request):
    title = "Xiaomi Claims"
    ctx = {"title" : title}
    return render(request, "xiaomi/xiaomi-claims.html", ctx)

def waiting(request):
    title = "Xiaomi Waiting"
    ctx = {"title" : title}
    return render(request, "xiaomi/xiaomi-waiting.html", ctx)

def prices(request):
    title = "Xiaomi Prices"
    ctx = {"title" : title}
    return render(request, "xiaomi/xiaomi-prices.html", ctx)
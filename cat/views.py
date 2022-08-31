from django.shortcuts import render

# Create your views here.

def cat(request):
    title = "CAT Default"
    ctx = {"title" : title}
    return render(request, "cat/cat.html", ctx)

def delivery(request):
    title = "CAT Delivery"
    ctx = {"title" : title}
    return render(request, "cat/cat-delivery.html", ctx)

def deliveries(request):
    title = "CAT Deliveries"
    ctx = {"title" : title}
    return render(request, "cat/cat-deliveries.html", ctx)

def parts(request):
    title = "CAT Parts"
    ctx = {"title" : title}
    return render(request, "cat/cat-parts.html", ctx)

def claims(request):
    title = "CAT Claims"
    ctx = {"title" : title}
    return render(request, "cat/cat-claims.html", ctx)

def waiting(request):
    title = "CAT Waiting"
    ctx = {"title" : title}
    return render(request, "cat/cat-waiting.html", ctx)

def prices(request):
    title = "CAT Prices"
    ctx = {"title" : title}
    return render(request, "cat/cat-prices.html", ctx)
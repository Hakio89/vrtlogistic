from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def cat(request):
    title = "CAT Default"
    ctx = {"title" : title}
    return render(request, "cat/cat.html", ctx)

@login_required
def delivery(request):
    title = "CAT Delivery"
    ctx = {"title" : title}
    return render(request, "cat/cat-delivery.html", ctx)

@login_required
def deliveries(request):
    title = "CAT Deliveries"
    ctx = {"title" : title}
    return render(request, "cat/cat-deliveries.html", ctx)

@login_required
def parts(request):
    title = "CAT Parts"
    ctx = {"title" : title}
    return render(request, "cat/cat-parts.html", ctx)

@login_required
def claims(request):
    title = "CAT Claims"
    ctx = {"title" : title}
    return render(request, "cat/cat-claims.html", ctx)

@login_required
def waiting(request):
    title = "CAT Waiting"
    ctx = {"title" : title}
    return render(request, "cat/cat-waiting.html", ctx)

@login_required
def prices(request):
    title = "CAT Prices"
    ctx = {"title" : title}
    return render(request, "cat/cat-prices.html", ctx)
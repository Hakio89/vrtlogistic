from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def alcatel(request):
    title = "Alcatel Default"
    ctx = {"title" : title}
    return render(request, "alcatel/alcatel.html", ctx)

@login_required
def delivery(request):
    title = "Alcatel Delivery"
    ctx = {"title" : title}
    return render(request, "alcatel/alcatel-delivery.html", ctx)

@login_required
def deliveries(request):
    title = "Alcatel Deliveries"
    ctx = {"title" : title}
    return render(request, "alcatel/alcatel-deliveries.html", ctx)

@login_required
def parts(request):
    title = "Alcatel Parts"
    ctx = {"title" : title}
    return render(request, "alcatel/alcatel-parts.html", ctx)

@login_required
def claims(request):
    title = "Alcatel Claims"
    ctx = {"title" : title}
    return render(request, "alcatel/alcatel-claims.html", ctx)

@login_required
def waiting(request):
    title = "Alcatel Waiting"
    ctx = {"title" : title}
    return render(request, "alcatel/alcatel-waiting.html", ctx)

@login_required
def prices(request):
    title = "Alcatel Prices"
    ctx = {"title" : title}
    return render(request, "alcatel/alcatel-prices.html", ctx)
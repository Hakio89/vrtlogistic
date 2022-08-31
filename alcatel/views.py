from django.shortcuts import render

# Create your views here.

def alcatel(request):
    title = "Alcatel Default"
    ctx = {"title" : title}
    return render(request, "alcatel/alcatel.html", ctx)

def delivery(request):
    title = "Alcatel Delivery"
    ctx = {"title" : title}
    return render(request, "alcatel/alcatel-delivery.html", ctx)

def deliveries(request):
    title = "Alcatel Deliveries"
    ctx = {"title" : title}
    return render(request, "alcatel/alcatel-deliveries.html", ctx)

def parts(request):
    title = "Alcatel Parts"
    ctx = {"title" : title}
    return render(request, "alcatel/alcatel-parts.html", ctx)

def claims(request):
    title = "Alcatel Claims"
    ctx = {"title" : title}
    return render(request, "alcatel/alcatel-claims.html", ctx)

def waiting(request):
    title = "Alcatel Waiting"
    ctx = {"title" : title}
    return render(request, "alcatel/alcatel-waiting.html", ctx)

def prices(request):
    title = "Alcatel Prices"
    ctx = {"title" : title}
    return render(request, "alcatel/alcatel-prices.html", ctx)
from django.shortcuts import render, HttpResponse

# Create your views here.
def dashboard(request):
    ctx = {"title" : "Dashboard"}
    return render(request, "dashboard\dashboard.html", ctx)
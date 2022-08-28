from django.shortcuts import render, HttpResponse

# Create your views here.
def dashboard(request):
    ctx = {"content" : "THIS IS THE MAIN PAGE"}
    return render(request, "dashboard\dashboard.html", ctx)
from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def xiaomi(request):
    return HttpResponse("XIAOMI")

def delivery(request):
    return HttpResponse("XIAOMI DELIVERY")

def deliveries(request):
    return HttpResponse("XIAOMI DELIVERIES")

def parts(request):
    return HttpResponse("XIAOMI PARTS")

def claims(request):
    return HttpResponse("XIAOMI CLAIMS")

def waiting(request):
    return HttpResponse("XIAOMI WAITING")
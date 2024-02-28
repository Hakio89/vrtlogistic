from typing import Any
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView
from django.contrib import messages
from django.template.loader import get_template
from django.core.mail import EmailMessage
from vrtlogistic.settings import EMAIL_HOST_USER
from django.conf import settings

from sqlalchemy import create_engine
from decouple import config

from .models import *
from .forms import *
from .utils.tables import Table

# Create your views here.

@method_decorator(login_required, name='dispatch')
class XiaomiView(ListView):
    model = Xiaomi
    template_name =  "xiaomi/xiaomi.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Xiaomi Default"
        context["claims"] = XiaomiClaimParts.objects.all()
        context["parts"] = XiaomiPartsCatalog.objects.all()
        context["waiting"] = XiaomiWaitingParts.objects.all()
        context["deliveries"] = Xiaomi.objects.all()
        return context
        
    def post(self, request, *args, **kwargs):        
        if self.request.POST:
            try:        
                emails = MailReportReceivers.objects.all()
                deliveries = Xiaomi.objects.all()
                parts = XiaomiPartsCatalog.objects.get()
                waiting = XiaomiWaitingParts.objects.get()
                
                table = Table(
                                delivery=deliveries, 
                                parts=parts,
                                waiting=waiting,
                            )
                
                report = table.mail_report()
                ctx = {
                    'report' : report,
                }
                subject = 'XIAOMI - Aktualny raport oczekujących dostaw'
                message = get_template('xiaomi/xiaomi-delivery-report.html').render(ctx)
                msg = EmailMessage(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    list(emails),
                )
                msg.content_subtype ="html"# Main content is now text/html
                msg.send()
                messages.success(self.request, 'report successfully sent')
                return redirect('xiaomi')
            except:
                messages.warning(self.request, 'Something went wrong. Please contact admin')
                return redirect('xiaomi')

@method_decorator(login_required, name='dispatch')     
class XiaomiDeliveryCreate(CreateView):
    model = Delivery
    form_class = XiaomiDeliveryCreateFileForm
    template_name = "xiaomi/xiaomi-delivery-create.html"

    def post(self, request):
        connection_string = config('MYSQL_CONNECTOR')
        engine = create_engine(connection_string)
        if engine:
            print('start engine"')
        else:
            print('engine error')
        try:
            form = XiaomiDeliveryCreateFileForm(request.POST, request.FILES)
            user = request.user
            
            if form.is_valid():
                delivery = form.save(commit=False)
                if delivery.file.name.endswith(('.xlsx', '.xls', '.xlsx', '.xlsm', '.xlsb', '.odf', '.ods', '.odt')):
                    delivery.creator = user
                    delivery.save()
                    messages.success(request, 'new delivery successfully created')
                    return redirect('xiaomi_deliveries')
                else:
                    messages.warning(request, 'You are trying o add the wrong file format')
        except:
            messages.warning(request, 'Something went wrong. Please contact admin')
            
        return redirect('xiaomi')


@login_required
def xiaomi_delivery_new(request):
    user = request.user
    form = XiaomiNewForm()    
    
    
    if request.method == "POST":
        try:
            form = XiaomiNewForm(request.POST, request.FILES)
            
            if form.is_valid():
                delivery = form.save(commit=False)
                if delivery.file.name.endswith(('.xlsx', '.xls', '.xlsx', '.xlsm', '.xlsb', '.odf', '.ods', '.odt')):
                    delivery.creator = user
                    delivery.save()
                    messages.success(request, 'new delivery successfully created')
                    return redirect('xiaomi_deliveries')
                else:
                    messages.warning(request, 'You are trying o add the wrong file format')
        except:
            messages.warning(request, 'Something went wrong. Please contact admin')
    
    ctx = {
        "title" : "Xiaomi New Delivery",
        "form" : form,
           }
    return render(request, "xiaomi/xiaomi-delivery-new.html", ctx)

@login_required
def xiaomi_delivery_update(request, pk):
    delivery_update = Xiaomi.objects.get(delivery=pk)
    form = XiaomiDeliveryForm(instance=delivery_update)
    
    if request.method == "POST":
        try:
            form = XiaomiDeliveryForm(request.POST, instance=delivery_update)

            if form.is_valid():
                form.save()

                messages.success(request, 'delivery successfully updated')
                return redirect('xiaomi_deliveries')
            
        except:
            messages.warning(request, 'Something went wrong. Please contact admin')
    
    ctx = {
        'title' : "Xiaomi Delivery Update",
        'form' : form,        
        'xiaomi' : delivery_update,
    }
    
    return render(request, "xiaomi/xiaomi-delivery-update.html", ctx)

@login_required
def xiaomi_delivery_file_update(request, pk):
    delivery_update = Xiaomi.objects.get(delivery=pk)
    form = XiaomiDeliveryFileForm(instance=delivery_update)
    
    if request.method == "POST":
        try:
            delivery_update.file.delete()
            form = XiaomiDeliveryFileForm(request.POST, request.FILES, instance=delivery_update)
            
            if form.is_valid():
                delivery = form.save(commit=False)
                if delivery.file.name.endswith(('.xlsx', '.xls', '.xlsx', '.xlsm', '.xlsb', '.odf', '.ods', '.odt')):
                    delivery.save()
                    messages.success(request, 'file successfully updated')
                    return redirect('xiaomi_deliveries')
                else:
                    messages.warning(request, 'You are trying o add the wrong file format')
                    
        except:
            messages.warning(request, 'Something went wrong. Please contact admin')
            
    
    ctx = {
        'title' : "Xiaomi Delivery File Update",
        'form' : form,
        'xiaomi' : delivery_update,
    }
    
    return render(request, "xiaomi/xiaomi-delivery-file-update.html", ctx)
    

@login_required
def xiaomi_delivery(request, pk):
    try:
        single_delivery = Xiaomi.objects.get(delivery=pk)
        parts = XiaomiPartsCatalog.objects.get()
        claim = XiaomiClaimParts.objects.all()
        waiting = XiaomiWaitingParts.objects.get()
        form_pmgp = PmgpDeliveryForm(instance=single_delivery)
        form_pmgh = PmghDeliveryForm(instance=single_delivery)


        table = Table(delivery=single_delivery, 
                    parts=parts, claim=claim,
                    waiting=waiting)
        del_data = table.delivery_joining()
        pmgp = table.pmgp_delivery(del_data)
        pmgh = table.pmgh_delivery(del_data)
        nan = table.nan_delivery(del_data)
        pmgp_html = pmgp.to_html(index=False, table_id="example2", classes="table table-striped table-bordered Transport")  
        pmgh_html = pmgh.to_html(index=False, table_id="example3", classes="table table-striped table-bordered TearDown")
        pmgp_len = len(pmgp)
        pmgh_len = len(pmgh)
        pmgp_sum = pmgp['Qty'].sum()
        pmgh_sum = pmgh['Qty'].sum()
        del_nan = nan.to_html(index=False, table_id="example4", classes="table table-striped table-bordered")
        del_empty = nan.empty
        
        if request.method == "POST":
            form_p = PmgpDeliveryForm(request.POST, instance=single_delivery)
            form_h = PmghDeliveryForm(request.POST, instance=single_delivery)
                            
            if "pmgp" in request.POST:       
                if form_p.is_valid():
                    form_p.save()
                    return redirect(request.path)
                
            if "pmgh" in request.POST:
                if form_h.is_valid():
                    form_h.save()
                    return redirect(request.path)
        
    except TypeError:    
        messages.error(request, 'Make sure your file has no float values. Please change your excel data into general data or contact with the administrator')
        return redirect('xiaomi_deliveries')
    
    except:
        messages.error(request, 'There no data. Please make sure you add parts catalog or contact with the administrator')
        return redirect('xiaomi_deliveries')
            
    ctx = {
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
        try:
            single_delivery_file.delete()
            if request.method == 'POST':
                single_delivery.delete()
                messages.success(request, 'delivery successfully removed')
                return redirect('xiaomi_deliveries')
        
        except:
            messages.warning(request, 'Something went wrong. Please contact admin')
    
    
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
        try:
            form = XiaomiClaimForm(request.POST)
            
            if form.is_valid():
                form.save()
                messages.success(request, 'claim successfully created')
                return redirect('xiaomi_claims')
        
        except:
            messages.warning(request, 'Something went wrong. Please contact admin')
    
    ctx = {"title" : "Xiaomi Claims New",
           "form" : form,
           }
    return render(request, "xiaomi/xiaomi-claims-new.html", ctx)

@login_required
def xiaomi_claims_update(request, pk):
    claim = XiaomiClaimParts.objects.get(id=pk)
    form = XiaomiClaimForm(instance=claim)
    
    if request.method == "POST":
        try:
            form = XiaomiClaimForm(request.POST, instance=claim)
            
            if form.is_valid():
                form.save()
                messages.success(request, 'claim successfully updated')
                return redirect('xiaomi_claims')
        
        except:
            messages.warning(request, 'Something went wrong. Please contact admin')
    
    ctx = {"title" : "Xiaomi Claims Update",
           "form" : form,
           "claim" : claim,
           }
    return render(request, "xiaomi/xiaomi-claims-update.html", ctx)

@login_required
def xiaomi_claims_delete(request, pk):
    claim = XiaomiClaimParts.objects.get(id=pk)
    
    if request.method == "POST":
        try:
            claim.delete()
            messages.success(request, 'claim successfully removed')
            return redirect('xiaomi_claims')
    
        except:
                messages.warning(request, 'Something went wrong. Please contact admin')
    
    ctx = {"title" : "Xiaomi Claims Update",
           "claim" : claim,
           }
    return render(request, "xiaomi/xiaomi-claims-delete.html", ctx)

@login_required
def xiaomi_waiting(request):
    try:
        waiting  = XiaomiWaitingParts.objects.get()
        waiting_all = XiaomiWaitingParts.objects.all()
        table = Table(waiting=waiting.file)
        waiting_table = table.waiting_to_html()
    except:
        messages.error(request, 'Please check your excel file or contact with the administrator')
        return redirect('xiaomi_deliveries')
    
    ctx = {"title" : "Xiaomi Waiting",
           "waiting" : waiting_table,
           "waiting_all" : waiting_all,
           }
    return render(request, "xiaomi/xiaomi-waiting.html", ctx)

@login_required
def xiaomi_waiting_all(request):
    try:
        waiting_all = XiaomiWaitingParts.objects.all()
    except:
        messages.error(request, 'Please check your excel file or contact with the administrator')
        return redirect('xiaomi_deliveries')
    
    ctx = {"title" : "Xiaomi Waiting",
           "all_waiting" : waiting_all,
           }
    return render(request, "xiaomi/xiaomi-waiting-all.html", ctx)

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
        try:
            waiting.file.delete()
            form = XiaomiWaitingForm(request.POST, request.FILES, instance=waiting)       
            
            if form.is_valid():
                waiting_file = form.save(commit=False)
                if waiting_file.file.name.endswith(('.xlsx', '.xls', '.xlsx', '.xlsm', '.xlsb', '.odf', '.ods', '.odt')):
                    waiting_file.save()
                    messages.success(request, 'file successfully updated')
                    return redirect('xiaomi_waiting')
                else:
                    messages.warning(request, 'You are trying o add the wrong file format')
        
        except:
            messages.warning(request, 'Something went wrong. Please contact admin')
        
    ctx = {"title" : "Xiaomi Waiting Update",
           "form" : form,
           }
    return render(request, "xiaomi/xiaomi-waiting-update.html", ctx)

@login_required
def xiaomi_parts(request):
    try:
        parts = XiaomiPartsCatalog.objects.get()
        parts_all = XiaomiPartsCatalog.objects.all()
        table = Table(parts=parts.file)
        parts_table = table.parts_to_html()
    except:
        messages.error(request, 'Please check your excel file or contact with the administrator')
        return redirect('xiaomi_deliveries')
    
    ctx = {"title" : "Xiaomi Parts",
           "parts" : parts_table,  
            "parts_all" : parts_all, 
           }
    return render(request, "xiaomi/xiaomi-parts.html", ctx)

@login_required
def xiaomi_parts_all(request):
    try:
        parts_all = XiaomiPartsCatalog.objects.all()
    except:
        messages.error(request, 'Please check your excel file or contact with the administrator')
        return redirect('xiaomi_deliveries')
    
    ctx = {"title" : "Xiaomi Parts All",
            "all_parts" : parts_all, 
           }
    return render(request, "xiaomi/xiaomi-parts-all.html", ctx)


@login_required
def xiaomi_parts_update(request, pk):
    parts = XiaomiPartsCatalog.objects.get(id=pk)
    form = XiaomiPartsForm(instance=parts)
    
    if request.method == "POST":
        try:
            parts.file.delete()
            form = XiaomiPartsForm(request.POST, request.FILES, instance=parts)       
            
            if form.is_valid():
                parts_file = form.save(commit=False)
                if parts_file.file.name.endswith(('.xlsx', '.xls', '.xlsx', '.xlsm', '.xlsb', '.odf', '.ods', '.odt')):
                    parts_file.save()
                    messages.success(request, 'file successfully updated')
                    return redirect('xiaomi_parts')
                else:
                    messages.error(request, 'Your file has float values. Please change your excel data into general data')
            
        except:
            messages.warning(request, 'Something went wrong. Please contact admin')
    
    ctx = {"title" : "Xiaomi Parts Update",           
        "form" : form,}
    return render(request, "xiaomi/xiaomi-parts-update.html", ctx)

def xiaomi_delivery_report(request):
    deliveries = Xiaomi.objects.all()
    
    try:
        deliveries = Xiaomi.objects.all()
        parts = XiaomiPartsCatalog.objects.get()
        waiting = XiaomiWaitingParts.objects.get()
        
        table = Table(
                        delivery=deliveries, 
                        parts=parts,
                        waiting=waiting,
                    )
        
        report = table.mail_report()
    
    except:
            messages.warning(request, 'Something went wrong. Please contact admin')
            
    ctx = {
        "title" : "Xiaomi Deliveries Report",
        "report" : report,
        "deliveries" : deliveries,
    }
    return render(request, "xiaomi/xiaomi-delivery-report.html", ctx)
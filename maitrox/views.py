from typing import Any
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import (ListView, 
                                  CreateView, 
                                  UpdateView,
                                  DeleteView,
                                  DetailView,
                                  TemplateView)
from django.views.generic.edit import FormView
from django.contrib import messages
from django.template.loader import get_template
from django.core.mail import EmailMessage
from vrtlogistic.settings import EMAIL_HOST_USER
from django.conf import settings
from django.db.migrations.operations import RunSQL
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Sum, OuterRef, Subquery

from sqlalchemy import create_engine
from decouple import config

from .models import *
from .forms import *
from .utils.tables import (Table, 
                           open_delivery_file,
                           open_waitings_file,
                           open_parts_file,)

# Create your views here.

@method_decorator(login_required, name='dispatch')
class MaitroxView(ListView):
    model = Maitrox
    template_name =  "maitrox/maitrox.html"
    
    def get_context_data(self, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
            context["title"] = "Maitrox Default"
            context["claims"] = ClaimParts.objects.all()
            context["parts"] = PartsCatalog.objects.all()
            context["waiting"] = WaitingParts.objects.all()
            context["deliveries"] = Maitrox.objects.all()
            return context
        except:
            messages.warning(self.request, 'Coś poszło nie tak. Skontaktuj się z administratorem')
            return redirect('maitrox')
    def post(self, request, *args, **kwargs):        
        if self.request.POST:
            try:        
                emails = MailReportReceivers.objects.all()
                deliveries = Maitrox.objects.all()
                parts = PartsCatalog.objects.get()
                waiting = WaitingParts.objects.get()
                
                table = Table(
                                delivery=deliveries, 
                                parts=parts,
                                waiting=waiting,
                            )
                
                report = table.mail_report()
                ctx = {
                    'report' : report,
                }
                subject = 'Maitrox - Aktualny raport dostaw'
                message = get_template('maitrox/maitrox-delivery-report.html').render(ctx)
                msg = EmailMessage(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    list(emails),
                )
                msg.content_subtype ="html"# Main content is now text/html
                msg.send()
                messages.success(self.request, 'Raport został poprawnie wysłany')
                return redirect('maitrox')
            except:
                messages.warning(self.request, 'Coś poszło nie tak. Skontaktuj się z administratorem')
                return redirect('maitrox')

@method_decorator(login_required, name='dispatch')     
class MaitroxDeliveryCreate(CreateView):
    model = Maitrox
    form_class = NewDeliveryForm
    template_name = "maitrox/maitrox-delivery-create.html"
    success_url = '/maitrox/deliveries'


    def form_valid(self, form):
        try:
            form.save(commit=False)
            if form.instance.file.name.endswith(('.xlsx', '.xls', '.xlsx', '.xlsm', '.xlsb', '.odf', '.ods', '.odt')):
                check_file =  open_delivery_file(form.instance.file)['SO Number'].values[0]
                check_so = form.instance.delivery
                if check_file == check_so:
                    form.instance.creator = self.request.user
                    connection_string = config('MYSQL_CONNECTOR')
                    engine = create_engine(connection_string)                
                    with engine.connect():
                        df = open_delivery_file(form.instance.file).to_sql('maitrox_deliverydetails', engine, if_exists='append', index=False)
                    form.save()
                    messages.success(self.request, f'Nowa dostawa {form.instance.delivery} utworzona')
                else:
                    messages.warning(self.request, 'Nr SO w formularzu i pliku różnią się, popraw dane!')
                    return redirect('maitrox_delivery_create')
        except TypeError:
                messages.warning(self.request, 'Plik jest uszkodzony. Pobierz template i wklej dane a następnie wczytaj plik')
                return redirect('maitrox_delivery_create')
        except:
            messages.warning(self.request, 'Coś poszło nie tak. Skontaktuj się z administratorem')
            return redirect('maitrox_delivery_create')
        return super().form_valid(form)        

@method_decorator(login_required, name='dispatch') 
class MaitroxDeliveryUpdate(UpdateView):
    model = Maitrox
    form_class = DeliveryForm
    template_name = "maitrox/maitrox-delivery-update.html"
    success_url = '/maitrox/deliveries/'
    
    def form_valid(self, form):
        try: 
            form.save()
            messages.success(self.request, f'Dostawa {form.instance.delivery} zaktualizowana')
            return super().form_valid(form)   
        except:
            messages.warning(self.request, 'Coś poszło nie tak. Skontaktuj się z administratorem')
            return redirect('maitrox')
    def get_object(self):
        try: 
            model_instance = Maitrox.objects.get(delivery=self.kwargs['pk'])
            return model_instance
        except:
            messages.warning(self.request, 'Coś poszło nie tak. Skontaktuj się z administratorem')
            return redirect('maitrox')
@method_decorator(login_required, name='dispatch') 
class MaitroxFileUpdate(UpdateView):
    model = Maitrox
    form_class = DeliveryFileForm
    template_name = "maitrox/maitrox-delivery-file-update.html"
    success_url = '/maitrox/deliveries/'
    
    def get_object(self):
        try:
            model_instance = Maitrox.objects.get(delivery=self.kwargs['pk'])
            return model_instance
        except:
            messages.warning(self.request, 'Coś poszło nie tak. Skontaktuj się z administratorem')
            return redirect('maitrox')
    def form_valid(self, form):
        try:
            to_be_deleted = Maitrox.objects.get(delivery=self.kwargs['pk'])
            detele_old_data = DeliveryDetails.objects.filter(so_number=to_be_deleted)
            detele_old_data.delete()
            to_be_deleted.file.delete()        
            form.save(commit=False)
            if form.instance.file.name.endswith(('.xlsx', '.xls', '.xlsx', '.xlsm', '.xlsb', '.odf', '.ods', '.odt')):
                check_file =  open_delivery_file(form.instance.file)['SO Number'].values[0]
                check_so = form.instance.delivery
                if check_file == check_so:
                    form.instance.creator = self.request.user
                    connection_string = config('MYSQL_CONNECTOR')
                    engine = create_engine(connection_string)                
                    with engine.connect():
                        df = open_delivery_file(form.instance.file).to_sql('maitrox_deliverydetails', engine, if_exists='append', index=False)
                    form.save()
                    messages.success(self.request, f'Plik {form.instance.delivery} został zaktualizowany')
                else:
                    messages.warning(self.request, 'Nr SO w formularzu i pliku różnią się, popraw dane!')
                    return redirect('maitrox_delivery_file_update')        
            return super().form_valid(form)    
        except:
            messages.warning(self.request, 'Coś poszło nie tak. Skontaktuj się z administratorem')
            return redirect('maitrox')
@method_decorator(login_required, name='dispatch') 
class MaitroxDeliveryDelete(DeleteView):
    model = Maitrox
    template_name = "maitrox/maitrox-delivery-delete.html"
    success_url = '/maitrox/deliveries/'
    
    def post(self, request, *args, **kwargs):        
        if self.request.POST:
            try:
                to_be_deleted = Maitrox.objects.get(delivery=self.kwargs['pk'])
                detele_old_data = DeliveryDetails.objects.filter(so_number=to_be_deleted)
                detele_old_data.delete()
                to_be_deleted.delete()
                messages.success(self.request, f'Dostawa {to_be_deleted} została usunięta')
                return redirect('maitrox_deliveries')
            except:
                messages.warning(self.request, 'Something went wrong. Please contact admin')
        return redirect('xiaomi_deliveries')
    
    def get_object(self):
        try:
            model_instance = Maitrox.objects.get(delivery=self.kwargs['pk'])
            return model_instance
        except:
            messages.warning(self.request, 'Coś poszło nie tak. Skontaktuj się z administratorem')
            return redirect('maitrox')

class MaitroxDeliveryDetails(DetailView):
    model = Maitrox
    template_name = "maitrox/maitrox-delivery.html"
    success_url = '/maitrox/deliveries/'
    
    def get_context_data(self, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
            context['title'] = Maitrox.objects.get(delivery=self.kwargs['pk'])
            delivery_details = DeliveryDetails.objects.filter(
                so_number=self.kwargs['pk'])
            context['delivery_details']= delivery_details
            context['countings'] = delivery_details.aggregate(count_pn=Count('parts_number'),
                sum_pn=Sum('qty'))
            return context
        except:
            messages.warning(self.request, 'Coś poszło nie tak. Skontaktuj się z administratorem')
            return redirect('maitrox')
    
    def get_object(self):
        try:
            model_instance = Maitrox.objects.get(delivery=self.kwargs['pk'])
            return model_instance
        except:
            messages.warning(self.request, 'Coś poszło nie tak. Skontaktuj się z administratorem')
            return redirect('maitrox')
@method_decorator(login_required, name='dispatch') 
class MaitroxDeliveries(ListView):
    model = Maitrox
    template_name = "maitrox/maitrox-deliveries.html"
    context_object_name = "maitrox"


@method_decorator(login_required, name='dispatch') 
class MaitroxClaims(ListView):
    model = ClaimParts
    template_name = "maitrox/maitrox-claims.html"
    context_object_name = "claims"

@method_decorator(login_required, name='dispatch') 
class MaitroxClaimsCreate(CreateView):
    model = ClaimParts
    template_name = 'maitrox/maitrox-claims-new.html'
    success_url = '/maitrox/claims/'
    form_class = ClaimForm
    
    def form_valid(self, form):
        try:
            form.save()
            messages.success(self.request, f'Nowa reklamacja {form.instance.claim_part} została dodana')
            return super().form_valid(form)
        except:
            messages.warning(self.request, 'Coś poszło nie tak. Skontaktuj się z administratorem')
            return redirect('maitrox')
@method_decorator(login_required, name='dispatch') 
class MaitroxClaimsUpdate(UpdateView):
    model = ClaimParts
    template_name = 'maitrox/maitrox-claims-update.html'
    success_url = '/maitrox/claims'
    form_class = ClaimForm
    
    def form_valid(self, form):
        try:
            form.save()
            messages.success(self.request, f'Claim for {form.instance.claim_part} updated successfully')
            return super().form_valid(form)
        except:
            messages.warning(self.request, 'Coś poszło nie tak. Skontaktuj się z administratorem')
            return redirect('maitrox')
@method_decorator(login_required, name='dispatch') 
class MaitroxClaimsDelete(DeleteView):
    model = ClaimParts
    template_name = 'maitrox/maitrox-claims-delete.html'
    success_url = '/maitrox/claims'
    
@method_decorator(login_required, name='dispatch')
class MaitroxWaitingCreate(CreateView):
    model = WaitingParts
    template_name = 'maitrox/maitrox-waiting-new.html'
    form_class = WaitingForm
    success_url = '/maitrox/waiting/all'
    
    def form_valid(self, form):
        try:
            form.save(commit=False)
            if form.instance.file.name.endswith(('.xlsx', '.xls', '.xlsx', '.xlsm', '.xlsb', '.odf', '.ods', '.odt')):
                #try: 
                connection_string = config('MYSQL_CONNECTOR')
                engine = create_engine(connection_string)                
                with engine.connect():
                    df = open_waitings_file(form.instance.file).to_sql('maitrox_waitingsdetails', engine, if_exists='append', index_label='id')
                form.save()
                messages.success(self.request, 'Nowe części czekające zostały dodane')
                #except:
                #    messages.warning(self.request, 'There is some error. Please contact administrator')
                #    return redirect('xiaomi_waiting_new')
            return super().form_valid(form)        
        except:
            messages.warning(self.request, 'Coś poszło nie tak. Skontaktuj się z administratorem')
            return redirect('maitrox')
@method_decorator(login_required, name='dispatch')
class MaitroxWaitings(ListView):
    model = WaitingsDetails
    template_name = "maitrox/maitrox-waiting.html"
    context_object_name = 'waiting_table'

@method_decorator(login_required, name='dispatch')
class MaitroxWaitingsAll(ListView):
    model = WaitingParts
    template_name = "maitrox/maitrox-waiting-all.html"
    context_object_name = "all_waiting"

@method_decorator(login_required, name='dispatch')
class MaitroxPrises(ListView):
    template_name = "xiaomi/xiaomi-prices.html"
    
@method_decorator(login_required, name='dispatch')
class MaitroxWaitingsUpdate(UpdateView):
    model = WaitingParts
    template_name = "maitrox/maitrox-waiting-update.html"
    form_class = WaitingForm
    success_url = '/maitrox/waiting/all'
    
    def form_valid(self, form):
        try:     
            form.save(commit=False)
            to_be_deleted = WaitingParts.objects.get(id=self.kwargs['pk'])
            to_be_deleted.file.delete() 
            if form.instance.file.name.endswith(('.xlsx', '.xls', '.xlsx', '.xlsm', '.xlsb', '.odf', '.ods', '.odt')):
                connection_string = config('MYSQL_CONNECTOR')
                engine = create_engine(connection_string)                
                with engine.connect():
                    df = open_waitings_file(form.instance.file).to_sql('xiaomi_waitingsdetails', engine, if_exists='replace', index_label='id')
                form.save()
                messages.success(self.request, 'Plik został poprawnie zaktualizowany')       
            return super().form_valid(form)    
        except:
            messages.warning(self.request, 'Coś poszło nie tak. Skontaktuj się z administratorem')
            return redirect('maitrox')
        
@method_decorator(login_required, name='dispatch')
class MaitroxPartsNew(CreateView):
    model = PartsCatalog
    template_name = 'maitrox/maitrox-parts-new.html'
    form_class = PartsForm
    success_url = '/maitrox/parts/all'
    
    def form_valid(self, form):
        form.save(commit=False)
        if form.instance.file.name.endswith(('.xlsx', '.xls', '.xlsx', '.xlsm', '.xlsb', '.odf', '.ods', '.odt')):
            try:    
                connection_string = config('MYSQL_CONNECTOR')
                engine = create_engine(connection_string)                
                with engine.connect():
                    df = open_parts_file(form.instance.file).to_sql('maitrox_partsdetails', engine, if_exists='append', index_label='id')
                    form.save()
                    messages.success(self.request, 'Nowy katalog części został dodany')
            except:
                messages.warning(self.request, 'There is some error. Please contact administrator')
                return redirect('xiaomi_parts_new')
        return super().form_valid(form)        
    
@method_decorator(login_required, name='dispatch')
class MaitroxParts(ListView):
    model = PartsDetails
    template_name = "maitrox/maitrox-parts.html"
    context_object_name = "parts_table"
    
@method_decorator(login_required, name='dispatch')
class MaitroxPartsAll(ListView):
    model = PartsCatalog
    template_name = "maitrox/maitrox-parts-all.html"
    context_object_name = "all_parts"
    
@method_decorator(login_required, name='dispatch')
class MaitroxPartsUpdate(UpdateView):
    model = PartsCatalog
    template_name = "maitrox/maitrox-parts-update.html"
    form_class = PartsForm
    success_url = '/maitrox/parts/all'
    
    def form_valid(self, form):
        try:     
            form.save(commit=False)
            to_be_deleted = PartsCatalog.objects.get(id=self.kwargs['pk'])
            to_be_deleted.file.delete() 
            if form.instance.file.name.endswith(('.xlsx', '.xls', '.xlsx', '.xlsm', '.xlsb', '.odf', '.ods', '.odt')):
                connection_string = config('MYSQL_CONNECTOR')
                engine = create_engine(connection_string)                
                with engine.connect():
                    df = open_parts_file(form.instance.file).to_sql('xiaomi_partsdetails', engine, if_exists='replace', index_label='id')
                form.save()
                messages.success(self.request, 'File has been updated successfully')       
            return super().form_valid(form)    
        except:
            messages.warning(self.request, 'Coś poszło nie tak. Skontaktuj się z administratorem')
            return redirect('maitrox')
        
class MaitroxDeliveryReport(TemplateView):
    template_name = "maitrox/maitrox-delivery-report.html"
    
    def get_context_data(self, **kwargs: Any):
        ctx = super().get_context_data(**kwargs)
        ctx['deliveries'] = Maitrox.objects.filter(status__status='Transport')
        ctx['title']= 'Maitrox Deliveries Report'            
        return ctx
    """def maitrox_delivery_report(request):
        deliveries = Maitrox.objects.all()
        
        try:
            deliveries = Maitrox.objects.all()
            parts = PartsCatalog.objects.get()
            waiting = WaitingParts.objects.get()
            
            table = Table(
                            delivery=deliveries, 
                            parts=parts,
                            waiting=waiting,
                        )
            
            report = table.mail_report()
        
        except:
                messages.warning(request, 'Coś poszło nie tak, skontakuj się z administratorem')
                
        ctx = {
            "title" : "Maitrox Deliveries Report",
            "report" : report,
            "deliveries" : deliveries,
        }
        return render(request, "maitrox/maitrox-delivery-report.html", ctx)"""
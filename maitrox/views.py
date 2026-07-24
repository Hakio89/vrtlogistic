from typing import Any
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
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
                           open_parts_file,
                           read_ax_zz,
                           )
from reports.models import BuyingOrder

# Create your views here.

@method_decorator(login_required, name='dispatch')
class MaitroxView(ListView):
    model = Maitrox
    template_name =  "maitrox/maitrox.html"
        
    def post(self, request, *args, **kwargs):        
        if self.request.POST:
            try:        
                emails = MailReportReceivers.objects.all()
                transport = Maitrox.objects.filter(status__status='Transport')
                verification = Maitrox.objects.filter(status__status='verification')
                base_url = request.build_absolute_uri('/')[:-1]
                ctx = {
                    'transport': transport,
                    'verification': verification,
                    'base_url': base_url,
                }
                subject = 'Raport dostaw by VL'
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

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["title"] = "Pulpit dostaw"
        
        # Deliveries list (needed for report generation POST action or legacy references)
        deliveries = Maitrox.objects.all()
        context["deliveries"] = deliveries
        
        # 1. Total deliveries count
        context["total_deliveries"] = deliveries.count()
        
        # 2. Total parts quantity in all deliveries
        context["total_parts_in_deliveries"] = DeliveryDetails.objects.aggregate(Sum('qty'))['qty__sum'] or 0
        
        # 3. Total waiting parts quantity
        context["total_waiting_parts"] = WaitingsDetails.objects.aggregate(Sum('qty'))['qty__sum'] or 0
        
        # 4. Total claimed parts quantity
        context["total_claimed_parts"] = ClaimParts.objects.aggregate(Sum('qty'))['qty__sum'] or 0
        
        # Additional context data for premium dashboard:
        # Deliveries by status
        context["status_counts"] = Maitrox.objects.values('status__status').annotate(count=Count('id'))
        
        # 5 latest deliveries
        context["latest_deliveries"] = Maitrox.objects.order_by('-date')[:5]
        
        # Total unique parts in catalog
        context["total_catalog_parts"] = PartsDetails.objects.count()
        
        # Active vs resolved claims
        context["active_claims_count"] = ClaimParts.objects.filter(status='Waiting').count()
        context["resolved_claims_count"] = ClaimParts.objects.filter(status='Claimed').count()
        
        return context
    

@method_decorator(login_required, name='dispatch')     
class MaitroxDeliveryCreate(CreateView):
    model = Maitrox
    form_class = NewDeliveryForm
    template_name = "maitrox/maitrox-delivery-create.html"
    success_url = reverse_lazy('maitrox_deliveries')
    extra_context = {"title": "Nowa dostawa"}


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
        except Exception as e:
            import traceback
            traceback.print_exc()
            messages.warning(self.request, f'Coś poszło nie tak: {str(e)}')
            return redirect('maitrox_delivery_create')
        return super().form_valid(form)        

@method_decorator(login_required, name='dispatch') 
class MaitroxDeliveryUpdate(UpdateView):
    model = Maitrox
    form_class = DeliveryForm
    template_name = "maitrox/maitrox-delivery-update.html"
    success_url = reverse_lazy('maitrox_deliveries')
    extra_context = {"title": "Edycja dostawy"}
    
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
    success_url = reverse_lazy('maitrox_deliveries')
    extra_context = {"title": "Edycja pliku dostawy"}
    
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
    success_url = reverse_lazy('maitrox_deliveries')
    extra_context = {"title": "Usuń dostawę"}
    
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
                messages.warning(self.request, 'Coś poszło nie tak. Skontaktuj się z administratorem')
        return redirect('maitrox_deliveries')
    
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
    success_url = reverse_lazy('maitrox_deliveries')
    
    def get_context_data(self, **kwargs: Any):
        try:
            ctx = super().get_context_data(**kwargs)
            ctx['title'] = Maitrox.objects.get(delivery=self.kwargs['pk'])
            delivery_details = list(DeliveryDetails.objects.filter(so_number=self.kwargs['pk']))
            
            # Bulk precalculate warehouse types and waiting quantities to eliminate N+1 queries
            part_numbers = [item.parts_number for item in delivery_details if item.parts_number]
            
            # Fetch PartsDetails in bulk
            parts_details_map = {
                pd.parts_number: pd.warehouse 
                for pd in PartsDetails.objects.filter(parts_number__in=part_numbers)
            }
            
            # Fetch LogisticWaiting aggregates from external ccs database in bulk
            from reports.models import LogisticWaiting
            waiting_aggregates = LogisticWaiting.objects.filter(
                KodPozycji__in=part_numbers,
                StatusWiersza='Braki zamówione'
            ).using('ccs').values('KodPozycji').annotate(total_waiting=Sum('Ilosc'))
            
            waiting_map = {
                item['KodPozycji']: item['total_waiting'] 
                for item in waiting_aggregates
            }
            
            # Attach precalculated variables
            for item in delivery_details:
                item.precalculated_warehouse = parts_details_map.get(item.parts_number, 'Brak')
                item.precalculated_waiting = waiting_map.get(item.parts_number) or 0
                
            ctx['delivery_details'] = delivery_details
            ctx['countings'] = DeliveryDetails.objects.filter(so_number=self.kwargs['pk']).aggregate(
                count_pn=Count('parts_number'),
                sum_pn=Sum('qty')
            )
            ax = BuyingOrder.objects.filter(OdwolanieDoDostawcy=self.kwargs['pk']).using("ccs")
            ctx['ax'] = read_ax_zz(ax)            
            return ctx
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
    extra_context = {"title": "Wszystkie dostawy"}
    queryset = Maitrox.objects.all().select_related('status', 'creator')


@method_decorator(login_required, name='dispatch') 
class MaitroxClaims(ListView):
    model = ClaimParts
    template_name = "maitrox/maitrox-claims.html"
    context_object_name = "claims"
    extra_context = {"title": "Rejestr reklamacji"}

@method_decorator(login_required, name='dispatch') 
class MaitroxClaimsCreate(CreateView):
    model = ClaimParts
    template_name = 'maitrox/maitrox-claims-new.html'
    success_url = reverse_lazy('maitrox_claims')
    form_class = ClaimForm
    extra_context = {"title": "Nowa reklamacja"}
    
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
    success_url = reverse_lazy('maitrox_claims')
    form_class = ClaimForm
    extra_context = {"title": "Edycja reklamacji"}
    
    def form_valid(self, form):
        try:
            form.save()
            messages.success(self.request, f'Reklamacja dla {form.instance.claim_part} została pomyślnie zaktualizowana')
            return super().form_valid(form)
        except:
            messages.warning(self.request, 'Coś poszło nie tak. Skontaktuj się z administratorem')
            return redirect('maitrox')
@method_decorator(login_required, name='dispatch') 
class MaitroxClaimsDelete(DeleteView):
    model = ClaimParts
    template_name = 'maitrox/maitrox-claims-delete.html'
    success_url = reverse_lazy('maitrox_claims')
    extra_context = {"title": "Usuń reklamację"}
    
@method_decorator(login_required, name='dispatch')
class MaitroxWaitingCreate(CreateView):
    model = WaitingParts
    template_name = 'maitrox/maitrox-waiting-new.html'
    form_class = WaitingForm
    success_url = reverse_lazy('maitrox_waiting_all')
    extra_context = {"title": "Dodaj plik czekających"}
    
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
    extra_context = {"title": "Części czekające"}

@method_decorator(login_required, name='dispatch')
class MaitroxWaitingsAll(ListView):
    model = WaitingParts
    template_name = "maitrox/maitrox-waiting-all.html"
    context_object_name = "all_waiting"
    extra_context = {"title": "Pliki czekających"}


@method_decorator(login_required, name='dispatch')
class MaitroxWaitingsUpdate(UpdateView):
    model = WaitingParts
    template_name = "maitrox/maitrox-waiting-update.html"
    form_class = WaitingForm
    success_url = reverse_lazy('maitrox_waiting_all')
    extra_context = {"title": "Edycja pliku czekających"}
    
    def form_valid(self, form):
        try:     
            form.save(commit=False)
            to_be_deleted = WaitingParts.objects.get(id=self.kwargs['pk'])
            to_be_deleted.file.delete() 
            if form.instance.file.name.endswith(('.xlsx', '.xls', '.xlsx', '.xlsm', '.xlsb', '.odf', '.ods', '.odt')):
                connection_string = config('MYSQL_CONNECTOR')
                engine = create_engine(connection_string)                
                with engine.connect():
                    df = open_waitings_file(form.instance.file).to_sql('maitrox_waitingsdetails', engine, if_exists='replace', index_label='id')
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
    success_url = reverse_lazy('maitrox_parts_all')
    extra_context = {"title": "Dodaj katalog części"}
    
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
                messages.warning(self.request, 'Wystąpił błąd. Skontaktuj się z administratorem')
                return redirect('maitrox_parts_new')
        return super().form_valid(form)        
    
@method_decorator(login_required, name='dispatch')
class MaitroxParts(ListView):
    model = PartsDetails
    template_name = "maitrox/maitrox-parts.html"
    context_object_name = "parts_table"
    extra_context = {"title": "Katalog części"}
    
@method_decorator(login_required, name='dispatch')
class MaitroxPartsAll(ListView):
    model = PartsCatalog
    template_name = "maitrox/maitrox-parts-all.html"
    context_object_name = "all_parts"
    extra_context = {"title": "Katalogi części"}
    
@method_decorator(login_required, name='dispatch')
class MaitroxPartsUpdate(UpdateView):
    model = PartsCatalog
    template_name = "maitrox/maitrox-parts-update.html"
    form_class = PartsForm
    success_url = reverse_lazy('maitrox_parts_all')
    extra_context = {"title": "Edycja katalogu części"}
    
    def form_valid(self, form):
        try:     
            form.save(commit=False)
            to_be_deleted = PartsCatalog.objects.get(id=self.kwargs['pk'])
            to_be_deleted.file.delete() 
            if form.instance.file.name.endswith(('.xlsx', '.xls', '.xlsx', '.xlsm', '.xlsb', '.odf', '.ods', '.odt')):
                connection_string = config('MYSQL_CONNECTOR')
                engine = create_engine(connection_string)                
                with engine.connect():
                    df = open_parts_file(form.instance.file).to_sql('maitrox_partsdetails', engine, if_exists='replace', index_label='id')
                form.save()
                messages.success(self.request, 'Plik został pomyślnie zaktualizowany')       
            return super().form_valid(form)    
        except:
            messages.warning(self.request, 'Coś poszło nie tak. Skontaktuj się z administratorem')
            return redirect('maitrox')
        
class MaitroxDeliveryReport(TemplateView):
    template_name = "maitrox/maitrox-delivery-report.html"
    
    def get_context_data(self, **kwargs: Any):
        try:
            ctx = super().get_context_data(**kwargs)
            ctx['transport'] = Maitrox.objects.filter(status__status='Transport')
            ctx['verification'] = Maitrox.objects.filter(status__status='Verification')
            ctx['title']= 'Maitrox Deliveries Report'
            ctx['base_url'] = self.request.build_absolute_uri('/')[:-1]
            return ctx
        except:
            messages.warning(self.request, 'Coś poszło nie tak. Skontaktuj się z administratorem')
            return redirect('maitrox')
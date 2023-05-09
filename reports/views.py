from typing import Any, Dict
from django.db.models.query import QuerySet
from django.shortcuts import redirect, render, HttpResponse
from django.views.generic import ListView
from .forms import CCSReportsForm
from xiaomi.models import Xiaomi
from django.contrib import messages
from .models import LogisticWaiting, BuyingOrder, Replacements
from django.db import connections
from .calculate import stock_checking, all_pn_stock, parts_for_repair, checking_enough_stock

# Create your views here.

class CCSReportsView(ListView):
    template_name = 'reports/allreportslist.html'
    queryset = Xiaomi.objects.all()    

    def get_context_data(self, object_list=None, **kwargs):        
        queryset = object_list if object_list is not None else self.object_list
        context = super().get_context_data(**kwargs)           
        form = CCSReportsForm()
        show = True
        """if self.request.GET:
            try:
                report_name = self.request.GET['report']
                if report_name == 'NC':
                    return redirect('logistic_waiting_report')
            except:
                messages.error(self.request, 'Błąd - głoś problem do administratora')"""
        context['form'] = form
        context['show'] = show
        return context
    
    def post(self, request, *args, **kwargs):
        if self.request.POST:
            try:
                report_name = self.request.POST['report']
                if report_name == 'NC':
                    return redirect('logistic_waiting_report')
                if report_name == 'DCC':
                    return redirect('available_stock_report')
                if report_name == 'PNDZ':
                    return redirect('potencial_repairs_to_release_report')
                if report_name == 'DX':
                    return redirect('deliveries_report')
            except:
                messages.error(self.request, 'Błąd - głoś problem do administratora')
                return redirect('reports_ccs')
            else:
                messages.warning(self.request, 'Wybierz raport, który chcesz wynegerować')        
                return redirect('reports_ccs'), 

        
class DeliveriesReport(ListView):
    template_name = 'reports/deliveriesreport.html'
    queryset = Xiaomi.objects.all()

class LogisticWaitingReport(ListView):
    template_name = 'reports/logisticwaitingreport.html'
    queryset = LogisticWaiting.objects.filter(
        Status='Czeka', 
        StatusWiersza='Braki zamówione'
        ).order_by('DataRejestracji', 'KodPozycjiTypNaprawy').using('ccs')   
    
    def get_context_data(self, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
            context['title'] = 'Naprawy czekające'    
            return context 
        except:
            messages.warning(self.request, 'Something went wrong. Please contact admin')
            return redirect('reports_ccs')

        

class BuyingOrderReport(ListView):
    template_name = 'reports/buyingordersreport.html'
    queryset = BuyingOrder.objects.all().filter(ZamowienieZakupu='ZZ/23/001129').using('ccs')


def run_procedure(request):
        try:
            all_parts =  all_pn_stock()
            ctx = {
            'title' : "Dostępne części pod naprawy czekające",
                'all_parts' : all_parts
            }

            return render(request, 'reports/availablestokcreport.html', ctx)
        except:
            messages.warning(request, 'Something went wrong. Please contact admin')
            return redirect('reports_ccs')

class PotencialRepairsToReleaseReport(ListView): 
    template_name = 'reports/potencialrepairstorelease.html'
    queryset = LogisticWaiting.objects.filter(
        Status='Czeka', 
        StatusWiersza='Braki zamówione'
        ).order_by(
            'DataRejestracji'
        ).using('ccs')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        show = False
        form = CCSReportsForm()
        if self.request.method == 'GET':
            form = CCSReportsForm(self.request.GET)
            if form.is_valid():
                data = self.request.GET.getlist('select_business')
                show = True
                queryset = LogisticWaiting.objects.filter(
                Producent__in=data,
                Status='Czeka', 
                StatusWiersza='Braki zamówione'
                ).order_by(
                    'DataRejestracji'
                ).using('ccs')
                stock = all_pn_stock(queryset)
                repair_parts = parts_for_repair(queryset)
                enough_stock = checking_enough_stock(stock, repair_parts)
                queryset = queryset.filter(NrNaprawy__in=enough_stock)
                if len(queryset) == 0:
                    messages.warning(self.request, 'Brak potencjalnych napraw do zwolnienia dla wybranych biznesów')
                context['queryset'] = queryset
                
       
        
        context['title'] = 'Potencjalne naprawy do zwolnienia'
        
        context['show'] = show
        context['form'] = form
        return context
        """except:
            messages.warning(self.request, 'Something went wrong. Please contact admin')"""
        
    
    def post(self, request, *args, **kwargs):
        pass
        

class ReplacementReport(ListView):
    template_name = 'reports/replacementreport.html'
    queryset = Replacements.objects.all().using('ccs')[0:4]
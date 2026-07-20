from django.shortcuts import redirect, render
from django.views.generic import ListView, View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import CCSReportsForm
from maitrox.models import Maitrox
from django.contrib import messages
from .models import (
    LogisticWaiting, 
    BuyingOrder, 
    Replacements,
    )

from .calculate import (
    parts_for_repair, 
    checking_enough_stock, 
    unrepeated_pn_stock,
    all_pn_stock,
    )
from maitrox.models import Maitrox

# Create your views here.

class CCSConnectionRequiredMixin:
    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except Exception as e:
            print(f"CCS Database connection error: {e}")
            return render(request, '500.html', status=500)

class PotencialRepairsToReleaseReport(View):

    def get(self, request, *args, **kwargs):
        return redirect('prospective_repairs_to_release_report')

@method_decorator(login_required, name='dispatch')
class CCSReportsView(ListView):
    template_name = 'reports/allreportslist.html'
    queryset = Maitrox.objects.all()
    extra_context = {"title": "Panel raportów"}

    def get_context_data(self, object_list=None, **kwargs):        
        queryset = object_list if object_list is not None else self.object_list
        context = super().get_context_data(**kwargs)           
        form = CCSReportsForm()
        show = True
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
    queryset = Maitrox.objects.all()
    extra_context = {"title": "Dostępne dostawy"}

class LogisticWaitingReport(CCSConnectionRequiredMixin, ListView):
    template_name = 'reports/logisticwaitingreport.html'
    model = LogisticWaiting
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Naprawy czekające' 
        context['reports'] =  LogisticWaiting.objects.filter(
        Status='Czeka', 
        StatusWiersza='Braki zamówione'
        ).order_by('DataRejestracji', 'KodPozycjiTypNaprawy').using("ccs")  
        return context 


class ProspectiveRepairsToReleaseReport(CCSConnectionRequiredMixin, ListView): 
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
                unrepeated_pn = unrepeated_pn_stock(queryset)
                all_pmgp, all_pmgh, all_smgs, all_tech_pmgp, all_tech_smgs  = all_pn_stock(unrepeated_pn)
                repair_parts, set_repair_parts = parts_for_repair(queryset)
                enough_stock = checking_enough_stock(
                    all_pmgp, 
                    all_pmgh, 
                    all_smgs,
                    all_tech_pmgp,
                    all_tech_smgs,
                    repair_parts, 
                    set_repair_parts,
                    queryset,
                    )
                queryset = queryset.filter(NrNaprawy__in=enough_stock)
                messages.success(self.request, 'Raport został poprawnie wygenerowany')
                if len(queryset) == 0:
                    messages.warning(self.request, 'Brak potencjalnych napraw do zwolnienia dla wybranych biznesów')
                context['queryset'] = queryset
            elif form.is_valid() == False:
                messages.info(self.request, 'Wybierz odpowiedni biznes/y lub wszystkie, a następnie wciśnij przycisk "Generuj Raport"')
        context['title'] = 'Potencjalne naprawy do zwolnienia'
        context['show'] = show
        context['form'] = form
        return context
        
    
    def post(self, request, *args, **kwargs):
        pass
        

class WaitingPartsInBatches(CCSConnectionRequiredMixin, ListView):
    template_name = 'reports/waiting-in-delivered-batches.html'
    queryset = Maitrox.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Czekające w dostawie'
        deliveries_in_batches = list(Maitrox.objects.filter(status__status='Verification'))
        batches = list(BuyingOrder.objects.filter(OdwolanieDoDostawcy__in=deliveries_in_batches).using("ccs"))
        
        # Bulk query LogisticWaiting aggregates to avoid N+1 queries to MS SQL Server
        from django.db.models import Sum
        from .models import LogisticWaiting
        part_numbers = [bo.KodPozycji for bo in batches if bo.KodPozycji]
        waiting_aggregates = LogisticWaiting.objects.filter(
            KodPozycji__in=part_numbers
        ).using('ccs').values('KodPozycji').annotate(total_waiting=Sum('Ilosc'))
        
        waiting_map = {
            item['KodPozycji']: item['total_waiting'] 
            for item in waiting_aggregates
        }
        
        for bo in batches:
            bo.precalculated_waiting = waiting_map.get(bo.KodPozycji) or 0
            
        context['batches'] = batches
        return context
        
class WaitingPartsInTransport(CCSConnectionRequiredMixin, ListView):
    template_name = 'reports/all-parts-in-transport.html'
    queryset = Maitrox.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Części w transporcie'
        deliveries_in_transport = list(Maitrox.objects.filter(status__status='Transport'))
        transport = list(BuyingOrder.objects.filter(OdwolanieDoDostawcy__in=deliveries_in_transport).using("ccs"))
        
        # Bulk query LogisticWaiting aggregates to avoid N+1 queries to MS SQL Server
        from django.db.models import Sum
        from .models import LogisticWaiting
        part_numbers = [bo.KodPozycji for bo in transport if bo.KodPozycji]
        waiting_aggregates = LogisticWaiting.objects.filter(
            KodPozycji__in=part_numbers
        ).using('ccs').values('KodPozycji').annotate(total_waiting=Sum('Ilosc'))
        
        waiting_map = {
            item['KodPozycji']: item['total_waiting'] 
            for item in waiting_aggregates
        }
        
        for bo in transport:
            bo.precalculated_waiting = waiting_map.get(bo.KodPozycji) or 0
            
        context['transport'] = transport
        return context

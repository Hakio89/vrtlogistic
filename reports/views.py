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

class PotencialRepairsToReleaseReport(View):

    def get(self, request, *args, **kwargs):
        return redirect('prospective_repairs_to_release_report')

@method_decorator(login_required, name='dispatch')
class CCSReportsView(ListView):
    template_name = 'reports/allreportslist.html'
    queryset = Maitrox.objects.all()

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

class LogisticWaitingReport(ListView):
    template_name = 'reports/logisticwaitingreport.html'
    model = LogisticWaiting
    
    def get_context_data(self, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
            context['title'] = 'Naprawy czekające' 
            context['reports'] =  LogisticWaiting.objects.filter(
            Status='Czeka', 
            StatusWiersza='Braki zamówione'
            ).order_by('DataRejestracji', 'KodPozycjiTypNaprawy').using("ccs")  
            return context 
        except:
            messages.warning(self.request, 'Błąd - głoś problem do administratora')
            return redirect('reports_ccs')

        

class BuyingOrderReport(ListView):
    template_name = 'reports/buyingordersreport.html'
    queryset = BuyingOrder.objects.all().filter(ZamowienieZakupu='ZZ/23/001129').using('ccs')


def run_procedure(request):
        try:
            all_parts =  all_pn_stock('410200005U5V')
            ctx = {
            'title' : "Dostępne części pod naprawy czekające",
                'all_parts' : all_parts
            }

            return render(request, 'reports/availablestokcreport.html', ctx)
        except:
            messages.warning(request, 'Błąd - głoś problem do administratora')
            return redirect('reports_ccs')

class ProspectiveRepairsToReleaseReport(ListView): 
    template_name = 'reports/potencialrepairstorelease.html'
    queryset = LogisticWaiting.objects.filter(
        Status='Czeka', 
        StatusWiersza='Braki zamówione'
        ).order_by(
            'DataRejestracji'
        ).using('ccs')
    
    def get_context_data(self, **kwargs):
        try:
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
        except:
            messages.warning(self.request, 'Błąd - głoś problem do administratora')
            return redirect('reports_ccs')
        
    
    def post(self, request, *args, **kwargs):
        pass
        

class ReplacementReport(ListView):
    template_name = 'reports/replacementreport.html'
    queryset = Replacements.objects.all().using('ccs')[0:4]

class WaitingPartsInBatches(ListView):
    template_name = 'reports/waiting-in-delivered-batches.html'
    queryset = Maitrox.objects.all()

    def get_context_data(self, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
            deliveries_in_batches = list(Maitrox.objects.filter(status__status='Verification'))
            context['batches'] = BuyingOrder.objects.filter(OdwolanieDoDostawcy__in=deliveries_in_batches).using("ccs")
            return context
        except:
            messages.warning(self.request, 'Błąd - głoś problem do administratora')
            return redirect('reports_ccs')
        
class WaitingPartsInTransport(ListView):
    template_name = 'reports/all-parts-in-transport.html'
    queryset = Maitrox.objects.all()

    def get_context_data(self, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
            deliveries_in_transport = list(Maitrox.objects.filter(status__status='Transport'))
            print(deliveries_in_transport)
            context['transport'] = BuyingOrder.objects.filter(OdwolanieDoDostawcy__in=deliveries_in_transport).using("ccs")
            return context
        except:
            messages.warning(self.request, 'Błąd - głoś problem do administratora')
            return redirect('reports_ccs')

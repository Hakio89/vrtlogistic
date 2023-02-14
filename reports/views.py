from django.shortcuts import redirect
from django.views.generic import ListView
from .forms import CCSReportsForm
from xiaomi.models import Xiaomi
from django.contrib import messages
from .models import Django

# Create your views here.

class CCSReportsView(ListView):
    template_name = 'reports/ccsreports.html'
    queryset = Xiaomi.objects.all()
    
    def get_context_data(self, object_list=None, **kwargs):        
        queryset = object_list if object_list is not None else self.object_list
        context = super().get_context_data(**kwargs)           
        form = CCSReportsForm(self.request.GET)
        show = False
        context['ccs'] = Django.objects.all().using('ccs')
        
        if self.request.GET:
            try:
                if form.is_valid():                        
                    queryset = queryset.order_by('-date')
                    show = True
                    messages.success(self.request, 'Raport został poprawnie wygenerowany')
            except:
                messages.error(self.request, 'Błąd - głoś problem do administratora')
        
        context['form'] = form
        context['deliveries'] = queryset
        context['show'] = show
        
    
        
        return context
        
        
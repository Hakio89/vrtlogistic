from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from maitrox.models import Maitrox

# Create your views here.

@method_decorator(login_required, name='dispatch')
class DashboardView(TemplateView):
    template_name = 'dashboard.html'
    
    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context["title"] =  "Dashboard"
            context["deliveries"] = Maitrox.objects.all()
            return context
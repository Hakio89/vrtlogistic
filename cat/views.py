from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

# Create your views here.
@method_decorator(login_required, name='dispatch')
class CatView(TemplateView):
    template_name = "cat/cat.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "CAT Default"
        return context
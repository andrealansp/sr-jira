from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView, ListView


from relatorios.models import Painel
from .forms import PaineisFilterForm


# Create your views here.
class RelatoriosListView(LoginRequiredMixin,TemplateView):
    template_name = 'relatorios.html'

class RelatorioPaineisView(LoginRequiredMixin,ListView):
    template_name = 'paineis.html'
    context_object_name = 'paineis'
    model = Painel
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PaineisFilterForm(self.request.GET or None)
        return context

    def get_queryset(self):
        instancia = super().get_queryset().all()
        ponto = self.request.GET.get("ponto")
        data_registro = self.request.GET.get("data_registro")

        if ponto:
            instancia = instancia.filter(ponto=ponto)
        if data_registro:
            instancia = instancia.filter(data_registro__date=data_registro)
        return instancia


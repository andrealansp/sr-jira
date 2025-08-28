import os

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import FileResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView, ListView

from app.settings import MEDIA_ROOT
from relatorios.models import Painel
from .forms import PaineisFilterForm
import pandas as pd

class RelatoriosListView(LoginRequiredMixin,TemplateView):
    template_name = 'relatorios.html'

class RelatorioPaineisView(LoginRequiredMixin,ListView):
    template_name = 'paineis.html'
    context_object_name = 'paineis'
    model = Painel
    paginate_by = 150

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PaineisFilterForm(self.request.GET or None)
        return context

    def get_queryset(self):
        instancia = super().get_queryset().all()
        ponto = self.request.GET.get("ponto")
        data_registro = self.request.GET.get("data_registro")
        horario = self.request.GET.get("horario")

        if ponto:
            instancia = instancia.filter(ponto=ponto)
        if data_registro:
            instancia = instancia.filter(data_registro__date=data_registro)
        if horario:
            instancia = instancia.filter(data_registro__hour=horario.split(":")[0])
        return instancia

class RelatorioPainelLastData(LoginRequiredMixin,ListView):
    template_name = 'paineis.html'
    model = Painel
    context_object_name = 'paineis'
    paginate_by = 150

    def get_queryset(self):
        instancia = super().get_queryset().all()
        instancia = instancia.order_by('ponto','-data_registro').distinct("ponto")
        return instancia


class ExportListView(LoginRequiredMixin,View):

    def get(self, request, *args, **kwargs):
        ponto = self.request.GET.get("ponto")
        data_registro = self.request.GET.get("data_registro")

        queryset = Painel.objects.all()

        if ponto:
            queryset = queryset.filter(ponto=ponto)
        if data_registro:
            queryset = queryset.filter(data_registro__date=data_registro)

        df = pd.DataFrame(queryset.values_list(), columns=('id', 'data_registro', 'ponto','ip','status','uptime'))
        df['data_registro']= df['data_registro'].dt.strftime('%Y-%m-%d %H:%M')
        df.to_excel(os.path.join(MEDIA_ROOT, 'xlsx/paineis.xlsx'), index=False)
        return FileResponse(open(os.path.join(MEDIA_ROOT, 'xlsx/paineis.xlsx'), "rb"), as_attachment=True,
                            filename="paineis.xlsx")
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView, MonthArchiveView

from processadores.forms import AcompanhamentoForm
from processadores.models import Processador, Acompanhamento


# Create your views here.
class ProcessadorListView(LoginRequiredMixin, ListView):
    template_name = "processador/processador_list.html"
    model = Processador

    def get_context_data(self, **kwargs):
        context = super(ProcessadorListView, self).get_context_data(**kwargs)
        context['qtd_processadores'] = Processador.objects.all().count()
        return context

class ProcessadorCreateView(LoginRequiredMixin,CreateView):
    template_name = "processador/processador_create.html"
    template_name_suffix = "_create"
    model = Processador
    fields = "__all__"
    success_url = reverse_lazy("processadores:listar")

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse_lazy("processadores:listar"))

class ProcessadorUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "processador/processador_update.html"
    template_name_suffix = "_update"
    model = Processador
    fields = "__all__"

class ProcessadorDeleteView(DeleteView):
    template_name = 'processador/processador_confirm_delete.html'
    model = Processador
    queryset = Processador.objects.all()
    success_url = reverse_lazy("processadores:listar")

class AcompanhamentoListView(LoginRequiredMixin, ListView):
    template_name = "acompanhamento/acompanhamento_list.html"
    model = Acompanhamento

class AcompanhamentoCreateView(LoginRequiredMixin, CreateView):
    template_name = "acompanhamento/acompanhamento_create.html"
    template_name_suffix = "_create"
    model = Acompanhamento
    form_class = AcompanhamentoForm
    success_url = reverse_lazy("processadores:listar_acompanhamento")

class AcompanhamentoUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "acompanhamento/acompanhamento_update.html"
    template_name_suffix = "_update"
    model = Acompanhamento
    form_class = AcompanhamentoForm
    success_url = reverse_lazy("processadores:listar_acompanhamento")

class AcompanhamentoDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'acompanhamento/acompanhamento_confirm_delete.html'
    model = Acompanhamento
    queryset = Acompanhamento.objects.all()
    success_url = reverse_lazy("processadores:listar_acompanhamento")

class AcompanhamentoMonthView(LoginRequiredMixin, MonthArchiveView):
    template_name = "acompanhamento/acompanhamento_list.html"
    queryset = Acompanhamento.objects.all()
    date_field = 'data_inicial'
    month_format = '%m'
    allow_future = False

class AcompanhamentoRelatorioView(LoginRequiredMixin, ListView):
    template_name = "acompanhamento/acompanhamento_report.html"
    model = Acompanhamento
    queryset = Acompanhamento.objects.all()

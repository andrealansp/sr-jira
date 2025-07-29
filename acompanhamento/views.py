from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView, DetailView

from .forms import AcompanhamentoForm
from .forms import AcompanhamentoFilterForm
from .models import Acompanhamento


class AcompanhamentoListView(LoginRequiredMixin, ListView):
    template_name = "acompanhamento/acompanhamento_list.html"
    model = Acompanhamento

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AcompanhamentoFilterForm(self.request.GET or None)
        return context


    def get_queryset(self):
        instancia = super().get_queryset().all()
        ano = self.request.GET.get('ano')
        mes = self.request.GET.get('mes')
        processador = self.request.GET.get("processador")

        if ano:
            instancia = instancia.filter(data_inicial__year=ano)
        if mes:
            instancia = instancia.filter(data_inicial__month=mes)
        if processador:
            instancia = instancia.filter(id_processador=processador)


        return instancia


class AcompanhamentoCreateView(LoginRequiredMixin, CreateView):
    template_name = "acompanhamento/acompanhamento_form.html"
    template_name_suffix = "_create"
    model = Acompanhamento
    form_class = AcompanhamentoForm
    success_url = reverse_lazy("acompanhamento:listar")

class AcompanhamentoUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "acompanhamento/acompanhamento_form.html"
    template_name_suffix = "_update"
    model = Acompanhamento
    form_class = AcompanhamentoForm
    success_url = reverse_lazy("acompanhamento:listar")


class AcompanhamentoDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'acompanhamento/acompanhamento_confirm_delete.html'
    model = Acompanhamento
    queryset = Acompanhamento.objects.all()
    success_url = reverse_lazy("acompanhamento:listar")


class AcompanhamentoRelatorioView(LoginRequiredMixin, ListView):
    template_name = "acompanhamento/acompanhamento_report.html"
    model = Acompanhamento
    queryset = Acompanhamento.objects.all()


class AcompanhamentoDetailView(LoginRequiredMixin, DetailView):
    template_name = "acompanhamento/acompanhamento_detail.html"
    model = Acompanhamento
    queryset = Acompanhamento.objects.all()

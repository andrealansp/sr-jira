from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.functions import ExtractYear, ExtractMonth
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView, MonthArchiveView
from django.db.models import Q
from pandas.core.interchange.from_dataframe import primitive_column_to_ndarray

from .forms import AcompanhamentoForm
from .models import Acompanhamento


class AcompanhamentoListView(LoginRequiredMixin, ListView):
    template_name = "acompanhamento/acompanhamento_list.html"
    model = Acompanhamento

    def get_context_data(self, **kwargs):
        context = super(AcompanhamentoListView, self).get_context_data(**kwargs)
        context["datas"] = (Acompanhamento.objects
                            .annotate(ano=ExtractYear('data_inicial'), mes=ExtractMonth('data_inicial'))
                            .values_list('ano', 'mes')
                            .distinct()
                            .order_by('ano', 'mes'))

        context["lista_processador"] = Acompanhamento.objects.order_by("id_processador").all().distinct(
            "id_processador__identificacao")
        return context

    def get_queryset(self):
        instancia = super().get_queryset().all()
        data = None
        if self.request.GET.get("data"):
            data = self.request.GET.get("data").split("/")
            if data[0]:
                instancia = instancia.filter(data_inicial__year=data[0])
            if data[1]:
                instancia = instancia.filter(data_inicial__month=data[1])
        processador = self.request.GET.get("processador")

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


class AcompanhamentoVisualizacaoView(LoginRequiredMixin, TemplateView):
    template_name = "acompanhamento/acompanhamento_visualizacao.html"

    def get_context_data(self, **kwargs):
        context = super(AcompanhamentoVisualizacaoView, self).get_context_data(**kwargs)
        context["acompanhamento"] = Acompanhamento.objects.filter(data_inicial__month=self.kwargs['month']).all()
        return context


class AcompanhamentoRelatorioView(LoginRequiredMixin, ListView):
    template_name = "acompanhamento/acompanhamento_report.html"
    model = Acompanhamento
    queryset = Acompanhamento.objects.all()

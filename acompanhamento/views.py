from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.functions import ExtractYear, ExtractMonth
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView, MonthArchiveView

from .forms import AcompanhamentoForm
from .models import Acompanhamento


class AcompanhamentoListView(LoginRequiredMixin, ListView):
    template_name = "acompanhamento_list.html"
    model = Acompanhamento

    def get_context_data(self, **kwargs):
        context = super(AcompanhamentoListView, self).get_context_data(**kwargs)
        context["datas"] = (Acompanhamento.objects
                            .annotate(ano=ExtractYear('data_inicial'), mes=ExtractMonth('data_inicial'))
                            .values_list('ano', 'mes')
                            .distinct()
                            .order_by('ano', 'mes'))
        return context


class AcompanhamentoCreateView(LoginRequiredMixin, CreateView):
    template_name = "acompanhamento_create.html"
    template_name_suffix = "_create"
    model = Acompanhamento
    form_class = AcompanhamentoForm
    success_url = reverse_lazy("processadores:listar_acompanhamento")


class AcompanhamentoUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "acompanhamento_update.html"
    template_name_suffix = "_update"
    model = Acompanhamento
    form_class = AcompanhamentoForm
    success_url = reverse_lazy("processadores:listar_acompanhamento")


class AcompanhamentoDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'acompanhamento_confirm_delete.html'
    model = Acompanhamento
    queryset = Acompanhamento.objects.all()
    success_url = reverse_lazy("processadores:listar_acompanhamento")


class AcompanhamentoVisualizacaoView(LoginRequiredMixin, TemplateView):
    template_name = "acompanhamento_visualizacao.html"

    def get_context_data(self, **kwargs):
        context = super(AcompanhamentoVisualizacaoView, self).get_context_data(**kwargs)
        context["acompanhamento"] = Acompanhamento.objects.filter(data_inicial__month=self.kwargs['month']).all()
        return context


class AcompanhamentoRelatorioView(LoginRequiredMixin, ListView):
    template_name = "acompanhamento_report.html"
    model = Acompanhamento
    queryset = Acompanhamento.objects.all()


class AcompanhamentoMonthListView(LoginRequiredMixin, MonthArchiveView):
    template_name = "acompanhamento_list.html"
    queryset = Acompanhamento.objects.all()
    date_field = "data_inicial"
    month_format = "%m"
    allow_future = False

    def get_context_data(self, **kwargs):
        context = super(AcompanhamentoMonthListView, self).get_context_data(**kwargs)
        context["datas"] = (Acompanhamento.objects
                            .annotate(ano=ExtractYear('data_inicial'), mes=ExtractMonth('data_inicial'))
                            .values_list('ano', 'mes')
                            .distinct()
                            .order_by('ano', 'mes'))
        return context

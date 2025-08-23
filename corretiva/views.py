import os

import pandas as pd
from dotenv import load_dotenv
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, FileResponse
from django.urls import reverse
from django.views.generic import TemplateView, FormView, View

from app.common.jira_handling import JiraHandling
from app.settings import MEDIA_ROOT
from corretiva.forms import CorretivaForm

load_dotenv()

class CorretivaTemplateView(LoginRequiredMixin, TemplateView):
    login_url = '/accounts/login/'
    template_name = "corretiva.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Corretivas"
        return context


class RmgvFormView(LoginRequiredMixin, FormView):
    login_url = '/accounts/login/'
    form_class = CorretivaForm
    template_name = "corretiva_handling.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Exportar Chamados Corretivos de RMGV"
        return context

    def form_valid(self, form):
        di = form.cleaned_data["data_inicial"]
        df = form.cleaned_data["data_final"]
        return HttpResponseRedirect(reverse('rmgv_lista', kwargs={'di': di, 'df': df}))


class ForaDivisaFormView(LoginRequiredMixin, FormView):
    login_url = '/accounts/login/'
    form_class = CorretivaForm
    template_name = "corretiva_handling.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Exportar Chamados Corretivos de FORA DIVISA"
        return context

    def form_valid(self, form):
        di = form.cleaned_data["data_inicial"]
        df = form.cleaned_data["data_final"]
        return HttpResponseRedirect(reverse('fora_divisa_lista', kwargs={'di': di, 'df': df}))


class RmgvListView(LoginRequiredMixin, TemplateView):
    login_url = '/accounts/login/'
    template_name = "corretiva_rmgv.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['chamados'] = self.get_tickets()
        context['resumo'] = self.get_statistics_corrective()
        context['data_final'] = self.kwargs['df']
        context['data_inicial'] = self.kwargs['di']
        return context

    def get_tickets(self):
        jira_context = JiraHandling(
            os.getenv("BASE_URL"),
            os.getenv("USER_JIRA"),
            os.getenv("API_TOKEN"),
            os.getenv("CAMPOS_CORRETIVAS"),
        )
        jira_context.set_jql("perkons-corretivas-rmgv", self.kwargs['di'], self.kwargs['df'])
        return jira_context.getissues()

    def get_statistics_corrective(self):
        jira_context = JiraHandling(
            os.getenv("BASE_URL"),
            os.getenv("USER_JIRA"),
            os.getenv("API_TOKEN"),
            os.getenv("CAMPOS_CORRETIVAS"),
        )
        jira_context.set_jql("perkons-corretivas-rmgv", self.kwargs['di'], self.kwargs['df'])
        return jira_context.get_statistic_corrective()


class ForaDivisaListView(LoginRequiredMixin, TemplateView):
    login_url = '/accounts/login/'
    template_name = "corretiva_fora_rmgv.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['chamados'] = self.get_tickets()
        context['resumo'] = self.get_statistics_corrective()
        context['data_final'] = self.kwargs['df']
        context['data_inicial'] = self.kwargs['di']
        return context

    def get_tickets(self):
        jira_context = JiraHandling(
            os.getenv("BASE_URL"),
            os.getenv("USER_JIRA"),
            os.getenv("API_TOKEN"),
            os.getenv("CAMPOS_CORRETIVAS"),
        )
        jira_context.set_jql("perkons-corretivas-fora-divisa", self.kwargs['di'], self.kwargs['df'])
        return jira_context.getissues()

    def get_statistics_corrective(self):
        jira_context = JiraHandling(
            os.getenv("BASE_URL"),
            os.getenv("USER_JIRA"),
            os.getenv("API_TOKEN"),
            os.getenv("CAMPOS_CORRETIVAS"),
        )
        jira_context.set_jql("perkons-corretivas-fora-divisa", self.kwargs['di'], self.kwargs['df'])
        return jira_context.get_statistic_corrective()


class ExportRmgvView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request, *args, **kwargs):
        jira_context = JiraHandling(
            os.getenv("BASE_URL"),
            os.getenv("USER_JIRA"),
            os.getenv("API_TOKEN"),
            os.getenv("CAMPOS_CORRETIVAS"),
        )
        jira_context.set_jql('perkons-corretivas-rmgv', self.kwargs['di'], self.kwargs['df'])
        lista = jira_context.getissues()
        lista_chamados = []

        for chamado in lista.values():
            atendimento_breached: str = "NO PRAZO"
            solucao_breached: str = "NO PRAZO"
            if chamado.fields.customfield_10063.completedCycles[0].breached:
                solucao_breached = "FORA DO PRAZO"

            if chamado.fields.customfield_10062.completedCycles[0].breached:
                atendimento_breached = "FORA DO PRAZO"

            lista_chamados.append({
                "Chave": chamado.key,
                "Prioridade": chamado.fields.priority,
                "Resumo": chamado.fields.summary,
                "Aberto Por": chamado.fields.reporter.displayName,
                "Local de Atendimento": chamado.fields.customfield_10060.child.value,
                "Sla Atendimento": atendimento_breached,
                "Sla Solução": solucao_breached
            })

        df = pd.DataFrame(lista_chamados)
        df.to_excel(os.path.join(MEDIA_ROOT, 'xlsx/corretiva.xlsx'), index=False)
        return FileResponse(open(os.path.join(MEDIA_ROOT, 'xlsx/corretiva.xlsx'), "rb"), as_attachment=True,
                            filename="CorretivasRMGV.xlsx")


class ExportForaDivisa(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request, *args, **kwargs):
        jira_context = JiraHandling(
            os.getenv("BASE_URL"),
            os.getenv("USER_JIRA"),
            os.getenv("API_TOKEN"),
            os.getenv("CAMPOS_CORRETIVAS"),
        )
        jira_context.set_jql('perkons-corretivas-fora-divisa', self.kwargs['di'], self.kwargs['df'])
        lista = jira_context.getissues()
        lista_chamados = []

        for chamado in lista.values():
            atendimento_breached: str = "NO PRAZO"
            solucao_breached: str = "NO PRAZO"
            if chamado.fields.customfield_10062.completedCycles[0].breached:
                atendimento_breached = "FORA DO PRAZO"

            if chamado.fields.customfield_10063.completedCycles[0].breached:
                solucao_breached = "FORA DO PRAZO"

            lista_chamados.append({
                "Chave": chamado.key,
                "Prioridade": chamado.fields.priority,
                "Resumo": chamado.fields.summary,
                "Aberto Por": chamado.fields.reporter.displayName,
                "Local de Atendimento": chamado.fields.customfield_10060.child.value,
                "Sla Atendimento": atendimento_breached,
                "Sla Solução": solucao_breached
            })

        df = pd.DataFrame(lista_chamados)
        df.to_excel(os.path.join(MEDIA_ROOT, 'xlsx/corretivafora.xlsx'), index=False)
        return FileResponse(open(os.path.join(MEDIA_ROOT, 'xlsx/corretivafora.xlsx'), "rb"), as_attachment=True,
                            filename="CorretivasFORADIVISA.xlsx")

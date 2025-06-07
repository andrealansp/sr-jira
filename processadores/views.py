from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView

from processadores.models import Processador


# Create your views here.
class ProcessadorListView(ListView):
    template_name = "processadores_list.html"
    model = Processador

    def get_context_data(self, **kwargs):
        context = super(ProcessadorListView, self).get_context_data(**kwargs)
        context['qtd_processadores'] = Processador.objects.all().count()
        return context

class ProcessadorCreateView(CreateView):
    template_name = "processadores_create.html"
    template_name_suffix = "_create"
    model = Processador
    fields = "__all__"
    success_url = reverse_lazy("processadores:lista")

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse_lazy("processadores:lista"))

class ProcessadorUpdateView(UpdateView):
    template_name = "processadores_update.html"
    template_name_suffix = "_update"
    model = Processador
    fields = "__all__"
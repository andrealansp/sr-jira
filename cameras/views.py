from datetime import datetime
from typing import Any
from django.db.models.query import QuerySet
from django.db.models import Q
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Cameras
from .forms import CameraForm


class CameraListView(LoginRequiredMixin, ListView):
    login_url = "/accounts/login/"
    model = Cameras
    paginate_by = 50
    template_name = "camera_list"

    def get_queryset(self) -> QuerySet[Any]:
        cameras = super().get_queryset().order_by("ponto","porta")
        ponto = self.request.GET.get("ponto")
        serial = self.request.GET.get("serial")
        regiao = self.request.GET.get("regiao")
        nome_camera = self.request.GET.get("nome_camera")

        if ponto:
            cameras = cameras.filter(ponto__icontains=ponto)
        if serial:
            cameras = cameras.filter(serial__icontains=serial)
        if regiao:
            cameras = cameras.filter(regiao__icontains=regiao)
        if nome_camera:
            cameras = cameras.filter(nome_camera__icontains=nome_camera)

        return cameras

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cameras = self.get_queryset()
        context["qtd_cameras"] = cameras.count()
        return context



class CameraCreateView(LoginRequiredMixin, CreateView):
    login_url = "/accounts/login/"
    model = Cameras
    form_class = CameraForm
    success_url = reverse_lazy("cameras:list")
    template_name_suffix = "_create_form"

    def get_initial(self, *args, **kwargs) -> dict[str, Any]:
        initial = super().get_initial(**kwargs)
        initial["atualizado"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return initial


class CameraUpdateView(LoginRequiredMixin, UpdateView):
    login_url = "/accounts/login/"
    model = Cameras
    form_class = CameraForm
    success_url = reverse_lazy("cameras:list")
    template_name_suffix = "_update_form"

    def get_initial(self, *args, **kwargs) -> dict[str, Any]:
        initial = super().get_initial(**kwargs)
        initial["atualizado"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return initial


class CameraDelete(LoginRequiredMixin, DeleteView):
    login_url = "/accounts/login/"
    queryset = Cameras.objects.all()
    success_url = reverse_lazy("cameras:list")
    template_name_suffix = "_confirm_delete"

from datetime import datetime
from typing import Any
from django.db.models.query import QuerySet
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Cameras
from .forms import CameraForm


class CameraListView(LoginRequiredMixin, ListView):
    login_url = "/accounts/login/"
    model = Cameras
    paginate_by = 15
    template_name = "camera_list.htnl"

    def get_queryset(self) -> QuerySet[Any]:
        cameras = super().get_queryset().order_by("ponto")
        ponto = self.request.GET.get("ponto")
        serial = self.request.GET.get("serial")
        regiao = self.request.GET.get("regiao")
        if ponto:
            cameras = cameras.filter(ponto__icontains=ponto)
        if serial:
            cameras = cameras.filter(serial__icontains=serial)
        if regiao:
            cameras = cameras.filter(regiao__icontains=regiao)
        return cameras


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

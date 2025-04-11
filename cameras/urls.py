from django.urls import path
from .views import *

app_name = "cameras"

urlpatterns = [
    path("", CameraListView.as_view(), name="list"),
    path("cadastro", CameraCreateView.as_view(), name="create"),
    path("atualizar/<int:pk>", CameraUpdateView.as_view(), name="update"),
    path("excluir/<int:pk>", CameraDelete.as_view(), name="delete"),
]

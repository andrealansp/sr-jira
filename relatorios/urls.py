from django.urls import path
from relatorios import views

app_name = 'relatorios'

urlpatterns = [
    path('', views.RelatoriosListView.as_view(), name='listar'),
    path('paineis', views.RelatorioPaineisView.as_view(), name='paineis'),
    path('paineis/exportar', views.ExportListView.as_view(), name='exportar'),
]

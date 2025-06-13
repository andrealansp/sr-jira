from django.urls import path
from acompanhamento import views

app_name = 'acompanhamento'


urlpatterns = [
    path('', views.AcompanhamentoListView.as_view(), name="listar"),
    path('registrar', views.AcompanhamentoCreateView.as_view(), name="registrar"),
    path('atualizar/<pk>', views.AcompanhamentoUpdateView.as_view(), name="atualizar"),
    path('deletar/<pk>', views.AcompanhamentoDeleteView.as_view(), name="deletar"),
    path('relatorio/<int:year>/<int:month>',views.AcompanhamentoRelatorioView.as_view(), name="relatorio"),
    path("visualizar/<int:year>/<int:month>", views.AcompanhamentoVisualizacaoView.as_view(), name="visualizar"),
]

from django.urls import path
from acompanhamento import views

app_name = 'acompanhamento'


urlpatterns = [
    path('acompanhamento', views.AcompanhamentoListView.as_view(), name="listar"),
    path("acompanhamento/<int:year>/<int:month>", views.AcompanhamentoMonthListView.as_view(), name="listar_mes"),
    path('acompanhamento/registrar', views.AcompanhamentoCreateView.as_view(), name="registrar"),
    path('acompanhamento/atualizar/<pk>', views.AcompanhamentoUpdateView.as_view(), name="atualizar"),
    path('acompanhamento/deletar/<pk>', views.AcompanhamentoDeleteView.as_view(), name="deletar"),
    path('acompanhamento/relatorio/<int:year>/<int:month>',views.AcompanhamentoRelatorioView.as_view(), name="relatorio"),
    path("acompanhamento/visualizar/<int:year>/<int:month>", views.AcompanhamentoVisualizacaoView.as_view(), name="visualizar"),
]

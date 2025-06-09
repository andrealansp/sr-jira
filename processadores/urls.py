from django.urls import path
from processadores import views

app_name = 'processadores'

urlpatterns = [
    path('', views.ProcessadorListView.as_view(), name='listar'),
    path('adicionar', views.ProcessadorCreateView.as_view(), name='adicionar'),
    path('atualizar/<pk>', views.ProcessadorUpdateView.as_view(), name='atualizar'),
    path('deletar/<pk>', views.ProcessadorDeleteView.as_view(), name='deletar'),
    path('acompanhamento', views.AcompanhamentoListView.as_view(), name="listar_acompanhamento"),
    path('acompanhamento/registrar', views.AcompanhamentoCreateView.as_view(), name="registrar_acompanhamento"),
    path('acompanhamento/atualizar/<pk>', views.AcompanhamentoUpdateView.as_view(), name="atualizar_acompanhamento"),
    path('acompanhamento/deletar/<pk>', views.AcompanhamentoDeleteView.as_view(), name="deletar_acompanhamento"),
    path('acompanhamento/relatorio/<int:year>/<int:month>',views.AcompanhamentoRelatorioView.as_view(), name="acompanhamento_relatorio"),
    path("acompanhamento/visualizar/<int:year>/<int:month>", views.AcompanhamentoVisualizacaoView.as_view(), name="acompanhamento_visualizar"),
]

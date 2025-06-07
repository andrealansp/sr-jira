from django.urls import path
from processadores import views

app_name = 'processadores'

urlpatterns = [
    path('', views.ProcessadorListView.as_view(), name='listar'),
    path('adicionar', views.ProcessadorCreateView.as_view(), name='adicionar'),
    path('atualizar/<pk>', views.ProcessadorUpdateView.as_view(), name='atualizar'),
    path('deletar/<pk>', views.ProcessadorDeleteView.as_view(), name='deletar'),
]

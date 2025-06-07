from django.urls import path
from processadores import views

app_name = 'processadores'

urlpatterns = [
    path('', views.ProcessadorListView.as_view(), name='lista'),
    path('adicionar', views.ProcessadorCreateView.as_view(), name='adicionar'),
]

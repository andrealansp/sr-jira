from django.urls import path
from acompanhamento import views


urlpatterns = [
    path('', views.Acompanhamento.as_view(), name='preventivas'),
]

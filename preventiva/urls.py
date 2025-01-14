from django.urls import path

from preventiva.views import (
    PreventivasView,
    PerkonsFormView,
    PerkonsRelatorioTemplateView,
    VelsisFormView,
    VelsisRelatorioTemplateView, SalasFormView, SalasRelatorioTemplateView,
    EstatisticasPreventivasAPIView)

urlpatterns = [
    path('', PreventivasView.as_view(), name='preventivas'),
    path('perkons/', PerkonsFormView.as_view(), name='preventivas_perkons'),
    path('perkons/relatorio/<str:di>/<str:df>',
         PerkonsRelatorioTemplateView.as_view(),
         name="perkons_relatorio"),
    path('velsis/', VelsisFormView.as_view(), name='preventivas_velsis'),
    path('velsis/relatorio/<str:di>/<str:df>',
         VelsisRelatorioTemplateView.as_view(),
         name="velsis_relatorio"),
    path('salas/', SalasFormView.as_view(), name='preventivas_salas'),
    path('salas/relatorio/<str:di>/<str:df>',
         SalasRelatorioTemplateView.as_view(),
         name="salas_relatorio"),
    path('estatisticas', EstatisticasPreventivasAPIView.as_view(), name='resume')
]

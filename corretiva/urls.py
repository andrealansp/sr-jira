from django.urls import path

from corretiva.views import CorretivaTemplateView, RmgvFormView, RmgvListView, ForaDivisaFormView, ForaDivisaListView, \
    ExportRmgvView, ExportForaDivisa

urlpatterns = [
    path('', CorretivaTemplateView.as_view(), name="corretivas"),
    path('rmgv', RmgvFormView.as_view(), name="rmgv"),
    path('rmgv/<str:di>/<str:df>', RmgvListView.as_view(), name="rmgv_lista"),
    path('rmgv/export/<str:di>/<str:df>', ExportRmgvView.as_view(), name="rmgv_export"),
    path('fora_divisa', ForaDivisaFormView.as_view(), name="fora_divisa"),
    path('fora_divisa/<str:di>/<str:df>', ForaDivisaListView.as_view(), name="fora_divisa_lista"),
    path('fora_divisa/export/<str:di>/<str:df>', ExportForaDivisa.as_view(), name="fora_divisa_export"),
]

from django.db import models

class Painel(models.Model):

    data_registro = models.DateTimeField("Data Registro",auto_created=True)
    ponto = models.CharField("Ponto",max_length=5)
    ip = models.GenericIPAddressField()
    status = models.CharField("Status",max_length=11)
    uptime = models.CharField("Uptime",max_length=31)

    class Meta:
        verbose_name = "Painel"
        verbose_name_plural = "Painéis"
        ordering = ['ponto',"data_registro"]

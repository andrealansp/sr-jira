from django.db import models


class Cameras(models.Model):
    ponto = models.CharField(max_length=6)
    regiao = models.CharField(max_length=50)
    nome_ponto = models.CharField(max_length=100)
    ip = models.GenericIPAddressField()
    nome_camera = models.CharField(unique=True, max_length=150)
    firmware = models.CharField(max_length=50, blank=True, null=True)
    serial = models.CharField(max_length=50, blank=True, null=True)
    porta = models.CharField(max_length=6)
    modelo = models.CharField(max_length=150, blank=True, null=True)
    longitude = models.CharField(max_length=10, blank=True, null=True)
    latitude = models.CharField(max_length=10, blank=True, null=True)
    atualizado = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "cameras"
        ordering = ["ponto"]

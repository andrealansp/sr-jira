from django.db import models

class Processador(models.Model):

    identificacao = models.CharField('Nome', max_length=10)
    serie = models.CharField('Serie', max_length=10, null=False, blank=False)
    numero_processador = models.CharField('Numero Processador', max_length=10)
    faixa = models.IntegerField()
    endereco = models.CharField('Endereco', max_length=250)
    latitude = models.CharField('Latitude', max_length=10)
    longitude = models.CharField('Longitude', max_length=10)
    velocidade = models.CharField('Velocidade', max_length=3)
    municipio = models.CharField('Municipio', max_length=100)
    regional = models.CharField('Regional', max_length=50)
    fabricante = models.CharField('Fabricante', max_length=20)
    cliente = models.CharField('Cliente', max_length=250)
    centro_custo = models.CharField('Centro custo', max_length=100)
    modelo = models.CharField('Modelo', max_length=100)
    tipo = models.CharField('Tipo', max_length=100)



    class Meta:
        verbose_name = "Processador"
        verbose_name_plural = "Processadores"
        ordering = ["-identificacao"]


    def __str__(self):
        return f"{self.identificacao} - {self.cliente}"
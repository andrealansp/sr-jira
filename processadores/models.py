import datetime

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


class Acompanhamento(models.Model):

    id_processador = models.ForeignKey(Processador, on_delete=models.CASCADE, related_name='acompanhamento')
    data_inicial = models.DateTimeField("Data Inicial", null=False, blank=False)
    data_final = models.DateTimeField("Data Final", null=False, blank=False)
    problema_apresentado = models.TextField("Problema Apresentado", null=False, blank=False)
    acao_tomada = models.TextField("Ação Tomada", null=False, blank=False)
    status_sla = models.CharField('Status', max_length=10, choices=[("dentro","DENTRO"),("fora","FORA")],default="fora")
    duracao = models.DurationField(editable=False,null=True,blank=True,
                                               help_text="Duração total da ocorrência (calculado automaticamente)")

    class Meta:
        verbose_name = "Acompanhamento"
        verbose_name_plural = "Acompanhamentos"
        ordering = ["-data_inicial"]

    def save(self, *args, **kwargs):
        # Verifica se ambas as datas foram definidas para poder calcular a diferença
        if self.data_inicial and self.data_final:
            # Garante que a data final não seja anterior à inicial
            if self.data_final > self.data_inicial:
                self.duracao = self.data_final - self.data_inicial
            else:
                # Opcional: define a duração como zero se as datas forem inválidas
                self.duracao = datetime.timedelta(days=0)

                # Chama o método save() original para salvar o objeto no banco de dados
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.id_processador.identificacao}-{self.data_inicial}'
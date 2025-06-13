from datetime import datetime

from django.db import models

from processadores.models import Processador


class Acompanhamento(models.Model):
    id_processador = models.ForeignKey(Processador, on_delete=models.CASCADE, related_name='acompanhamento', verbose_name="Procesador")
    data_inicial = models.DateTimeField("Data Inicial", null=False, blank=False, help_text="Data inicial da ocorrência")
    data_final = models.DateTimeField("Data Final", null=False, blank=False, help_text="Data final da ocorrência")
    problema_apresentado = models.TextField("Problema Apresentado", null=False, blank=False,
                                            help_text="Problema apresentado pelo equipamento")
    acao_tomada = models.TextField("Ação Tomada", null=False, blank=False,
                                   help_text="Ação realizada para retorno do equipamento")
    status_sla = models.CharField('Status do SLA', max_length=10,
                                  choices=[("dentro", "DENTRO DO PRAZO"), ("fora", "FORA DO PRAZO")], default="fora",
                                  help_text="Essa ocorrência durou mais que 1 dia ? se sim, fora do prazo, caso contrário, dentro do prazo.")
    duracao = models.DurationField(editable=False, null=True, blank=True,
                                   help_text="Duração total da ocorrência (calculado automaticamente)")

    class Meta:
        verbose_name = "Acompanhamento"
        verbose_name_plural = "Acompanhamentos"
        ordering = ["data_inicial"]

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
        return f'{self.id_processador_id}-{self.id_processador.identificacao}-{self.data_inicial}'

from django import forms

from processadores.models import Processador
from .models import Acompanhamento

class AcompanhamentoForm(forms.ModelForm):
    class Meta:
        model = Acompanhamento
        fields = "__all__"
        widgets = {
            'data_inicial': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'data_final': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class AcompanhamentoFilterForm(forms.Form):
    ANOS_CHOICES = [(ano, str(ano)) for ano in Acompanhamento.get_anos_disponiveis()]
    ANOS_CHOICES.insert(0, ('', 'Todos os Anos'))
    MESES_CHOICES = [(mes, str(mes)) for mes in Acompanhamento.get_meses_disponiveis()]
    MESES_CHOICES.insert(0, ('', 'Todos os Meses'))
    ano = forms.ChoiceField(choices=ANOS_CHOICES, required=False)
    mes = forms.ChoiceField(choices=MESES_CHOICES, required=False)
    processador = forms.ModelChoiceField(queryset=Processador.objects.all(), required=False)


from django import forms

from .models import Acompanhamento

class AcompanhamentoForm(forms.ModelForm):
    class Meta:
        model = Acompanhamento
        fields = "__all__"
        widgets = {
            'data_inicial': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'data_final': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
from django import forms

class PaineisFilterForm(forms.Form):
    ponto = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),required=False)
    data_registro = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}),required=False)


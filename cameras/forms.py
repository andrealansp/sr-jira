from django import forms

from cameras.models import Cameras


class CameraForm(forms.ModelForm):
    class Meta:
        model = Cameras
        fields = "__all__"

class CameraFilterForm(forms.Form):
    ponto = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),required=False)
    serial = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),required=False)
    regiao = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),required=False)
    nome_camera = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),required=False)


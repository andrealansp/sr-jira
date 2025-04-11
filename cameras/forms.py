from django import forms

from cameras.models import Cameras


class CameraForm(forms.ModelForm):
    class Meta:
        model = Cameras
        fields = "__all__"

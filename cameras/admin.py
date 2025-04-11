from django.contrib import admin
from .models import Cameras


@admin.register(Cameras)
class ColaboradorAdmin(admin.ModelAdmin):
    list_display = ("id", "ponto", "nome_camera")

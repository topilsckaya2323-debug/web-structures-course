from django.contrib import admin
from .models import Asset  # импортируем наш класс

# Регистрируем
admin.site.register(Asset)
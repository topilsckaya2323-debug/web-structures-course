import os
from django import forms
from django.core.exceptions import ValidationError
from .models import Asset

class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        # 👇 ДОБАВИЛИ 'category' В СПИСОК ПОЛЕЙ
        fields = ['title', 'file', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название модели'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
            # 👇 ДОБАВИЛИ WIDGET ДЛЯ КАТЕГОРИИ
            'category': forms.Select(attrs={'class': 'form-control'}),
        }
    
    # Валидация файла
    def clean_file(self):
        file = self.cleaned_data['file']
        ext = os.path.splitext(file.name)[1].lower()
        valid_extensions = ['.glb', '.gltf']
        if ext not in valid_extensions:
            raise ValidationError('Неподдерживаемый формат. Пожалуйста, загрузите .glb или .gltf')
        return file
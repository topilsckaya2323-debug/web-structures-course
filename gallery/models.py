import os
from django.db import models
from django.conf import settings

class Asset(models.Model):
    # Поле "Название" - строка до 200 символов
    title = models.CharField(max_length=200, verbose_name="Название модели")
    
    # Поле для файла 3D-модели
    file = models.FileField(upload_to='3d_assets/', verbose_name="3D файл")
    
    # --- НОВОЕ ПОЛЕ ДЛЯ МИНИАТЮРЫ ---
    # blank=True - разрешаем пустые значения (на случай, если скриншот не удался)
    # null=True - разрешаем NULL в базе данных
    image = models.ImageField(upload_to='thumbnails/', blank=True, null=True, verbose_name="Превью")
    
    # Поле "Дата создания"
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата загрузки")
    
    def __str__(self):
        return self.title
    
    @property
    def file_size_safe(self):
        """Безопасно возвращает размер файла или None если файла нет"""
        try:
            if self.file and os.path.exists(self.file.path):
                return self.file.size
        except (FileNotFoundError, ValueError, OSError):
            return None
        return None
    
    class Meta:
        verbose_name = "3D Модель"
        verbose_name_plural = "3D Модели"






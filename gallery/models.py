# Импортируем базовый класс для создания моделей
from django.db import models

# Создаем класс Asset, который наследуется от models.Model
# Каждый такой класс - это будущая таблица в базе данных
class Asset(models.Model):
    # Поле "Название" - строка до 200 символов
    # CharField - тип данных для короткого текста
    # verbose_name - отображаемое имя в админке
    title = models.CharField(max_length=200, verbose_name="Название модели")
    
    # Поле для файла 3D-модели
    # FileField НЕ хранит файл в БД, только путь к нему
    # upload_to - подпапка в media/ куда будут сохраняться файлы
    # '3d_assets/' - создаст папку media/3d_assets/
    file = models.FileField(upload_to='3d_assets/', verbose_name="3D файл")
    
    # Поле "Дата создания"
    # DateTimeField - тип для даты и времени
    # auto_now_add=True - автоматически ставит текущее время при создании записи
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата загрузки")
    
    # Магический метод для строкового представления объекта
    # Без него в админке будет "Asset object (1)", с ним - название модели
    def __str__(self):
        return self.title
    
    # Класс Meta для дополнительных настроек модели
    class Meta:
        # Как будет называться одна запись в админке
        verbose_name = "3D Модель"
        # Как будет называться раздел с записями
        verbose_name_plural = "3D Модели"
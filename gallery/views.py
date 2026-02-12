from django.contrib import messages #ДОМАШНЯЯ РАБОТА
from django.shortcuts import render, redirect  # Добавляем redirect
from django.contrib import messages  # Для сообщений об успехе (бонус)
from .models import Asset
from .forms import AssetForm  # Импортируем форму

def home(request):
    # ORM запрос: "Дай мне все объекты Asset из базы"
    assets = Asset.objects.all().order_by('-created_at')
    
    context_data = {
        'page_title': 'Главная Галерея',
        'assets': assets,  # передаем реальный QuerySet (список)
    }
    return render(request, 'gallery/index.html', context_data)

def about(request):
    """Страница 'О нас'"""
    context = {
        'page_title': 'О нас',
    }
    return render(request, 'gallery/about.html', context)

def upload(request):
    """Страница загрузки моделей"""
    if request.method == 'POST':
        # Сценарий: Пользователь нажал "Отправить"
        # ВАЖНО: передаем request.FILES, иначе файл потеряется!
        form = AssetForm(request.POST, request.FILES)
        if form.is_valid():
            # Если все поля заполнены верно - сохраняем в БД
            form.save()
            # Бонус: добавляем сообщение об успехе
            messages.success(request, 'Модель успешно загружена!')
            # Перекидываем пользователя на главную
            return redirect('home')
    else:
        # Сценарий: Пользователь просто зашел на страницу (GET)
        form = AssetForm()  # Создаем пустую форму
    
    # Отдаем шаблон, передавая туда форму
    return render(request, 'gallery/upload.html', {'form': form})
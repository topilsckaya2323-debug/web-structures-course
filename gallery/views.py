from django.contrib import messages
from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Asset
from .forms import AssetForm
import base64
from django.core.files.base import ContentFile
from django.utils import timezone
from datetime import timedelta
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

# Словарь с категориями (вынес отдельно, чтобы использовать везде)
CATEGORY_CHOICES = [
    ('animals', 'Животные'),
    ('characters', 'Персонажи'),
    ('vehicles', 'Техника'),
    ('nature', 'Природа'),
    ('fantasy', 'Фэнтези'),
    ('other', 'Другое'),
]

def home(request):
    # Получаем параметры из URL
    search_query = request.GET.get('q', '')
    ordering = request.GET.get('ordering', 'new')
    days_param = request.GET.get('days')
    category_filter = request.GET.get('category', '')  # 👈 Фильтр по категории

    # Базовый запрос
    assets = Asset.objects.all()

    # Поиск по названию
    if search_query:
        assets = assets.filter(title__icontains=search_query)

    # 👇 ФИЛЬТР ПО КАТЕГОРИИ
    if category_filter:
        assets = assets.filter(category=category_filter)

    # Фильтр по дате
    if days_param:
        try:
            days = int(days_param)
            filter_date = timezone.now() - timedelta(days=days)
            assets = assets.filter(created_at__gte=filter_date)
        except ValueError:
            pass

    # Сортировка
    if ordering == 'old':
        assets = assets.order_by('created_at')
    elif ordering == 'name':
        assets = assets.order_by('title')
    else:
        assets = assets.order_by('-created_at')

    # Пагинация
    paginator = Paginator(assets, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # 👇 СЧИТАЕМ КОЛИЧЕСТВО МОДЕЛЕЙ В КАЖДОЙ КАТЕГОРИИ
    categories_count = {}
    for cat_value, cat_name in CATEGORY_CHOICES:
        count = Asset.objects.filter(category=cat_value).count()
        if count > 0:  # Показываем только категории, где есть модели
            categories_count[cat_value] = {
                'name': cat_name,
                'count': count
            }
    total_models_count = Asset.objects.count()
    # Контекст для шаблона
    context_data = {
        'page_title': 'Julka3D Gallery',
        'page_obj': page_obj,
        'categories': categories_count,           # 👈 Для кнопок категорий
        'current_category': category_filter,      # 👈 Текущая выбранная категория
        'search_query': search_query,
        'ordering': ordering,
        'days': days_param,
        'total_models_count': total_models_count,
    }
    return render(request, 'gallery/index.html', context_data)


def about(request):
    """Страница 'О нас'"""
    context = {
        'page_title': 'О нас',
    }
    return render(request, 'gallery/about.html', context)

@login_required
def upload(request):
    if request.method == 'POST':
        form = AssetForm(request.POST, request.FILES)
        if form.is_valid():
            # Создаем объект, но пока НЕ сохраняем в базу
            new_asset = form.save(commit=False)
            
            # Обрабатываем картинку из скрытого поля
            image_data = request.POST.get('image_data')
            if image_data:
                format, imgstr = image_data.split(';base64,')
                ext = format.split('/')[-1]
                data = base64.b64decode(imgstr)
                file_name = f"{new_asset.title}_thumb.{ext}"
                new_asset.image.save(file_name, ContentFile(data), save=False)
            
            # Финальное сохранение
            new_asset.save()
            
            messages.success(request, f'Модель "{new_asset.title}" успешно загружена!')
            return redirect('home')
    else:
        form = AssetForm()
    
    return render(request, 'gallery/upload.html', {'form': form})
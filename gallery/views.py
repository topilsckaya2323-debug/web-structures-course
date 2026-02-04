from django.shortcuts import render

def home(request):
    # ВСЁ ВНУТРИ ФУНКЦИИ ДОЛЖНО БЫТЬ С ОТСТУПОМ (4 пробела или Tab)
    fake_database = [
        {'id': 1, 'name': 'Sci-Fi Helmet', 'file_size': '15 MB'},
        {'id': 2, 'name': 'Old Chair', 'file_size': '2 MB'},
        {'id': 3, 'name': 'Cyber Truck', 'file_size': '10 MB'},
        {'id': 4, 'name': 'Egor Monkey', 'file_size': '2 MB'},

    ]
    
    context_data = {
        'page_title': 'Главная Галерея',
        'models_count': len(fake_database),
        'assets': fake_database,
    }
    
    return render(request, 'gallery/index.html', context_data)
def about(request):
    """Страница "О проекте" """
    context = {
        'page_title': 'О проекте',
        'author_name': '[SAKURA]',  # Замените на своё имя
        'course_name': 'Web Структуры'
    }
    return render(request, 'gallery/about.html', context)

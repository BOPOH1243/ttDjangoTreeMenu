from django.shortcuts import render, get_object_or_404
from menu.models import MenuItem

def index(request):
    # простая «главная»
    return render(request, 'page.html', {'title': 'Home'})

def page(request, title):
    # проверяем, что такой пункт меню есть (иначе 404)
    get_object_or_404(MenuItem, title=title)
    return render(request, 'page.html', {'title': title})

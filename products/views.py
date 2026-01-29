from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from .models import Product

def product_list(request):
    products = Product.objects.filter(is_available=True).order_by('-created_at')
    return render(request, 'products/list.html', {'products': products})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_available=True)
    return render(request, 'products/detail.html', {'product': product})

def filter_products(request):
    """
    View для AJAX-фильтрации товаров.
    Возвращает HTML с отфильтрованными карточками товаров.
    """
    # 1. Получаем параметры из запроса
    price_min = request.GET.get('price_min', '')
    price_max = request.GET.get('price_max', '')
    conditions = request.GET.getlist('condition[]')  # Список: ['new', 'used']
    availability = request.GET.get('availability', '')

    # 2. Начинаем с базового QuerySet всех доступных товаров
    products = Product.objects.filter(is_available=True)

    # 3. Применяем фильтры, если они указаны
    # Фильтр по цене (мин)
    if price_min:
        products = products.filter(price__gte=float(price_min))
    # Фильтр по цене (макс)
    if price_max:
        products = products.filter(price__lte=float(price_max))

    # Фильтр по состоянию (если выбраны оба или ни одного — фильтр не применяем)
    if conditions and len(conditions) < 2:
        # Если выбран только один вариант
        products = products.filter(condition__in=conditions)

    # Фильтр по наличию (если снята галочка "В наличии")
    if availability != 'available':
        # Если галочка снята, показываем все (включая отсутствующие)
        products = Product.objects.all()  # Переопределяем QuerySet

    # Сортировка по новизне
    products = products.order_by('-created_at')

    # 4. Рендерим HTML-фрагмент с карточками
    html = render_to_string('products/_product_items.html', {'products': products})

    # 5. Возвращаем JSON с HTML
    return JsonResponse({'html': html, 'count': products.count()})
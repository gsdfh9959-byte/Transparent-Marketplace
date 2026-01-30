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
    from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import Cart, CartItem, Product, Favorite  # Добавляем импорт новых моделей

# ... предыдущий код (product_list, product_detail, filter_products) ...

# ========== VIEWS ДЛЯ КОРЗИНЫ ==========

@login_required  # Только для авторизованных пользователей
def add_to_cart(request, product_id):
    """Добавляет товар в корзину пользователя."""
    product = get_object_or_404(Product, id=product_id)
    
    # Получаем или создаём корзину для текущего пользователя
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Получаем или создаём элемент корзины
    cart_item, item_created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': 1}
    )
    
    # Если элемент уже был в корзине, увеличиваем количество
    if not item_created:
        cart_item.quantity += 1
        cart_item.save()
    
    # Возвращаем JSON-ответ для AJAX
    return JsonResponse({
        'success': True,
        'message': f'Товар "{product.title}" добавлен в корзину.',
        'cart_items_count': cart.items.count()
    })

@login_required
def remove_from_cart(request, item_id):
    """Удаляет товар из корзины (или уменьшает количество)."""
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    
    if cart_item.quantity > 1:
        # Если больше 1 штуки, уменьшаем количество
        cart_item.quantity -= 1
        cart_item.save()
        message = f'Количество товара "{cart_item.product.title}" уменьшено.'
    else:
        # Если 1 штука — удаляем позицию
        cart_item.delete()
        message = f'Товар "{cart_item.product.title}" удалён из корзины.'
    
    # Возвращаем JSON-ответ
    return JsonResponse({
        'success': True,
        'message': message,
        'cart_items_count': Cart.objects.get(user=request.user).items.count()
    })

@login_required
def view_cart(request):
    """Отображает страницу корзины (создадим позже)."""
    cart = get_object_or_404(Cart, user=request.user)
    items = cart.items.all()
    return render(request, 'products/cart.html', {'cart': cart, 'items': items})

# ========== VIEWS ДЛЯ ИЗБРАННОГО ==========

@login_required
def toggle_favorite(request, product_id):
    """Добавляет или удаляет товар из избранного."""
    product = get_object_or_404(Product, id=product_id)
    
    # Пытаемся найти товар в избранном у пользователя
    favorite, created = Favorite.objects.get_or_create(
        user=request.user,
        product=product
    )
    
    if not created:
        # Если запись уже существовала — удаляем (переключаем)
        favorite.delete()
        is_favorite = False
        message = f'Товар "{product.title}" удалён из избранного.'
    else:
        # Если создали новую запись — добавили
        is_favorite = True
        message = f'Товар "{product.title}" добавлен в избранное.'
    
    return JsonResponse({
        'success': True,
        'message': message,
        'is_favorite': is_favorite
    })
    from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect

# ... предыдущий код ...

def signup(request):
    """Регистрация нового пользователя."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Автоматически входим после регистрации
            return redirect('product_list')  # Перенаправляем на главную
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
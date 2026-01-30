from django.urls import path
from . import views

urlpatterns = [
    # ������� �������� �� ������� �������
    path('', views.product_list, name='product_list'),
    # ��������� �������� ������
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    # НОВЫЙ ПУТЬ для фильтрации
    path('filter-products/', views.filter_products, name='filter_products'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('filter-products/', views.filter_products, name='filter_products'),
    
    # ========== НОВЫЕ URL ДЛЯ КОРЗИНЫ И ИЗБРАННОГО ==========
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('favorite/toggle/<int:product_id>/', views.toggle_favorite, name='toggle_favorite'),
]
path('signup/', views.signup, name='signup'),
from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('filter-products/', views.filter_products, name='filter_products'),
    
    # Корзина и избранное
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('favorite/toggle/<int:product_id>/', views.toggle_favorite, name='toggle_favorite'),
    
    # Регистрация
    path('signup/', views.signup, name='signup'),  # ДОБАВЬ ЭТУ СТРОКУ
]
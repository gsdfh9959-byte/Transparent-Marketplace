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
from django.contrib import admin
from .models import Product, ProductImage, Cart, CartItem, Favorite  # Добавил новые модели

# Класс для отображения фото внутри товара в админке
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3  # Сколько пустых полей для фото показывать
    fields = ['image', 'uploaded_at']
    readonly_fields = ['uploaded_at']

# Регистрируем Product с встроенными фото
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'condition', 'price', 'is_available', 'created_at']
    list_filter = ['condition', 'is_available']
    search_fields = ['title', 'description']
    inlines = [ProductImageInline]  # Это добавляет блок фото к товару
    
# Регистрируем отдельно ProductImage (опционально)
@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'image', 'uploaded_at']
    list_filter = ['uploaded_at']

# ========== РЕГИСТРАЦИЯ НОВЫХ МОДЕЛЕЙ (Корзина и Избранное) ==========

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at', 'updated_at']
    list_filter = ['created_at']

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product', 'quantity']
    list_filter = ['cart']

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'added_at']
    list_filter = ['added_at']
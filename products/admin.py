from django.contrib import admin
from .models import Product, ProductImage

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
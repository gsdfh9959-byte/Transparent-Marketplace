from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    # Основные поля
    seller = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Продавец")
    title = models.CharField(max_length=200, verbose_name="Название товара")
    
    # Состояние: новое или б/у
    CONDITION_CHOICES = [
        ('new', 'Новый'),
        ('used', 'Б/У'),
    ]
    condition = models.CharField(
        max_length=10, 
        choices=CONDITION_CHOICES, 
        default='new',
        verbose_name="Состояние"
    )
    
    # Цена (Decimal для точности с деньгами)
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name="Цена"
    )
    
    # Описание
    description = models.TextField(verbose_name="Описание")
    
    # Поле для недостатков (ОБЯЗАТЕЛЬНО для Б/У)
    flaws = models.TextField(
        blank=True, 
        verbose_name="Недостатки и дефекты",
        help_text="Подробно опишите все царапины, сколы, потёртости"
    )
    
    # Наличие
    is_available = models.BooleanField(default=True, verbose_name="В наличии")
    
    # Даты
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title


# ====== НОВАЯ МОДЕЛЬ ДЛЯ ФОТО ======
# ОТДЕЛЬНЫЙ класс, НЕ внутри класса Product!

class ProductImage(models.Model):
    """Модель для хранения нескольких изображений товара"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/', verbose_name="Изображение")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Image for {self.product.title}"
    
    class Meta:
        ordering = ['uploaded_at']
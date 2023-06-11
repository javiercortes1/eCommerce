from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone

# Create your models here.

#categorias para producto
class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=200)
    image = models.ImageField(upload_to="categories/", blank=True, null=True)

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        sin_categoria, _ = Category.objects.get_or_create(name='Sin categoría', defaults={'description': 'Categoría predeterminada para productos sin categoría'})
        products = self.product_set.all()
        for product in products:
            product.category = sin_categoria
            product.save()
        super().delete(*args, **kwargs)

#producto
class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField()
    description = models.TextField(max_length=200)
    is_new = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    stock = models.IntegerField()
    is_featured = models.BooleanField(default=False)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_rentable = models.BooleanField(default=False)

    def __str__(self):
        return self.name

#tipo de consulta
class QueryType(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=200)

    def __str__(self):
        return self.name

#consulta
class Contact(models.Model):
    STATUS_CHOICES = (
        ('Nuevo', 'Nuevo'),
        ('En progreso', 'En progreso'),
        ('Finalizado', 'Finalizado'),
    )

    name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.IntegerField()
    message = models.TextField(max_length=200)
    query_type = models.ForeignKey(QueryType, on_delete=models.PROTECT)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Nuevo')

    def __str__(self):
        return self.name
    
class RentalOrder(models.Model):
    rut = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    deliver_date = models.DateTimeField()
    products = models.ManyToManyField(Product)

    def __str__(self):
        return self.name

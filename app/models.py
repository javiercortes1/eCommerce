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
    new = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    stock = models.IntegerField()
    featured = models.BooleanField(default=False)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

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
    queryType = models.ForeignKey(QueryType, on_delete=models.PROTECT)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Nuevo')

    def __str__(self):
        return self.name

# modelo para objeto arrendable
class RentableProduct(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField()
    description = models.TextField(max_length=200)
    stock = models.IntegerField()
    image = models.ImageField(upload_to='rentable_products/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# modelo para el arriendo
class Rental(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rentables = models.ManyToManyField(RentableProduct)
    status = models.CharField(max_length=20)
    deposit_paid = models.BooleanField(default=False)
    delivery_date = models.DateField()

    def __str__(self):
        return f"{self.user.username} - Rental {self.pk}"
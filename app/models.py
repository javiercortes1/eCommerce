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
    name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.IntegerField()
    message = models.TextField(max_length=200)
    queryType = models.ForeignKey(QueryType, on_delete=models.PROTECT)

    def __str__(self):
        return self.name

# modelo para objeto arrendable
class Rentable(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=200)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# modelo para el arriendo
class Rental(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rentables = models.ManyToManyField(Rentable)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20)
    deposit_paid = models.BooleanField(default=False)

    def clean(self):
        if self.start_date > self.end_date:
            raise ValidationError(
                "La fecha de inicio no puede ser posterior a la fecha de finalización.")

    def get_duration(self):
        return (self.end_date - self.start_date).days

    @property
    def is_active(self):
        today = timezone.now().date()
        return self.start_date <= today <= self.end_date

    def __str__(self):
        return f"{self.user.username} - Rental {self.pk}"
    
class Usuarios(models.Model):
    usrN= models.CharField(max_length=30,verbose_name="Nombre de Usuario")
    pswrdN= models.CharField(max_length=15, verbose_name="Contraseña")
    pswrdN2=models.CharField(max_length=15, verbose_name="Contraseña2")
#fin modelos para usuarios

#se crea modelo de token
class Tokens(models.Model):
    token= models.CharField(max_length=256)
    user = models.CharField(max_length=256)    
from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=200)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField()
    description = models.TextField(max_length=200)
    new = models.BooleanField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    cc = models.IntegerField()
    stock = models.IntegerField()

    def __str__(self):
        return self.name
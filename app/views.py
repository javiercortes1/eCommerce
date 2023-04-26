from django.shortcuts import render
from .models import Product

# Create your views here.
def home(request):
    products = Product.objects.all()
    data = {
        'products': products
    }
    return render(request, 'app/home.html', data)

def catalogue(request):
    return render(request, 'app/catalogue.html')

def services(request):
    return render(request, 'app/services.html')

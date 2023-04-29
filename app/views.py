from django.shortcuts import render
from .models import Product
from .forms import ContactForm, ProductForm

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

def contact(request):
    data = {
        'form': ContactForm()
    }

    if request.method == 'POST':
        form = ContactForm(data=request.POST)
        if form.is_valid():
            form.save()
            data["message"] = "Enviado exitosamente"
        else:
            data["form"] = form
    return render(request, 'app/contact.html', data)

def add_product(request):

    data = {
        'form': ProductForm()
    }

    if request.method == 'POST':
        form = ProductForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            data["message"] = "Agregado exitosamente"
        else:
            data["form"] = form
    return render(request, 'app/product/add.html',data)

def list_product(request):
    products = Product.objects.all()
    data = {
        'products': products
    }
    return render(request, 'app/product/list.html', data)
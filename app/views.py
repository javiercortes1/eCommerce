from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category
from .forms import ContactForm, ProductForm
from django.contrib import messages
from django.core.paginator import Paginator

# Create your views here.
def home(request):
    products = Product.objects.all()
    data = {
        'products': products
    }
    return render(request, 'app/home.html', data)

def catalogue(request):
    products = Product.objects.all()
    data = {
        'products': products
    }
    return render(request, 'app/catalogue.html',data)

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
            messages.success(request, "Producto Agregado")
            return redirect(to="list_product")
        else:
            data["form"] = form
    return render(request, 'app/product/add.html',data)

def list_product(request):
    products = Product.objects.all()
    page = request.GET.get('page', 1)


    data = {
        'products': products
    }
    return render(request, 'app/product/list.html', data)

def update_product(request, id):

    product = get_object_or_404(Product, id=id)

    data = {
        'form':ProductForm(instance=product)
    }

    if request.method == 'POST':
        form = ProductForm(data=request.POST, instance=product, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Modificado correctamente")
            return redirect(to="list_product")
        data["form"] = form


    return render(request, 'app/product/update.html',data)

def delete_product(request, id):
    product = get_object_or_404(Product, id=id)
    product.delete()
    messages.success(request, "Eliminado correctamente")
    return redirect(to="list_product")

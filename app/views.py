from django.shortcuts import render, redirect, get_object_or_404
from .forms import ContactForm, ProductForm, CustomUserCreationForm, CategoryForm, RentalForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .models import Product, Category, Rental, Contact
from django.core.paginator import Paginator, EmptyPage
from django.http import Http404
from rest_framework import viewsets, generics
from .serializers import ProductSerializer, CategorySerializer, ContactSerializer
import requests
from django.contrib.auth.decorators import login_required, permission_required
from django.core.cache import cache
from app.cart import Cart
from django.core.mail import send_mail
from django.db.models import Q
from datetime import date
from rest_framework.response import Response
from django.conf import settings
import json
import base64
from django.core.files.uploadedfile import InMemoryUploadedFile
import io
import logging
from django.http import QueryDict
from django.utils.datastructures import MultiValueDict

# Create your views here.


class CategoryViewset(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewset(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        products = Product.objects.all()

        name = self.request.GET.get('name')
        featured = self.request.GET.get('featured')
        category = self.request.GET.get('category')
        new = self.request.GET.get('new')
        min_price = self.request.GET.get('min_price_filter')
        max_price = self.request.GET.get('max_price_filter')

        if name:
            products = products.filter(name__contains=name)
        if featured:
            products = products.filter(featured=True)
        if category:
            products = products.filter(category=category)
        if new:
            products = products.filter(new=True)
        if min_price and max_price:
            products = products.filter(price__range=(min_price, max_price))
        elif min_price:
            products = products.filter(price__gte=min_price)
        elif max_price:
            products = products.filter(price__lte=max_price)

        return products
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)
    
    def perform_create(self, serializer):
        serializer.save()
    
class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        contact = serializer.save()  # Utilizar el método save() del serializador

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)


def home(request):
    params = {
        'featured': True,
        'new': True
    }
    
    response = requests.get(settings.API_BASE_URL + 'product/', params=params).json()
    
    data = {
        'products': response
    }
    
    return render(request, 'app/home.html', data)


def catalogue(request):
    name_filter = request.GET.get('name', '')
    category_filter = request.GET.get('category', '')
    min_price_filter = request.GET.get('min_price_filter', '')
    max_price_filter = request.GET.get('max_price_filter', '')

    api_url = 'http://127.0.0.1:8000/api/product/'

    params = {
        'name': name_filter,
        'category': category_filter,
        'min_price_filter': min_price_filter,
        'max_price_filter': max_price_filter,
    }

    response = requests.get(api_url, params=params)
    products = response.json()

    categories = requests.get('http://127.0.0.1:8000/api/category/').json()

    if 'clear_filters' in request.GET:
        response = requests.get('http://127.0.0.1:8000/api/product/').json()
        products = response

    data = {
        'products': products,
        'categories': categories,
    }

    return render(request, 'app/catalogue.html', data)


def services(request):

    return render(request, 'app/services.html')


def contact(request):
    data = {
        'form': ContactForm()
    }

    return render(request, 'app/contact.html', data)

# product


# @permission_required('app.add_product')
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            # Obtener los datos del formulario
            name = form.cleaned_data['name']
            price = form.cleaned_data['price']
            description = form.cleaned_data['description']
            new = form.cleaned_data['new']
            category_id = form.cleaned_data['category'].id  # Obtener el ID de la categoría
            stock = form.cleaned_data['stock']
            featured = form.cleaned_data['featured']
            image = form.cleaned_data['image']

            # Crear un diccionario con los datos del producto
            product_data = {
                'name': name,
                'price': price,
                'description': description,
                'new': new,
                'category': category_id,  # Usar el ID de la categoría
                'stock': stock,
                'featured': featured,
            }

            # Realizar una solicitud POST a la API para crear el producto
            response = requests.post(
                settings.API_BASE_URL + 'product/',
                data=product_data,  # Enviar los datos como formulario
                files={'image': image}  # Adjuntar el archivo de imagen
            )

            if response.status_code == 201:
                print('Producto creado exitosamente')
                return redirect('list_product')
            else:
                # Manejar el caso de error en la solicitud
                print(f'Error al crear el producto: {response.content}')
                error_message = "Error al crear el producto a través de la API"
        else:
            error_message = "Error en los datos del formulario"
        data = {
            'form': form,
            'error_message': error_message
        }
    else:
        data = {
            'form': ProductForm()
        }
    return render(request, 'app/product/add.html', data)


# @permission_required('app.view_product')
def list_product(request):
    response = requests.get(settings.API_BASE_URL + 'product/')
    products = response.json()
    page = request.GET.get('page', 1)

    try:
        paginator = Paginator(products, 5)
        products = paginator.page(page)
    except:
        raise Http404

    data = {
        'entity': products,
        'paginator': paginator
    }
    return render(request, 'app/product/list.html', data)


#@permission_required('app.change_product')
def update_product(request, id):
    product = get_object_or_404(Product, id=id)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            name = form.cleaned_data['name']
            existing_product = Product.objects.exclude(id=id).filter(name__iexact=name).first()
            if existing_product:
                if existing_product.id != product.id:
                    form.add_error('name', 'Este producto ya existe')
                    error_message = "Este producto ya existe"  # Agregar definición de error_message
            else:
                price = form.cleaned_data['price']
                description = form.cleaned_data['description']
                new = form.cleaned_data['new']
                category_id = form.cleaned_data['category'].id
                stock = form.cleaned_data['stock']
                featured = form.cleaned_data['featured']
                image = form.cleaned_data['image']

                product_data = {
                    'name': name,
                    'price': price,
                    'description': description,
                    'new': new,
                    'category': category_id,
                    'stock': stock,
                    'featured': featured,
                }

                response = requests.put(
                    settings.API_BASE_URL + f'product/{id}/',
                    data=product_data,
                    files={'image': image}
                )

                if response.status_code == 200:
                    print('Producto actualizado exitosamente')
                    messages.success(request, "Modificado correctamente")
                    return redirect(to="list_product")
                else:
                    print(f'Error al actualizar el producto: {response.content}')
                    error_message = "Error al actualizar el producto a través de la API"
        else:
            error_message = "Error en los datos del formulario"
    else:
        form = ProductForm(instance=product)
        error_message = ""

    data = {
        'form': form,
        'error_message': error_message
    }

    return render(request, 'app/product/update.html', data)

@permission_required('app.delete_product')
def delete_product(request, id):
    product = get_object_or_404(Product, id=id)

    # Realizar una solicitud DELETE a la API para eliminar el producto
    response = requests.delete(settings.API_BASE_URL + f'product/{id}/')

    if response.status_code == 204:
        product.delete()
        messages.success(request, "Eliminado correctamente")
        return redirect(to="list_product")
    else:
        # Manejar el caso de error en la solicitud
        print(f'Error al eliminar el producto: {response.content}')
        error_message = "Error al eliminar el producto a través de la API"
        data = {
            'form': ProductForm(instance=product),
            'error_message': error_message
        }
        return render(request, 'app/product/update.html', data)


def product_detail(request, id):
    # Realizar una solicitud GET a la API para obtener los detalles del producto
    response = requests.get(settings.API_BASE_URL + f'product/{id}/')

    if response.status_code == 200:
        product_data = response.json()
        product = Product(**product_data)
        data = {
            'product': product
        }
        return render(request, 'app/product/detail.html', data)
    else:
        # Manejar el caso de error en la solicitud
        print(f'Error al obtener los detalles del producto: {response.content}')
        error_message = "Error al obtener los detalles del producto a través de la API"
        return render(request, 'app/product/detail.html', {'error_message': error_message})

# register


def register(request):
    data = {
        'form': CustomUserCreationForm()
    }
    if request.method == 'POST':
        formulario = CustomUserCreationForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            user = authenticate(
                username=formulario.cleaned_data["username"], password=formulario.cleaned_data["password1"])
            login(request, user)
            messages.success(request, "Te has registrado correctamente")
            # redirigir al home
            return redirect(to="home")
        data["form"] = formulario
    return render(request, 'registration/register.html', data)

# carrito


def add_prod_cart(request, product_id):
    cart = Cart(request)
    product = Product.objects.get(id=product_id)

    if product.stock <= 0:
        messages.error(request, "Error: Product is out of stock.")
    elif cart.get_product_quantity(product) >= product.stock:
        messages.error(request, "Error: Maximum stock limit reached.")
    else:
        cart.add(product)
        # messages.success(request, "Product added to cart successfully.")

    return redirect(to="Cart")


def del_prod_cart(request, product_id):
    cart = Cart(request)
    product = Product.objects.get(id=product_id)
    cart.delete(product)
    return redirect(to="Cart")


def subtract_product_cart(request, product_id):
    cart = Cart(request)
    product = Product.objects.get(id=product_id)
    cart.subtract(product)
    return redirect("Cart")


def clean_cart(request):
    cart = Cart(request)
    cart.clean()
    return redirect("Cart")


def cart_page(request):
    products = Product.objects.all()
    data = {
        'products': products
    }

    return render(request, 'app/cart_page.html', data)

# def checkout(request):

#     return render(request,'core/checkout.html')


def buy_confirm(request):
    cart = Cart(request)
    cart.buy()
    cart.clean()
    return redirect('cart')

# def pago_exitoso(request):

#     return render(request,'core/pago_exitoso.html')

# Category


@permission_required('app.add_category')
def add_category(request):

    data = {
        'form': CategoryForm()
    }

    if request.method == 'POST':
        form = CategoryForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Categoria Agregada")
            return redirect(to="list_category")
        else:
            data["form"] = form
    return render(request, 'app/category/add.html', data)


@permission_required('app.view_category')
def list_category(request):
    categories = Category.objects.all()
    page = request.GET.get('page', 1)

    try:
        paginator = Paginator(categories, 5)
        categories = paginator.page(page)
    except:
        raise Http404

    data = {
        'entity': categories,
        'paginator': paginator
    }
    return render(request, 'app/category/list.html', data)


@permission_required('app.change_category')
def update_category(request, id):

    category = get_object_or_404(Category, id=id)

    data = {
        'form': CategoryForm(instance=category)
    }

    if request.method == 'POST':
        form = CategoryForm(data=request.POST,
                            instance=category, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Modificado correctamente")
            return redirect(to="list_category")
        data["form"] = form

    return render(request, 'app/category/update.html', data)


@permission_required('app.delete_category')
def delete_category(request, id):
    category = get_object_or_404(Category, id=id)
    category.delete()
    messages.success(request, "Eliminado correctamente")
    return redirect(to="list_category")


def admin_panel(request):

    return render(request, 'app/admin_panel.html')


def list_rental(request):
    rentals = Rental.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(rentals, 5)

    try:
        rentals = paginator.page(page)
    except EmptyPage:
        # Si el número de página es mayor que el número total de páginas,
        # redirigir al usuario a la última página válida
        rentals = paginator.page(paginator.num_pages)

    data = {
        'entity': rentals,
        'paginator': paginator
    }
    return render(request, 'app/rental/list.html', data)


def rental_detail(request, id):
    rental = get_object_or_404(Rental, id=id)

    data = {
        'rental': rental
    }

    return render(request, 'app/rental/detail.html', data)


def add_rental(request):
    data = {
        'form': RentalForm()
    }

    if request.method == 'POST':
        form = RentalForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Arriendo agregado")
            return redirect(to="list_rental")
        else:
            # Mostrar mensajes de error al usuario
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")

            data["form"] = form

    return render(request, 'app/rental/add.html', data)


def update_rental(request, id):
    rental = get_object_or_404(Rental, id=id)

    data = {
        'form': RentalForm(instance=rental)
    }

    if request.method == 'POST':
        form = RentalForm(data=request.POST, instance=rental)
        if form.is_valid():
            form.save()
            messages.success(request, "Arriendo modificado correctamente")
            return redirect(to="list_rental")
        else:
            # Mostrar mensajes de error al usuario
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")

            data["form"] = form

    return render(request, 'app/rental/update.html', data)


def delete_rental(request, id):
    rental = get_object_or_404(Rental, id=id)
    rental.delete()
    messages.success(request, "Eliminado correctamente")
    return redirect(to="list_rental")

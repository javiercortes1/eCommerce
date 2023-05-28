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
    
class ContactAPIView(generics.CreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    def perform_create(self, serializer):
        contact = serializer.save()

        # Obtener los datos del formulario
        name = contact.name
        email = contact.email
        phone = contact.phone
        message = contact.message

        # Construir el mensaje de correo electrónico con los datos del formulario
        subject = 'Nuevo mensaje de contacto'
        email_message = f'''
            Se ha recibido un nuevo mensaje de contacto:
            Nombre: {name}
            Correo electrónico: {email}
            Teléfono: {phone}
            Mensaje: {message}
        '''
        from_email = 'erreapectm@gmail.com'  # Tu dirección de correo electrónico
        # La dirección de correo electrónico del destinatario
        to_email = 'dario.vera96@gmail.com'
        send_mail(subject, email_message, from_email, [to_email])


def home(request):
    # products = Product.objects.all()
    # data = {
    #     'products': products
    # }
    response = requests.get('http://127.0.0.1:8000/api/product/?featured=True&new=True').json()
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

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()

            # Obtener los datos del formulario
            name = contact.name
            email = contact.email
            phone = contact.phone
            message = contact.message

            # Construir el mensaje de correo electrónico con los datos del formulario
            subject = 'Nuevo mensaje de contacto'
            email_message = f'''
                Se ha recibido un nuevo mensaje de contacto:
                Nombre: {name}
                Correo electrónico: {email}
                Teléfono: {phone}
                Mensaje: {message}
            '''
            from_email = 'erreapectm@gmail.com'  # Tu dirección de correo electrónico
            # La dirección de correo electrónico del destinatario
            to_email = 'dario.vera96@gmail.com'
            send_mail(subject, email_message, from_email, [to_email])

            # Redireccionar a la página de éxito o cualquier otra página
            return redirect('contact')

    else:
        form = ContactForm()
    data['form'] = form
    return render(request, 'app/contact.html', data)

# product


@permission_required('app.add_product')
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
    return render(request, 'app/product/add.html', data)


@permission_required('app.view_product')
def list_product(request):
    products = Product.objects.all()
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


@permission_required('app.change_product')
def update_product(request, id):

    product = get_object_or_404(Product, id=id)

    data = {
        'form': ProductForm(instance=product)
    }

    if request.method == 'POST':
        form = ProductForm(data=request.POST,
                           instance=product, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Modificado correctamente")
            return redirect(to="list_product")
        data["form"] = form

    return render(request, 'app/product/update.html', data)


@permission_required('app.delete_product')
def delete_product(request, id):
    product = get_object_or_404(Product, id=id)
    product.delete()
    messages.success(request, "Eliminado correctamente")
    return redirect(to="list_product")


def product_detail(request, id):
    product = get_object_or_404(Product, id=id)

    data = {
        'product': product
    }

    return render(request, 'app/product/detail.html', data)

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

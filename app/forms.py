from django import forms
from .models import Contact, Product, Category, QueryType, Rental, RentableProduct
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django.contrib.auth.forms import UserCreationForm
from .validators import MaxSizeFileValidator
from django.forms import ValidationError
from django.core.validators import validate_email, MinValueValidator
from django.core.exceptions import ValidationError
from django.contrib.admin.widgets import AdminDateWidget


class ContactForm(forms.ModelForm):
    name = forms.CharField(min_length=8, max_length=50,
                           required=True, label='Nombre completo')
    email = forms.EmailField(required=True, label='Correo electrónico')
    phone = forms.IntegerField(
        label='Teléfono', min_value=100000000, max_value=999999999)
    message = forms.CharField(required=True, max_length=200, label='Mensaje', widget=forms.Textarea)
    query_type = forms.ModelChoiceField(
        queryset=QueryType.objects.all(), required=True, label='Tipo de consulta')

    class Meta:
        model = Contact
        fields = ["name", "email", "phone", "message", "query_type"]
        labels = {
            'name': 'Nombre completo',
            'email': 'Correo electrónico',
            'phone': 'Teléfono',
            'message': 'Mensaje',
            'query_type': 'Tipo de consulta'
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            validate_email(email)
        except ValidationError:
            raise forms.ValidationError(
                "El correo electrónico no es válido.")
        return email

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if len(str(phone)) != 9:
            raise forms.ValidationError(
                "El número de teléfono debe contener 9 dígitos.")
        return phone

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        queryType = cleaned_data.get('queryType')
        name = cleaned_data.get('name')
        phone = cleaned_data.get('phone')

        if not email:
            self.add_error('email', 'Este campo es obligatorio.')
        if not queryType:
            self.add_error('queryType', 'Este campo es obligatorio.')
        if name and len(name) < 8:
            self.add_error(
                'name', 'El nombre debe tener al menos 8 caracteres.')
        if phone:
            try:
                cleaned_phone = self.clean_phone()
                cleaned_data['phone'] = cleaned_phone
            except forms.ValidationError as e:
                self.add_error('phone', e.message)

class QueryTypeForm(forms.ModelForm):
    name = forms.CharField(min_length=3, max_length=50)


    class Meta:
        model = QueryType
        fields = '__all__'
        labels = {
            'name': 'Nombre',
            'description': 'Descripcion',
        }

class ProductForm(forms.ModelForm):
    image = forms.ImageField(required=False, validators=[MaxSizeFileValidator(20)])
    name = forms.CharField(min_length=3, max_length=50)
    price = forms.IntegerField(min_value=1, max_value=1500000)
    stock = forms.IntegerField(validators=[MinValueValidator(0)])


    class Meta:
        model = Product
        fields = '__all__'
        labels = {
            'name': 'Nombre',
            'description': 'Descripción',
            'price': 'Precio',
            'category': 'Categoría',
            'stock': 'Unidades',
            'is_new': '¿Nuevo?',
            'is_featured': '¿Destacado?',
            'image': 'Imagen'
        }

class CustomUserCreationForm(UserCreationForm):
    pass

class CategoryForm(forms.ModelForm):

    image = forms.ImageField(required=False, validators=[
                             MaxSizeFileValidator(20)])
    name = forms.CharField(min_length=3, max_length=50)


    class Meta:
        model = Category
        fields = '__all__'
        labels = {
            'name': 'Nombre',
            'description': 'Descripcion',
            'image': 'Imagen'
        }

class RentalForm(forms.ModelForm):
    delivery_date = forms.DateField(widget=AdminDateWidget)

    class Meta:
        model = Rental
        fields = ['user', 'rentables',  'status', 'deposit_paid', 'delivery_date']
        labels = {
            'user': 'Usuario',
            'rentables': 'Arrendables',
            'status': 'Estado',
            'deposit_paid': 'Depósito pagado',
            'delivery_date': 'Fecha de delivery'
        }
        widgets = {
            'user': forms.HiddenInput(),
            'rentables': forms.CheckboxSelectMultiple(),
            'status': forms.HiddenInput(),
            'deposit_paid': forms.HiddenInput()
        }

class RentableProductForm(forms.ModelForm):
    class Meta:
        model = RentableProduct
        fields = ['name', 'price', 'description', 'stock', 'image']
        labels = {
            'name': 'Nombre',
            'price': 'Precio',
            'description': 'Descripción',
            'stock': 'Stock',
            'image': 'Imagen'
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

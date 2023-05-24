from django import forms
from .models import Contact, Product, Category, QueryType
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django.contrib.auth.forms import UserCreationForm
from .validators import MaxSizeFileValidator
from django.forms import ValidationError
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

class ContactForm(forms.ModelForm):
    name = forms.CharField(min_length=8, max_length=50, required=True, label='Nombre completo')
    email = forms.EmailField(required=True, label='Correo electrónico')
    phone = forms.IntegerField(label='Teléfono', min_value=100000000, max_value=999999999)
    message = forms.CharField(max_length=200, label='Mensaje')
    queryType = forms.ModelChoiceField(queryset=QueryType.objects.all(), required=True, label='Tipo de consulta')

    class Meta:
        model = Contact
        fields = ["name", "email", "phone", "message", "queryType"]
        labels = {
            'name': 'Nombre completo',
            'email': 'Correo electrónico',
            'phone': 'Teléfono',
            'message': 'Mensaje',
            'queryType': 'Tipo de consulta'
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            validate_email(email)
        except ValidationError:
            raise forms.ValidationError("El correo electrónico no es válido.")
        return email
    
    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if len(str(phone)) != 9:
            raise forms.ValidationError("El número de teléfono debe contener 9 dígitos.")
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
            self.add_error('name', 'El nombre debe tener al menos 8 caracteres.')
        if phone:
            try:
                cleaned_phone = self.clean_phone()
                cleaned_data['phone'] = cleaned_phone
            except forms.ValidationError as e:
                self.add_error('phone', e.message)

class ProductForm(forms.ModelForm):

    image = forms.ImageField(required=False,validators=[MaxSizeFileValidator(20)])
    name = forms.CharField(min_length=3,max_length=50)
    price = forms.IntegerField(min_value=1,max_value=1500000)

    def clean_name(self):
        name = self.cleaned_data["name"]
        instance = self.instance  # Obtener la instancia actual del producto

        # Verificar si existe otro producto con el mismo nombre
        exists = Product.objects.filter(name__iexact=name).exclude(pk=instance.pk).exists()

        if exists:
            raise ValidationError("Este producto ya existe")
        return name

    class Meta:
        model = Product
        # fields = ["name", "price", "description", "new", "category", "stock", "featured", "image"]
        fields = '__all__'
        labels = {
            'name': 'Nombre',
            'description': 'Descripcion',
            'price': 'Precio',
            'category': 'Categoria',
            'stock': 'Unidades',
            'new': '¿Nuevo?',
            'featured': '¿Destacado?',
            'rental_product' : '¿Arrendable?',
            'image': 'Imagen'
        }
class CustomUserCreationForm(UserCreationForm):
    pass         

class CategoryForm(forms.ModelForm):

    image = forms.ImageField(required=False,validators=[MaxSizeFileValidator(20)])
    name = forms.CharField(min_length=3,max_length=50)

    def clean_name(self):
        name = self.cleaned_data["name"]
        instance = self.instance  # Obtener la instancia actual de la categoría

        # Verificar si existe otra categoría con el mismo nombre
        exists = Category.objects.filter(name__iexact=name).exclude(pk=instance.pk).exists()

        if exists:
            raise ValidationError("Esta categoría ya existe")
        return name

    class Meta:
        model = Category
        # fields = ["name", "price", "description", "new", "category","cc", "stock", "featured", "image"]
        fields = '__all__'
        labels = {
            'name': 'Nombre',
            'description': 'Descripcion',
            'image': 'Imagen'
        }
from django import forms
from .models import Contact, Product
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django.contrib.auth.forms import UserCreationForm
from .validators import MaxSizeFileValidator
from django.forms import ValidationError

class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        fields = ["name", "email", "phone", "message", "queryType"]
        # fields = '__all__'
        labels = {
            'name': 'Nombre completo',
            'email': 'Correo electrónico',
            'phone': 'Teléfono',
            'message': 'Mensaje',
            'queryType': 'Tipo de consulta'
        }

class ProductForm(forms.ModelForm):

    image = forms.ImageField(required=False,validators=[MaxSizeFileValidator(20)])
    name = forms.CharField(min_length=3,max_length=50)
    price = forms.IntegerField(min_value=1,max_value=1500000)

    def clean_name(self):
        name =self.cleaned_data["name"]
        exist = Product.objects.filter(name__iexact=name).exist()

        if exist:
            raise ValidationError("Este producto ya existe")
        return name 

    class Meta:
        model = Product
        # fields = ["name", "price", "description", "new", "category","cc", "stock", "featured", "image"]
        fields = '__all__'
        labels = {
            'name': 'Nombre',
            'description': 'Descripcion',
            'price': 'Precio',
            'category': 'Categoria',
            'cc': 'Cantidad(cc)',
            'stock': 'Unidades',
            'new': '¿Nuevo?',
            'featured': 'Destacado?',
            'image': 'Imagen'
        }
class CustomUserCreationForm(UserCreationForm):
    pass         

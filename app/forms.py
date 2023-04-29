from django import forms
from .models import Contact, Product
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit

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
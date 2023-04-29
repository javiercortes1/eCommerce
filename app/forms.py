from django import forms
from .models import Contact
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit

class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        fields = ["name", "email", "phone", "message", "queryType"]
        # fields = '__all__'


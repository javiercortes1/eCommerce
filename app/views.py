from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'app/home.html')

def catalogue(request):
    return render(request, 'app/catalogue.html')

def services(request):
    return render(request, 'app/services.html')

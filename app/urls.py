from django.urls import path
from .views import home, services, catalogue, contact, add_product, list_product, update_product, delete_product, register

urlpatterns = [
    path('', home, name="home"),
    path('catalogue/', catalogue, name="catalogue"),
    path('services/', services, name="services"),
    path('contact/', contact, name="contact"),
    path('add-product/', add_product, name="add_product"),
    path('list-product/', list_product, name="list_product"),
    path('update-product/<id>/', update_product, name="update_product"),
    path('delete-product/<id>/', delete_product, name="delete_product"),
    path('register/',register,name="registro")

]
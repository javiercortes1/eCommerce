from django.urls import path, include
from .views import home, services, catalogue, contact,\
    add_product, list_product, update_product, delete_product,\
          ProductViewset, CategoryViewset, register, product_detail,\
          add_prod_cart, del_prod_cart, subtract_product_cart,\
          clean_cart, cart_page, buy_confirm, add_category,\
              list_category, update_category, delete_category

from rest_framework import routers

router = routers.DefaultRouter()
router.register('product', ProductViewset)
router.register('category', CategoryViewset)


urlpatterns = [
    path('', home, name="home"),
    path('catalogue/', catalogue, name="catalogue"),
    path('services/', services, name="services"),
    path('contact/', contact, name="contact"),
    path('add-product/', add_product, name="add_product"),
    path('list-product/', list_product, name="list_product"),
    path('update-product/<id>/', update_product, name="update_product"),
    path('delete-product/<id>/', delete_product, name="delete_product"),
    path('product-detail/<int:id>/', product_detail, name="product_detail"),
    path('add-category/', add_category, name="add_category"),
    path('list-category/', list_category, name="list_category"),
    path('update-category/<id>/', update_category, name="update_category"),
    path('delete-category/<id>/', delete_category, name="delete_category"),
    path('api/', include(router.urls)),
    path('register/',register,name="register"),
    path("add/<int:product_id>", add_prod_cart, name="Add"),
    path("delete/<int:product_id>", del_prod_cart, name="Del"),
    path("subtract/<int:product_id>", subtract_product_cart, name="Sub"),
    path("clean/", clean_cart, name="Clean"),
    path("cart/", cart_page, name="Cart"),
    # path("checkout/", checkout, name="Checkout"),
    path("buy-confirm/", buy_confirm, name="buy_confirm"),
    # path("success-payment/", pago_exitoso, name="pago_exitoso"),

]
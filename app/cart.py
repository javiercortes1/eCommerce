from .models import Product

class Cart:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        cart = self.session.get("cart")
        if not cart:
            self.session["cart"] = {}
            self.cart = self.session["cart"]
        else:
            self.cart = cart
    
    def add(self, product):
        id = str(product.id)
        if id not in self.cart.keys():
            self.cart[id]={
                "product_id": product.id,
                "product_name": product.name,
                "product_price": product.price,
                "accumulated": product.price,
                "amount": 1,
               
            }           
        else:
             if self.cart[id]["amount"] < product.stock:
                self.cart[id]["amount"] += 1
                self.cart[id]["accumulated"] += product.price
            
            # deberiamos tener un else con un mensaje de error

        self.save_cart()
    
    def save_cart(self):
        self.session["cart"] = self.cart
        self.session.modified = True

    def delete(self, product):
        id = str(product.id)
        if id in self.cart:
            del self.cart[id]
            self.save_cart()

    def subtract(self, product):
        id = str(product.id)
        if id in self.cart.keys():
            self.cart[id]["amount"] -= 1
            self.cart[id]["accumulated"] -= product.price
            if self.cart[id]["amount"] <= 0: self.delete(product)
            self.save_cart()

    def clean(self):
        self.session["cart"] = {}
        self.session.modified = True

    def buy(request):
        product = Product.objects.all()
        for keys, value in request.session["cart"].items():
            for y in product:
                    if "cart" in request.session.keys():
                        if int(value["product_id"]) == y.id:
                            print("Borrado")
                            y.stock = y.stock - int(value["amount"])
                            y.save()
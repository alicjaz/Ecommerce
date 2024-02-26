from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from store.models import Product

from .cart import Cart


def cart_summary(request):
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants()

    print("Cart Products:", cart_products)  # Add this line
    print("Quantities:", quantities)        # Add this line

    return render(request, "cart_summary.html", {"cart_products": cart_products, "quantities": quantities})


def cart_add(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        product = get_object_or_404(Product, id=product_id)

        print("Adding Product to Cart:", product.name, "Quantity:", product_qty)

        cart.add(product=product, quantity=product_qty)
        cart_quantity = cart.__len__()
        response = JsonResponse({'qty': cart_quantity})
        return response


def cart_delete(request):
    pass


def cart_update(request):
    pass

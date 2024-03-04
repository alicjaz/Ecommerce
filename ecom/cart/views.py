from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from store.models import Product

from .cart import Cart


def cart_summary(request):
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants()
    totals = cart.cart_total()
    print("Cart Products:", cart_products)
    print("Quantities:", quantities)

    return render(request, "cart_summary.html", {"cart_products": cart_products, "quantities": quantities,
                                                 "totals": totals})


def cart_add(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        product = get_object_or_404(Product, id=product_id)

        print("Adding Product to Cart:", product.name, "Quantity:", product_qty)

        cart.add(product=product, quantity=product_qty)
        cart_quantity = len(cart)
        response = JsonResponse({'qty': cart_quantity})
        return response


def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        cart.delete(product=product_id)
        response = JsonResponse({'product': product_id})

        return response


def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        cart.update(product=product_id, quantity=product_qty)

        response = JsonResponse({'qty': product_qty})

        return response

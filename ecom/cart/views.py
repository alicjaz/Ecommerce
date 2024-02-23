from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from store.models import Product

from .cart import Cart


def cart_summary(request):
    cart = Cart(request)
    cart_products = cart.get_prods
    return render(request, "cart_summary.html", {"cart_products": cart_products})


def cart_add(request):
    cart = Cart(request)

    product_id_str = request.POST.get('product_id')
    print(f"Received product ID: {product_id_str}")

    if product_id_str is not None:
        try:
            product_id = int(product_id_str)
            product = get_object_or_404(Product, id=product_id)
            cart.add(product=product)
            cart_quantity = cart.__len__()
            #response = JsonResponse({'Product Name': product.name})
            response = JsonResponse({'qty': cart_quantity})
            return response
        except (ValueError, Product.DoesNotExist) as e:
            print(f"Error: {e}")

    response = JsonResponse({'error': 'Invalid product ID'})
    response.status_code = 400  # Bad Request

    return response


def cart_delete(request):
    pass


def cart_update(request):
    pass

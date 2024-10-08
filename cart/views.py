from django.shortcuts import get_object_or_404, redirect, render
from .models import Product, Cart, CartItem
from django.contrib.auth.decorators import login_required

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    
    return redirect('cart_detail')

@login_required
def cart_detail(request):
    cart = get_object_or_404(Cart, user=request.user)
    items = CartItem.objects.filter(cart=cart)
    total_price = sum(item.total_price() for item in items)
    
    return render(request, 'cart_detail.html', {'items': items, 'total_price': total_price})

@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    cart_item.delete()
    return redirect('cart_detail')

@login_required
def update_cart_item(request, cart_item_id, quantity):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    cart_item.quantity = quantity
    cart_item.save()
    return redirect('cart_detail')

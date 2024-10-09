from django.shortcuts import get_object_or_404, redirect, render
from .models import Product, Cart, CartItem
from django.contrib.auth.decorators import login_required

# carrito/views.py
from django.shortcuts import render

def vista_carrito(request):
    return render(request, 'carrito.html')


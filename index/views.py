from django.shortcuts import render, redirect, HttpResponseRedirect
from django.views.generic.list import ListView
from django.contrib.auth import authenticate, login
from django.http import HttpResponse

from index.models import (
    Product, Category, Cart, CartProduct
)

def index(request): # fbv
    product_list = Product.objects.filter(is_active=True)[:3]

    category_list = Category.objects.all()[:3]

    if request.user.is_authenticated:
        cart = Cart.objects.get_or_create(user=request.user)[0]
    else:
        cart = None

    # cart = Cart.objects.get_or_create(user=request.user)[0] if request.user.is_authenticated else None

    context = {
        'product_list': product_list,
        'category_list': category_list,
        'cart':cart,
    }
    return render(request, "base.html", context)

# class ShopView(ListView): #cbv
#     model = Product 
#     template_name = 'shop.html'
#     context_object_name = 'product_list'    
#     queryset = Product.objects.select_related('category').all()

def shop(request):
    product_list = Product.objects.filter(is_active=True)

    # TODO: Rann pwodwi yo aktif/inaktif depann de stok la.

    category_list = Category.objects.all()

    brand_list = list(set(product_list.values_list('brand', flat=True)))

    if request.user.is_authenticated:
        cart = Cart.objects.get_or_create(user=request.user)[0]
    else:
        cart = None

    context = {
        'product_list': product_list,
        'category_list': category_list,
        'brand_list':brand_list,
        'cart': cart,
    }

    return render(request, 'shop.html', context)

def cart(request):
    if request.user.is_authenticated:
        # try:
        #     cart = Cart.objects.get(user=request.user)
        # except Cart.DoesNotExist:
        #     cart = Cart.objects.create(user=request.user)

        cart = Cart.objects.get_or_create(user=request.user)[0]
        cart_items = cart.cartproduct_set.all()    
    else:
        cart = None
        cart_items = []

    context = {
        'cart': cart,
        'cart_items':cart_items,
    }
    return render(request, 'cart.html', context)

def loginView(request):
    if request.user.is_authenticated: # Test si User a konekte
        return redirect('index')

    error_message = None
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        #1 Tcheke si user a otantifye
        user = authenticate(username=email, password=password)

        if user is not None:
            #2 Kreye sesyon
            login(request, user)

            # redireksyon nan non URL la.
            return redirect('index') # Referans (urls.py): path('', index, name='index'),
        else:
            error_message = "Idantifyan sa yo pa korèk, oubyen pa ekziste"
    
    context = {
        'error_message': error_message
    }
    return render(request, "login.html", context) 

def register(request):
    if request.user.is_authenticated: # Test si User a konekte
        return redirect('index')
    context = {}
    return render(request, "register.html", context)  

def addToCart(request, product_id):
    referer_url = request.META.get('HTTP_REFERER', '/')
        
    try:
        if request.user.is_authenticated:
            product = Product.objects.get(id=product_id)
            cart = Cart.objects.get_or_create(user=request.user)[0]

            # cp = CartProduct.objects.create(
            cp = CartProduct.objects.filter(
                cart = cart,
                product = product,
            ).first()

            if cp:
                cp.price = product.price
                cp.quantity += 1
                cp.save()
            else:
                CartProduct.objects.create(cart=cart, product=product,
                        price=product.price, quantity=1)

            

    except Product.DoesNotExist:
        pass 

    return redirect(referer_url)






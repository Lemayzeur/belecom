from django.shortcuts import render, redirect, HttpResponseRedirect
from django.views.generic.list import ListView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.http import HttpResponse

from index.models import (
    Product, Category, Cart, CartProduct
)

def getCart(request):
    if request.user.is_authenticated:
        print("AA")
        cart = Cart.objects.get_or_create(user=request.user)[0]
    elif 'cart_id' in request.session:
        print("BB")
        cart = Cart.objects.get(id=request.session['cart_id'])
        print(request.session['cart_id'])
    else:
        print("CC")
        request.session['cart_id'] = -1

        # Kreye yon panye ak enstans session_key ki kreye a
        cart,created = Cart.objects.get_or_create(
            session_id = request.session.session_key,
        )

        print(created)

        request.session['cart_id'] = cart.id

    return cart

def index(request): # fbv
    product_list = Product.objects.filter(is_active=True)[:3]

    category_list = Category.objects.all()[:3]

    cart = getCart(request)

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

    cart = getCart(request)

    context = {
        'product_list': product_list,
        'category_list': category_list,
        'brand_list':brand_list,
        'cart': cart,
    }

    return render(request, 'shop.html', context)

def cart(request):
    cart = getCart(request)
    cart_items = cart.cartproduct_set.all()

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

            # TODO: Database transaction

            # rekipere yon potansyel cart, ki nan sesyon an
            if 'cart_id' in request.session:
                # rekipere panye ki te nan sesyon an
                session_cart = Cart.objects.get(id=request.session['cart_id'])
                # Teste si itilizate ki ap konekte a, pat gen yon panye deja.
                if user.cart_set.exists():
                    # Si li te gen panye, ann rekipere l
                    cart = user.cart_set.first()
                    # Tout pwodwi ki te nan panye sa, nou ajoute yo nan panye sesyon an pito
                    all_items = cart.cartproduct_set.all()
                    all_items.update(cart=session_cart)
                    # Epi nou efase panye user a te genyen an
                    # cart.delete()
                # Panye sesyon an, vin pou itilizate ki konekte a kounya
                session_cart.user = user 
                # nou dekonekte panye a, ak sesyon an
                session_cart.session = None
                session_cart.save() 
            #2 Kreye sesyon
            login(request, user)

            # redireksyon nan non URL la.
            return redirect('index') # Referans (urls.py): path('', index, name='index'),
        else:
            error_message = "Idantifyan sa yo pa korèk, oubyen pa ekziste"
        
    cart = getCart(request)

    context = {
        'error_message': error_message,
        'cart':cart,
    }
    return render(request, "login.html", context) 

def logoutView(request):
    print(request.session.get('cart_id'))
    request.session.pop('cart_id', None)
    print(request.session.get('cart_id'))
    session = Session.objects.all().delete()
    logout(request) 
    return redirect('login')

def register(request):
    if request.user.is_authenticated: # Test si User a konekte
        return redirect('index')

    error_message = None
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            error_message = "Modpas yo pa menm"

        elif len(password) < 6:
            error_message = "Modpas sa twò kout"

        else:
            user = User.objects.create_user(
                username = email,
                password = password
            )

            login(request, user)

            return redirect('index')

    context = {
        'error_message': error_message,
    }
    return render(request, "register.html", context)  

def addToCart(request, product_id):
    referer_url = request.META.get('HTTP_REFERER', '/')
        
    try:
        product = Product.objects.get(id=product_id)
        if request.user.is_authenticated:
            cart = Cart.objects.get_or_create(user=request.user)[0]
        elif 'cart_id' in request.session:
            cart = Cart.objects.get(id=request.session['cart_id'])
        else:
            cart = None

        # Test si cart la ekziste
        if cart:
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

def removeFromCart(request, product_id):
    referer_url = request.META.get('HTTP_REFERER', '/')
        
    try:
        product = Product.objects.get(id=product_id)
        if request.user.is_authenticated:
            cart = Cart.objects.get_or_create(user=request.user)[0]
        elif 'cart_id' in request.session:
            cart = Cart.objects.get(id=request.session['cart_id'])
        else:
            cart = None

        # Test si cart la ekziste
        if cart:
            # cp = CartProduct.objects.create(
            cp = CartProduct.objects.filter(
                cart = cart,
                product = product,
            ).first()

            if cp:
                # si pwodwi a ekziste nan panye a, tout bon
                cp.delete()            

    except Product.DoesNotExist:
        pass 

    return redirect(referer_url)



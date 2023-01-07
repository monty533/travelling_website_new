from django.shortcuts import render,redirect
from django.views import View
from .models import Customer, Product, Cart, OrderPlaced
from .forms import CustomerRegistrationForm, CustomerProfile
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# def home(request):
#  return render(request, 'app/home.html')


class ProductView(View):
    def get(self, request):
        all_products = Product.objects.filter(category__in=['BW', 'TW', 'M'])
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/home.html', {'all_products': all_products, 'totalitem' : totalitem})


class ProductDetailView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        totalitem = 0
        item_already_in_cart = False
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
            print('product brand', product.brand)
        return render(request, 'app/productdetail.html', {'product': product,'item_already_in_cart':item_already_in_cart,'totalitem' : totalitem})

def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        amount = 00.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user==request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
        data = {
            'amount' : amount,
            'total_amount' : amount + shipping_amount,
            'quantity' : c.quantity
        }
        return JsonResponse(data)        

def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        amount = 00.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user==request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
        data = {
            'amount' : amount,
            'total_amount' : amount + shipping_amount,
            'quantity' : c.quantity
        }
        return JsonResponse(data)        

def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount = 00.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user==request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
        data = {
            'total_amount' : amount + shipping_amount,
            'quantity' : c.quantity
        }
        return JsonResponse(data)  

@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(pk=product_id)
    Cart(user=user,product=product).save()
    return redirect('/cart')

@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 00.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [cart_all_data for cart_all_data in Cart.objects.all() if cart_all_data.user==user]
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount += tempamount
                total_amount= amount + shipping_amount
            return render(request,'app/addtocart.html',{'cart':cart,'total_amount':total_amount,'amount':amount})
        else:
            return render(request,'app/emptycart.html')
    else:
        user = request.user
        print(user)
        print(user)
        return render(request,'app/emptycart.html')


def buy_now(request):
    return render(request, 'app/buynow.html')

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self,request):
        form = CustomerProfile()
        return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})
    
    def post(self,request):
        usr = request.user
        form = CustomerProfile(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=usr,name=name,locality=locality,city=city,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request,'Congratulations!! Profile updated successfully')
        return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})

@login_required
def address(request):
    user=request.user
    current_user = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html',{'current_users':current_user})

@login_required
def orders(request):
    op = OrderPlaced.objects.filter(user=request.user)
    print(op)
    return render(request, 'app/orders.html',{'op':op})


def mobile(request, data=None):
    if data == None:
        mobiles = Product.objects.filter(category='M')
    elif data == 'samsung' or data == 'oneplus':
        mobiles = Product.objects.filter(category='M').filter(brand=data)
    elif data == 'below':
        print(data)
        mobiles = Product.objects.filter(
            category='M').filter(discounted_price__lt=10000)
    elif data == 'above':
        mobiles = Product.objects.filter(
            category='M').filter(discounted_price__gt=10000)

    return render(request, 'app/mobile.html', {'mobiles': mobiles})


class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm
        return render(request, 'app/customerregistration.html', {'form': form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(
                request, 'Congratulations!! Resgistered Successfully')
            form.save()
        return render(request, 'app/customerregistration.html', {'form': form})

@login_required
def checkout(request):
    user = request.user
    address = Customer.objects.filter(user=user)
    cart_items = [p for p in Cart.objects.all() if p.user == user]
    amount = 00.0
    shipping_amount = 70.0
    total_amount = 0.0
    if cart_items:
        for p in cart_items:
            tempamount = (p.quantity * p.product.discounted_price)
            amount +=tempamount
        total_amount = amount + shipping_amount

    return render(request, 'app/checkout.html', {'address':address,'totalamount':total_amount,'cart_item':cart_items})

@login_required
@login_required
def paymentdone(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    print(type(customer))
    cart_items_base_on_user = Cart.objects.filter(user=user)
    # print(cart_items.values())
    for c in cart_items_base_on_user:
        OrderPlaced(user=user,customer=customer,product=c.product ,quantity=c.quantity).save()
        c.delete()
    return redirect('orders')
from django.shortcuts import render,redirect
from django.views import View
from .models import Customer, Product, Cart, OrderPlaced
from .forms import  CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class ProductView(View):
  def get(self,request):
    totalitem = 0
    topwears =Product.objects.filter(category="TW")
    bottomwears =Product.objects.filter(category="BW")
    mobiles =Product.objects.filter(category="M")
    laptop =Product.objects.filter(category="L")
    if request.user.is_authenticated:
      totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/home.html',
    {'topwears':topwears, 'bottomwears':bottomwears, 'mobiles':mobiles, 'laptop':laptop, 'totalitem':totalitem})

class ProductDetailView(View):
  def get(self,request,pk):
    totalitem = 0
    product = Product.objects.get(pk=pk)
    item_already_in_cart = False
    if request.user.is_authenticated:
      totalitem = len(Cart.objects.filter(user=request.user))
      item_already_in_cart =Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
    return render(request, 'app/productdetail.html',
     {'product':product,'item_already_in_cart':item_already_in_cart,'totalitem':totalitem})


@login_required
def add_to_cart(request):
  user=request.user
  product_id= request.GET.get('prod_id')
  product = Product.objects.get(id=product_id)
  cart = Cart.objects.filter(user=request.user)
  Cart(user=user, product=product).save()
  return redirect('/cart')
    
@login_required
def show_cart(request):
  totalitem = 0
  if request.user.is_authenticated:
    totalitem = len(Cart.objects.filter(user=request.user))
    cart = Cart.objects.filter(user=request.user)
    amount= 0.0
    shipping_amount = 70.0
    totalamount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    #print(cart)
    if cart_product:
      for p in cart_product:
        tempamount = (p.quantity * p.product.discounted_price)
        amount += tempamount
        totalamount =amount + shipping_amount
      return render(request,'app/addtocart.html',{'cart':cart,'amount':amount, 'totalamount':totalamount,'totalitem':totalitem})
    else:
      return render(request,'app/emptycart.html')

def plus_cart(request):
  if request.method == 'GET':
    prod_id = request.GET['prod_id']
    c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
    c.quantity+=1
    c.save()
    amount= 0.0
    shipping_amount =70.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user] 
    if cart_product:   
      for p in cart_product:
        tempamount = (p.quantity * p.product.discounted_price)
        amount += tempamount
      

      data = {
        'quantity':c.quantity,
        'amount':amount,
        'totalamount':amount + shipping_amount
      }
    return JsonResponse(data)

def minus_cart(request):
  if request.method == 'GET':
    prod_id = request.GET['prod_id']
    c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
    c.quantity-=1
    c.save()
    amount= 0.0
    shipping_amount =70.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user] 
    if cart_product:   
      for p in cart_product:
        tempamount = (p.quantity * p.product.discounted_price)
        amount += tempamount

      data = {
        'quantity':c.quantity,
        'amount':amount,
        'totalamount':amount + shipping_amount
      }
    return JsonResponse(data)

def remove_cart(request):
  if request.method == 'GET':
    prod_id = request.GET['prod_id']
    c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
    c.quantity+=1
    c.delete()
    amount= 0.0
    shipping_amount =70.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user] 
    if cart_product:   
      for p in cart_product:
        tempamount = (p.quantity * p.product.discounted_price)
        amount += tempamount

      data = {
        'quantity':c.quantity,
        'amount':amount,
        'totalamount':amount + shipping_amount
      }
    return JsonResponse(data)

@login_required  
def buy_now(request):
  return render(request, 'app/buynow.html')


@login_required
def checkout(request):
  totalitem = 0
  if request.user.is_authenticated:
    totalitem = len(Cart.objects.filter(user=request.user))
  user = request.user
  add = Customer.objects.filter(user=user)
  cart_items = Cart.objects.filter(user=user)
  amount= 0.0
  shipping_amount =70.0
  totalamount = 0.0
  cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    #print(cart)
  if cart_product:
    for p in cart_product:
      tempamount = (p.quantity * p.product.discounted_price)
      amount += tempamount
      totalamount =amount + shipping_amount
  return render(request,'app/checkout.html',{'add':add, 'totalamount':totalamount,'cart_items':cart_items,'totalitem':totalitem})

@login_required
def payment_done(request):
  totalitem = 0
  if request.user.is_authenticated:
    totalitem = len(Cart.objects.filter(user=request.user))
  user = request.user
  custiid = request.GET.get('custid')
  customer = Customer.objects.get(id=custiid)
  cart = Cart.objects.filter(user=user)
  for c in cart:
    OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
    c.delete()
  return redirect("orders")

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
      form = CustomerProfileForm()
      return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary'})


    def post(self, request):
      form = CustomerProfileForm(request.POST)
      if form.is_valid():
        usr = request.user
        name =form.cleaned_data['name'] 
        locality =form.cleaned_data['locality']       
        city =form.cleaned_data['city']
        state =form.cleaned_data['state']
        zipcode =form.cleaned_data['zipcode']
        reg = Customer(user=usr,name=name,locality=locality,city=city,state=state,zipcode=zipcode)
        reg.save()
        messages.success(request,'Congratulations!! Profile Updated successfully')
        return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary'})

      
@login_required
def address(request):
  totalitem = 0
  if request.user.is_authenticated:
    totalitem = len(Cart.objects.filter(user=request.user))
  ad =Customer.objects.filter(user=request.user)
  return render(request, 'app/address.html',{'add':ad,'active':'btn-primary'})

@login_required
def orders(request):
  totalitem = 0
  if request.user.is_authenticated:
    totalitem = len(Cart.objects.filter(user=request.user))
  op = OrderPlaced.objects.filter(user=request.user)
  return render(request, 'app/orders.html', {'order_placed':op,'totalitem':totalitem})


def change_password(request):
  return render(request, 'app/changepassword.html')


def mobile(request,data=None):
  totalitem = 0
  if request.user.is_authenticated:
    totalitem = len(Cart.objects.filter(user=request.user))
  if data== None:
    mobiles = Product.objects.filter(category='M')
  elif data == 'Oppo' or data == 'Samsung' or data == 'Vivo' or data =='Apple' or data == 'Nokia':
    mobiles = Product.objects.filter(category='M').filter(brand=data)
  elif data == 'below':
    mobiles = Product.objects.filter(category='M').filter(discounted_price__lt=20000)  
  elif data == 'above':
    mobiles = Product.objects.filter(category='M').filter(discounted_price__gt=20000)  
  return render(request, 'app/mobile.html',{'mobiles':mobiles,'totalitem':totalitem})
  

def laptop(request,data=None):
  totalitem = 0
  if request.user.is_authenticated:
    totalitem = len(Cart.objects.filter(user=request.user))
  if data== None:
    laptops = Product.objects.filter(category='L')
  elif data == 'HP' or data == 'DELL' or data == 'ASUS' or data =='Apple' or data == 'Nokia':
    laptops = Product.objects.filter(category='L').filter(brand=data)
  return render(request, 'app/laptop.html',{'laptops':laptops,'totalitem':totalitem})



def topwear(request,data=None):
  totalitem = 0
  if request.user.is_authenticated:
    totalitem = len(Cart.objects.filter(user=request.user))
  if data== None:
    topwears = Product.objects.filter(category='TW')
  elif data == 'DennisLingo' or data == 'IndoPrimo':
    topwears = Product.objects.filter(category='TW').filter(brand=data)
  return render(request, 'app/topwear.html',{'topwears':topwears,'totalitem':totalitem})  


def bottomwear(request,data=None):
  totalitem = 0
  if request.user.is_authenticated:
    totalitem = len(Cart.objects.filter(user=request.user))
  if data== None:
    bottomwears = Product.objects.filter(category='BW')
  elif data == 'InkastDenim' or data == 'WRANGLER':
    bottomwears = Product.objects.filter(category='BW').filter(brand=data)
  return render(request, 'app/bottomwear.html',{'bottomwears':bottomwears,'totalitem':totalitem}) 



def CustomerRegistration(request):
    if request.method == 'GET':
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', {'form': form})    
   
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST) 
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'You have singed up successfully.')
            login(request, user)
            return render(request, 'app/registration_done.html', {'form': form})        
        else:
            return render(request, 'app/customerregistration.html', {'form': form})
from django.shortcuts import render , redirect
from django.views import View
from .models import Product , Customer , Cart , OrderPlaced
from .forms import CutomerRegistrationForm ,MyProfileViewForm
from django.contrib import messages
from django.contrib.auth.models import User 
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator



class ProductView(View):
   def get(self, request):
    topwears=Product.objects.filter(category='TW')
    bottomwears=Product.objects.filter(category='BW')
    mobile=Product.objects.filter(category='M')
    return render(request , 'home.html',{'bottomwears':bottomwears , 'topwears':topwears , 'mobile':mobile})

        

class ProductDetailView(View):
 def get(self , request , pk):
    product=Product.objects.get(pk=pk)
    return render(request, 'productdetail.html' , {'product':product})

def mobile(request , data=None):
 if data==None:
  mobile=Product.objects.filter(category='M')
 elif data=='Redmi' or data=='Samsung':
  mobile=Product.objects.filter(category='M').filter(brand=data)
 elif data=='below':
  mobile=Product.objects.filter(category='M').filter(category='M').filter(descounted_price__lt=10000)
 elif data=='above':
  mobile=Product.objects.filter(category='M').filter(category='M').filter(descounted_price__gt=10000)
 return render( request , 'mobile.html',{'mobile':mobile}) 
  

class CutomerRegistrationView(View):
  def get(self , request):
      form=CutomerRegistrationForm()
      return render(request , 'customerregistration.html' , {'form':form})
  def post(self , request):
      form=CutomerRegistrationForm(request.POST)
      if form.is_valid():
         messages.info(request , 'Congratulation!! Registered Successfully')
         form.save()
         form=CutomerRegistrationForm() 
      return render(request , 'customerregistration.html',{'form':form})



@method_decorator(login_required , name='dispatch')
class ProfileViews(View):
  def get(slef , request):
    form=MyProfileViewForm()
    return render(request , 'profile.html' , {'form':form, 'active':'btn-primary'})
  def post(self, request):
    form = MyProfileViewForm(request.POST)
    if form.is_valid():
      usr=request.user
      name=form.cleaned_data['name']
      locality=form.cleaned_data['locality']
      city=form.cleaned_data['city']
      state=form.cleaned_data['state']
      zipcode=form.cleaned_data['zipcode']
      reg=Customer(user=usr,name=name , locality=locality , city=city , state=state , zipcode=zipcode)  
      reg.save()
      form=MyProfileViewForm()
      messages.info(request , 'Congratulation!! Profile Update Successfully!!')
    return render(request , 'profile.html' , {'form':form})

@login_required
def address(request):
 add=Customer.objects.filter(user=request.user)
 return render(request, 'address.html',{'add':add , 'active':'btn btn-primary'})
     



@login_required
def add_to_cart(request):
 user=request.user
 product_id=request.GET.get('prod_id')
 product=Product.objects.get(id=product_id)
 Cart(user=user , product=product).save()
 return redirect('/cart/')


@login_required
def show_cart(request):
  if request.user.is_authenticated:
    user=request.user
    cart=Cart.objects.filter(user=user)
    amount=0.0
    shipping_amount=70.0
    total_amount=0.0
    cart_product=[p for p in Cart.objects.all() if p.user==user]
    print(cart_product)
    if cart_product:
     for p in cart_product:
        tempamount=(p.quantity*p.product.descounted_price)
        amount += tempamount
        totalamount=amount+shipping_amount
     return render (request , 'addtocart.html',
     {'carts': cart , 'totalamount':totalamount,'amount':amount})
    else:
       return render(request, 'emptycart.html') 



def plus_cart(request):
   if request.method == 'GET':
     prod_id=request.GET['prod_id']
     c=Cart.objects.get(Q(product=prod_id)& Q(user=request.user))
     c.quantity+=1
     c.save()
     amount=0.0
     shipping_amount=70.0
     cart_product=[p for p in Cart.objects.all() if p.user==request.user]
     for p in cart_product:
        tempamount=(p.quantity*p.product.descounted_price)
        amount += tempamount
        

     data={
          'quantity':c.quantity,
          'amount':amount,
          'totalamount':amount+shipping_amount

        }
     return JsonResponse(data)





def minus_cart(request):
   if request.method == 'GET':
     prod_id=request.GET['prod_id']
     c=Cart.objects.get(Q(product=prod_id)& Q(user=request.user))
     c.quantity-=1
     c.save()
     amount=0.0
     shipping_amount=70.0
     cart_product=[p for p in Cart.objects.all() if p.user==request.user]
     for p in cart_product:
        tempamount=(p.quantity*p.product.descounted_price)
        amount += tempamount
       

     data={
          'quantity':c.quantity,
          'amount':amount,
          'totalamount':amount+shipping_amount

        }
     return JsonResponse(data)   


     
def remove_cart(request):
   if request.method == 'GET':
     prod_id=request.GET['prod_id']
     c=Cart.objects.get(Q(product=prod_id)& Q(user=request.user))
     c.delete()
     amount=0.0
     shipping_amount=70.0
     cart_product=[p for p in Cart.objects.all() if p.user==request.user]
     for p in cart_product:
        tempamount=(p.quantity*p.product.descounted_price)
        amount += tempamount

     data={
          'amount':amount,
          'totalamount':amount+shipping_amount

        }
     return JsonResponse(data)     
  

   




def buy_now(request):
 return render(request, 'buynow.html')

def orders(request):
 op=OrderPlaced.objects.filter(user=request.user)
 return render(request, 'orders.html',{'op':op})

@login_required
def checkout(request):
 user=request.user
 add=Customer.objects.filter(user=user)
 cart_items=Cart.objects.filter(user=user)
 amount=0.0
 shipping_amount=70.0
 totalamount=0.0
 cart_product=[p for p in Cart.objects.all() if p.user==request.user]
 if cart_product:
  for p in cart_product:
    tempamount=(p.quantity*p.product.descounted_price)
    amount += tempamount
  totalamount=amount+shipping_amount  
 return render(request, 'checkout.html', {'add':add , 'totalamount':totalamount,'cart_items':cart_items})

@login_required
def payment_done(request):
  user=request.user
  custid=request.GET.get('custid')
  customer=Customer.objects.get(id=custid)
  cart=Cart.objects.filter(user=user)
  for c in cart:
     OrderPlaced(user=user , customer=customer ,
     product=c.product , quantity=c.quantity ).save()
     c.delete()
  return redirect("orders")   
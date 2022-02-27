from django.contrib import admin
from .models import (

Customer,
Product ,
 Cart ,
  OrderPlaced
  )
# Register your models here.
@admin.register(Customer)
class AdminCustomer(admin.ModelAdmin):
    list_display=('id' , 'user' , 'name' , 'locality' , 'city'  , 'zipcode' , 'state')


@admin.register(Product)
class AdminProduct(admin.ModelAdmin):
    list_display=('image','id' , 'title' , 'selling_price' , 'descounted_price' , 'descripiton'  , 'brand' , 'category')

@admin.register(Cart)
class AdminCart(admin.ModelAdmin):
    list_display=('id' , 'user' , 'product' , 'quantity')    

@admin.register(OrderPlaced)
class AdminOrdered(admin.ModelAdmin):
    list_display=('id' , 'user' , 'customer' , 'product' , 'quantity'  , 'ordered_date' , 'status')
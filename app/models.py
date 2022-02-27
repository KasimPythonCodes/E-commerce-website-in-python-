from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinValueValidator
from django.utils.html import format_html
STATE_CHOICES=(
    ('Andaman & Nicobar Islands','Andaman & Nicobar Islands'),
    ('Andhra Pradesh','Andhra Pradesh'),
    ('Assam','Assam'),
    ('Bihar','Bihar'),
    ('Chandigarh','Chandigarh'),
    ('Chhattisgarh','Chhattisgarh'),
    ('Dadra','Dadra'),
    ('Utter Pradesh','Utter Pradesh'),
    ('Ghaziabad','Ghaziabad'),
    ('Dasna','Dasna'),
)



class Customer(models.Model):
    user=models.ForeignKey(User , on_delete=models.CASCADE)
    name=models.CharField(max_length=90)
    locality=models.CharField(max_length=90)
    city=models.CharField(max_length=90)
    zipcode=models.IntegerField()
    state=models.CharField(choices=STATE_CHOICES ,max_length=90)
    

    def __str__(self):
        return str(self.id)


CATEGORY_CHOICES=(
    ('M','Mobile'),
    ('L','Laptop'),
    ('TW','Top Wear'),
    ('BW','Bottom Wear'),

)

class Product(models.Model):
    title=models.CharField(max_length=90)
    selling_price=models.FloatField()
    descounted_price=models.FloatField()
    descripiton=models.TextField()
    brand=models.CharField(max_length=90)
    category=models.CharField(choices=CATEGORY_CHOICES , max_length=2)
    product_image=models.ImageField(upload_to='producting')

    def image(self):
      return format_html('<img  src="/media/{}" style="width:40px;height:40px;border-radius:50%;" / >'.format(self.product_image))


    def __str__(self):
        return str(self.id)


class Cart(models.Model):
    user=models.ForeignKey(User , on_delete=models.CASCADE)
    product=models.ForeignKey(Product , on_delete=models.CASCADE) 
    quantity=models.PositiveIntegerField(default=1)

    @property
    def total_cost(self):
      return self.quantity * self.product.descounted_price  
    




STATUS_CHOICES=(
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On The Way','On The Way'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel'),
)


class OrderPlaced(models.Model):
    user=models.ForeignKey(User , on_delete=models.CASCADE)
    customer=models.ForeignKey(Customer , on_delete=models.CASCADE)
    product=models.ForeignKey(Product , on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    ordered_date=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=90 , choices=STATUS_CHOICES , default='pending')


    def __str__(self):
        return str(self.id)


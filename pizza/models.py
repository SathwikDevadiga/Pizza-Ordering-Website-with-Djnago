
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Customer(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE , null=True , blank=True)
    name = models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=100, null=True)
    password = models.CharField(max_length=25, null=True)
    ph_no = models.CharField(max_length=11,null=True)

    def __str__(self):
        return self.name


    def EmailExists(self):
        if Customer.objects.filter(email = self.email):
            return True
        return False
    
    @staticmethod
    def getCustomerByEmail(email1):
        try:
            print(email1)
            return Customer.objects.get(email = email1)
           
        except:
            return False
            

    
class Product(models.Model) :
    name = models.CharField(max_length=100, null=True)
    price = models.FloatField(null=True,blank=True)
    desc = models.CharField(max_length=250,null=True)
    img = models.ImageField(null=True,blank=True,default='custom.webp') 
    custom = models.BooleanField(null=True,blank=True,default=False)  

    def __str__(self):
        return self.name
    
    @property
    def imageURL(self):
        try:
            url = self.img.url
        except:
            url = ''    
        return url    
    
class Order( models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL,blank=True,null=True  )
    Order_id = models.CharField(max_length=200,null=True)
    date_orderd = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)
    
    def get_cart_items(self):
        orderitems = self.oderitems_set.all()
        total = sum([item.quntity for item in orderitems ])
        return total
    
    def get_cart_total(self):
        orderitems = self.oderitems_set.all()
        total = sum([item.get_total for item in orderitems ])
        return total
    
    def razorpayAmt(self):
        orderitems = self.oderitems_set.all()
        total = sum([item.get_total for item in orderitems ])*100
        return int(total)
       

class OderItems(models.Model):
    product= models.ForeignKey(Product, on_delete=models.SET_NULL,blank=True,null=True  )
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
    quntity = models.IntegerField(default=0,null=True,blank=True)
    date_orderd = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quntity
        return total

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL,blank=True,null=True  ) 
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
    address = models.CharField(max_length=200,null=True)
    city = models.CharField(max_length=200,null=True)
    state = models.CharField(max_length=200,null=True)
    pincode = models.CharField(max_length=200,null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address



    

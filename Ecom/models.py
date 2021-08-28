from django.db import models
from django.contrib.auth.models import User

# Create your models here.
#class Customer(models.Model):
    #user=models.OneToOneField(User,on_delete=models.CASCADE)
    #profile_pic= models.ImageField(upload_to='profile_pic/',null=True,blank=True)
    #address = models.CharField(max_length=40)
    #mobile = models.CharField(max_length=20,null=False)
    #@property
    #def get_name(self):
     #   return self.user.first_name+" "+self.user.last_name
    #@property
    #def get_id(self):
     #   return self.user.id
    #def __str__(self):
     #   return self.user.first_name



class Product(models.Model):
    name=models.CharField(max_length=40)
    category=models.CharField(max_length=50,default="")
    price = models.PositiveIntegerField()
    description=models.CharField(max_length=100)
    product_image = models.ImageField(upload_to='product_image/', null=True, blank=True)
    def __str__(self):
        return self.name



class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=70, default="")
    phone = models.CharField(max_length=70, default="")
    desc = models.CharField(max_length=500, default="")


    def __str__(self):
        return self.name


class Orders(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Order Confirmed', 'Order Confirmed'),
        ('Out for Delivery', 'Out for Delivery'),
        ('Delivered', 'Delivered'),
    )


    amount=models.IntegerField(default=0)
    product = models.CharField(max_length=900,default="")
    name=models.CharField(max_length=90)
    email=models.CharField(max_length=111)
    address=models.CharField(max_length=111)
    city=models.CharField(max_length=111)
    state=models.CharField(max_length=111)
    zip_code=models.CharField(max_length=111)
    phone=models.CharField(max_length=111,default="")
    order_date = models.DateField(auto_now_add=True, null=True)
    status = models.CharField(max_length=50, null=True, choices=STATUS)
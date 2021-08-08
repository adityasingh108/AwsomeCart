from django.db import models

# Create your models here.


class product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=100, default="")
    product_price = models.IntegerField(default=0)
    product_catogory = models.CharField(max_length=100, default="")
    product_brand = models.CharField(max_length=100, default="")
    product_sub_catogory = models.CharField(max_length=100, default="")
    description = models.CharField(max_length=500, default="")
    publish_date = models.DateField(default="")
    product_image = models.ImageField(upload_to='shop/images', default="")

    def __str__(self):
        return self.product_name


# create the model of the contact
class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    phone = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    desc = models.CharField(max_length=1000)

    def __str__(self):
        return self.name


class orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    item_json = models.CharField(max_length=500000)
    amount = models.IntegerField(default=0)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    adress = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=100)

    # def __str__(self):
    #     return self.name
    
    
class orderUpdate(models.Model):
    update_id = models.AutoField(primary_key=True)
    order_id= models.IntegerField(default="")
    update_desc = models.CharField(max_length=5000)
    timestamp = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return  f"{self.order_id}   {self.update_desc[0:20]}"
    
    
class accaunt(models.Model):
    username = models.CharField(max_length=100)
    name = models.CharField(max_length=500000)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=50)
    
    def __str__(self):
        return self.username
    
    
        
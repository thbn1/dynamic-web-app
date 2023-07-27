from django.db import models
from django.contrib.auth.models import User
from django.db import models


class Product(models.Model):
    productname = models.CharField(max_length=250,null=False)
    productdesc=models.TextField()
    productcategory=models.CharField(max_length=50)
    productprice=models.FloatField()
    productoldprice=models.FloatField(default=0)
    productseller= models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(default="", null=False,unique=True)


class Image(models.Model):
    image = models.ImageField(upload_to='images',null=True)
    product=models.ForeignKey(Product, on_delete=models.CASCADE,null=True)

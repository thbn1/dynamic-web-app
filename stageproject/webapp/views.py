from django.shortcuts import render

from django.http.response import HttpResponse

from django.views.generic import TemplateView
from django.shortcuts import render,redirect
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout

from django.db.models import Q
import random
from webapp.models import Product,Image


def image_upload_view(request):
    """Process images uploaded by users"""
    if request.method == 'POST':
        
            name=request.POST["name"]
            description=request.POST["description"]
            category=request.POST["category"]
            price=request.POST["price"]
        
            print("ahahahaha")
            slug=name.replace(" ","-")
            filt=Product.objects.filter(slug=name.replace(" ","-"))
            print(filt)
            foo_instance = Product.objects.create(productname=name, productdesc=description,productprice=price, productcategory=category,slug=slug, productseller=request.user)

            foo_instance.save()
            # Get the current instance object to display in the template
            
            images = request.FILES.getlist('images')
            for image in images:
                Image.objects.create(image=image, product_id=foo_instance.id)
            images = Image.objects.all()
            return render(request, 'addproduct.html', {'images': images})
 
    return render(request, 'addproduct.html')
def index(request):

    return render(request,"index.html")


def register(request):
    rdata={} 
    if request.method =="POST":
        
        username= request.POST["username"]
        password= request.POST["password"]
        password2= request.POST["password2"]
        email= request.POST["email"]
        if len(username)<5:

            rdata["error"]="kullanıcı adınız 5 haneden kısa"
        if len(password)<8:
            rdata["error"]="Şifreniz 8 haneden kısa"
        elif User.objects.filter(username=username).exists():
            rdata["error"]="Kullanıcı adı kullanımda."
        else:
            user =User.objects.create_user(username=username,email=email,password=password)
            user.save()
            user = authenticate(request,username = username,password = password)
            if user is not None:
                login(request,user)
                return redirect("/index")
        print(rdata)
    return render(request,"register.html",rdata)


def Login(request):
    rdata={}
    if request.method =="POST":
        
        username= request.POST["username"]
        
        password= request.POST["password"]
        if len(username)==0:
            rdata["error"]="Kullanıcı adı boş bırakılamaz."
        if len(password)==0:
            rdata["error"]="Şifre boş bırakılamaz."
        else:
            user = authenticate(request,username = username,password = password)
            if user is not None:
                login(request,user)
                return redirect("/index")
            else:
                rdata["error"]="Kullanıcı adı veya şifre yanlış."
    return render(request,"login.html",rdata)

def addproduct(request):

    if request.user.is_authenticated:
        return render(request,"addproduct.html")
    else:
        return render(request,"index.html")
        
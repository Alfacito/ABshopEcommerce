from django.contrib.auth.models import Group,User
from django.contrib.auth import authenticate,login,logout
from . import forms
from django.shortcuts import render,redirect,reverse
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from . import models
from django.contrib import messages
from . models import Orders

import razorpay



def home(request):
    products = models.Product.objects.all()
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter = product_ids.split('|')
        product_count_in_cart = len(set(counter))
    else:
        product_count_in_cart = 0
    return render(request, 'Ecom/home.html',{'products':products,'product_count_in_cart':product_count_in_cart})

def  handleSignup(request):
    if request.method=='POST':

        # get all the parameters from signup page
        username=request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        #checks
        if len(username)>10:
            messages.error(request,"username must be under 10 characters")
            return redirect("home")

        if not username.isalnum():
            messages.error(request,"username should contain only letters and numbers ")
            return redirect("home")

        if pass1!=pass2:
            messages.error(request,"password donot match")
            return redirect("home")



        #create the user
        user=User.objects.create_user(username,email,pass1)
        user.first_name=fname
        user.last_name=lname
        user.save()
        messages.success(request,"your AB shop account is successfully created")
        return redirect('home')
    else:
        return HttpResponse("404 -page not found")

def handleLogin(request):
    if request.method=='POST':
        # get all the parameters from signup page
        loginusername=request.POST['loginusername']
        loginpass = request.POST['loginpass']
        user=authenticate(username=loginusername,password=loginpass)
        if user is not None:
            login(request,user)
            messages.success(request,"successfully logged in ")
            return redirect("home")
        else:
            messages.error(request,"invalid credentials, please try again")
            return redirect("home")
    return HttpResponse('404- page not found')

def handleLogout(request):
    logout(request)
    messages.success(request,"successfully logged out")
    return redirect("home")




def search_view(request):
    # whatever user write in search box we get in query
    query = request.GET['query']
    products=models.Product.objects.all().filter(name__icontains=query)
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=0

    # word variable will be shown in html when user click on search button
    word="Searched Result :"
    return render(request,'Ecom/home.html',{'products':products,'word':word,'product_count_in_cart':product_count_in_cart})


def add_to_cart_view(request,pk):
    products=models.Product.objects.all()

    #for cart counter, fetching products ids added by customer from cookies
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=1

    response = render(request, 'Ecom/home.html',{'products':products,'product_count_in_cart':product_count_in_cart})

    #adding product id to cookies
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        if product_ids=="":
            product_ids=str(pk)
        else:
            product_ids=product_ids+"|"+str(pk)
        response.set_cookie('product_ids', product_ids)
    else:
        response.set_cookie('product_ids', pk)

    product=models.Product.objects.get(id=pk)
    messages.info(request, product.name + ' added to cart successfully!')

    return response


def cart_view(request):
    #for cart counter
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=0

    # fetching product details from db whose id is present in cookie
    products=None
    total=0
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        if product_ids != "":
            product_id_in_cart=product_ids.split('|')
            products=models.Product.objects.all().filter(id__in = product_id_in_cart)

            #for total price shown in cart
            for p in products:
                total=total+p.price
    return render(request,'Ecom/cart.html',{'products':products,'total':total,'product_count_in_cart':product_count_in_cart})

def remove_from_cart_view(request,pk):
    #for counter in cart
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=0

    # removing product id from cookie
    total=0
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        product_id_in_cart=product_ids.split('|')
        product_id_in_cart=list(set(product_id_in_cart))
        product_id_in_cart.remove(str(pk))
        products=models.Product.objects.all().filter(id__in = product_id_in_cart)
        #for total price shown in cart after removing product
        for p in products:
            total=total+p.price

        #  for update coookie value after removing product id in cart
        value=""
        for i in range(len(product_id_in_cart)):
            if i==0:
                value=value+product_id_in_cart[0]
            else:
                value=value+"|"+product_id_in_cart[i]
        response = render(request, 'Ecom/cart.html',{'products':products,'total':total,'product_count_in_cart':product_count_in_cart})
        if value=="":
            response.delete_cookie('product_ids')
        response.set_cookie('product_ids',value)
        return response

def about(request):
    return render(request,'Ecom/about.html')


def contact(request):
    thank = False
    if request.method=="POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        contact = models.Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
        thank = True
    return render(request, 'Ecom/contact.html', {'thank': thank})


def productview(request, myid):

    # Fetch the product using the id
    product = models.Product.objects.filter(id=myid)

    return render(request, 'Ecom/prodview.html', {'product':product[0]})


RAZORPAY_API_KEY='rzp_test_lMbW52HiYUESqz'
RAZORPAY_API_SECRET_KEY='5XIWCBFKwYKqHUYNreICYYAI'
client = razorpay.Client(auth=(RAZORPAY_API_KEY , RAZORPAY_API_SECRET_KEY))
def customer_address_view(request):
    total = 0
    product_ids = request.COOKIES['product_ids']
    product_id_in_cart = product_ids.split('|')
    products = models.Product.objects.all().filter(id__in=product_id_in_cart)
        # for total price shown in cart
    for p in products:
        total = total + p.price

    if request.method=="POST":
        pro=[]
        product_ids = request.COOKIES['product_ids']
        product_id_in_cart = product_ids.split('|')
        products = models.Product.objects.all().filter(id__in=product_id_in_cart)
        pro.append(products)
        product=pro
        name = request.POST.get('name', '')
        amount = total
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        order = Orders( name=name, email=email, address=address, city=city,
                       state=state, zip_code=zip_code, phone=phone, amount=amount,product=product)
        order.save()


        #-------------------------------for rozarpay payment-----------
        total = 0
        product_ids = request.COOKIES['product_ids']
        product_id_in_cart = product_ids.split('|')
        products = models.Product.objects.all().filter(id__in=product_id_in_cart)
        # for total price shown in cart
        for p in products:
            total = total + p.price

        order_amount = total * 100
        order_currency = 'INR'
        payment_order = client.order.create(dict(amount=order_amount, currency=order_currency, payment_capture=1))
        payment_order_id = payment_order['id']
        context = {'amount': total, 'api_key': RAZORPAY_API_KEY, 'order_id': payment_order_id}


        return render(request, 'Ecom/payment.html', context)

       #-------------------------------------------------------------------------------------
    return render(request, 'Ecom/customer_address.html', {'total':total})







def my_order_view(request):
    user=request.user.id
    orders=models.Orders.objects.all().filter(id = user)
    ordered_products=[]
    for order in orders:
        ordered_product=models.Product.objects.all().filter(id=order.id)
        ordered_products.append(ordered_product)

    return render(request,'Ecom/my_order.html',{'data':zip(ordered_products,orders)})

def my_profile_view(request):

    user= request.user
    return render(request,'Ecom/my_profile.html',{'user':user})

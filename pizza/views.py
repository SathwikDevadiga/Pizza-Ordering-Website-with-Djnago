from django.shortcuts import render , redirect 
from .models import *
from django.contrib import messages
from django.http import JsonResponse
import json
from django.core.mail import send_mail
import datetime
import razorpay
from django.contrib.auth.models import User
from django.contrib.auth import authenticate ,logout 
from django.contrib.auth import login as auth_login
from django.http import HttpResponse , HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required


# Create your views here.
def login(request):
    context = {}
    if request.method == "GET":
        return render(request, 'login.html', context)
    else :
        email = request.POST['email']
        password = request.POST['pass']
        
        error_message = None
        
        
        user = authenticate(request,username=email,password=password)

        if user:

            if user.is_active:
                auth_login(request,user)
                return redirect('home')
            else:
                error_message ='User is not Active'
        else:
            error_message ='User Not Available'            
    return render(request, 'login.html', {'error':error_message})


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action: ' , action )
    print('productId: ',productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order , created = Order.objects.get_or_create(customer=customer ,complete=False )

    orderItem , created = OderItems.objects.get_or_create(order = order , product = product ) 
    if action == 'add':
        orderItem.quntity = (orderItem.quntity + 1)
    elif action == 'remove':
        orderItem.quntity = (orderItem.quntity - 1) 
         

    orderItem.save()
    if orderItem.quntity <=0:
        orderItem.delete() 

    
    messages.success(request,"Item was Added to Cart")
    return  JsonResponse('Item was added', safe=False)  

def addcustom(request):
    total = request.GET.get('total')
    customer = request.user.customer
    product = Product.objects.create(name = "custom" , price = total ,custom=True ) 
    order , created = Order.objects.get_or_create(customer=customer ,complete=False )
    OderItems.objects.get_or_create(order = order , product = product ,quntity = 1,)  
    return redirect(cart)
    
    
def contact(request):
    context = {}
    if request.method == "POST" :
        name = request.POST["name"]
        email = request.POST["email"]
        subject = request.POST["Subject"]
        comment = request.POST["comment"]
        email_message = f"From: {name}\nEmail: {email}\n\n{comment}"
        send_mail(subject, email_message, email, ['devadiga.sathwik81544@gmail.com'])
        print("success")
        return redirect(contact)
    return render(request, 'contact.html', context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order , created = Order.objects.get_or_create(customer=customer ,complete = False)
        items = order.oderitems_set.all()
    else:
        items = []	
    context = {'items':items , 'order': order}
    return render(request, 'cart.html', context)

def registration(request):
    
    if request.method == 'POST':
        name = request.POST["name"]
        email = request.POST["email"]
        password = request.POST["password"]
        ph_no = request.POST["ph_no"]
        customer = Customer(name = name , email = email , password = password , ph_no = ph_no)
        EmailExits =  customer.EmailExists() 
        if EmailExits:
            messages.error(request , "Email already Exist")
            return render(request, 'registration.html')
        
        user = User.objects.create_user(username=name, password=password, email=email, ) 
        customer = Customer(user = user ,name = name , email = email , password = password , ph_no = ph_no)                              
        customer.save()   
        
        return redirect(login)
    return render(request, 'registration.html')
    
def orderDetails(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    customer = request.user.customer
    orders = Order.objects.filter(customer=customer,complete = True).order_by('-date_orderd')
    ordered = []
    for order in orders:
        tt = []
        items = OderItems.objects.filter(order=order)
        for item in items:
            tt.append(item)
        ordered.append({'order':order , 'items':tt})

   
    print(ordered)
   
    context = {
        'orders' : orders,
        'items' : tt,
        'ordered': ordered,
    }     
    return render(request, 'orderDetails.html',context) 



def checkout(request):
    
    customer = request.user.customer
    order , created = Order.objects.get_or_create(customer=customer ,complete = False)
    items = order.oderitems_set.all()
    
    amt = order.razorpayAmt()
    print("amt")
    print(amt)
        
    
    client = razorpay.Client(auth=("rzp_test_OLtkEv9d4tEzRr", "jCfN2LohZgZuhE8qLWunMM8c"))

    data = { "amount": amt, "currency": "INR", "receipt": "order_rcptid_11" }
    payment = client.order.create(data=data)
    context = {'items':items , 'order': order , 'payment':payment}
    return render(request, 'checkout.html', context)

def home(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    products= Product.objects.filter(custom = False)
    customer = request.user.customer
    order , created = Order.objects.get_or_create(customer=customer ,complete = False)
    items = order.oderitems_set.all()
    context = {'products':products,'items':items ,'order': order}
    return render(request, 'home.html', context)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    customer = request.user.customer
    order , created = Order.objects.get_or_create(customer=customer,complete=False )
    total = float(data['form']['total'])
    order.Order_id = transaction_id
    
    order.complete = True
    print("oder completes")

    order.save()

    ShippingAddress.objects.create(
        customer = customer,
        order = order,
        address = data['shipping']['address'],
        city = data['shipping']['city'],
        state = data['shipping']['state'],
        pincode = data['shipping']['zipcode'],


    )
    
    return JsonResponse('Payment submitted..',safe=False)


@login_required()
def user_logout(request):
    logout(request)
    return render(request, 'home')

def customize(request):
    context = {}
    return render(request, 'customize.html', context)




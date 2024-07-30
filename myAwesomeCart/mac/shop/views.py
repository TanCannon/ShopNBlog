from django.shortcuts import render
#maine import kiya hai
from django.shortcuts import HttpResponse, redirect
from .models import Products, Contact, Orders, OrderUpdate
from math import ceil
import json
from django.contrib import messages 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


# Create your views here.
def index(requests):
    # products = Product.objects.all()
    # print(products)
    # n = len(products)
    # nSlides = n//4 + ceil((n/4)-(n//4))
    print(requests.user.id)

    allProds = []
    catprods = Products.objects.values('category', 'id')
    # print(f'catprods:{catprods}')
    cats = {item['category'] for item in catprods} #stores various categories
    # print(cats)
    for cat in cats:
        prod = Products.objects.filter(category=cat) #category wise filter product
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4)) #calculating no. of slides needed
        allProds.append([prod, range(1, nSlides), nSlides])

    # params = {'no_of_slides':nSlides, 'range': range(1,nSlides),'product': products}
    # allProds = [[products, range(1, nSlides), nSlides],
    #             [products, range(1, nSlides), nSlides]]
    params = {'allProds':allProds}
    # print(f'allProds--{allProds}')
    messages.success(requests,"Hello there welcome to My Awesome Cart")
    return render(requests, 'shop/index.html', params)

#to check the words present in query and items fetched from the database one by one
def searchMatch(query, item):
    if (query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower()):
        return True
    
def search(requests):
    query =  requests.GET.get('search')
    # print(f"query- {query}")

    allProds = []
    catprods = Products.objects.values('category', 'id')
    # print(f'catprods:{catprods}')
    cats = {item['category'] for item in catprods} #stores various categories
    # print(cats)
    for cat in cats:
        prodtemp = Products.objects.filter(category=cat) #category wise filter product, returns a list of objects
        prod = [item for item in prodtemp if (searchMatch(query, item))] #checking if the item exists in the query or words made or put by the user in the search.
        n = len(prod)
        if (n != 0):
            print(f"n-{n}")
            nSlides = n // 4 + ceil((n / 4) - (n // 4))
            allProds.append([prod, range(1, nSlides), nSlides])

    params = {'allProds':allProds}

    return render(requests,"shop/search.html",params)

def about(requests):
    # return HttpResponse('shop/about.html')
    return render(requests,'shop/about.html')

def contact(requests):
    # return HttpResponse('contact page')
    thank = False
    if (requests.method=="POST"):
        print(requests) 
        name=requests.POST.get("name")
        email=requests.POST.get("email")
        phone=requests.POST.get("phone")
        desc=requests.POST.get("desc")
        print(name,email,phone,desc)
        fetched_contact = Contact(name=name, email=email, phone=phone, desc=desc)
        fetched_contact.save()
        thank = True
    return render(requests,'shop/contact.html',{'thank': thank})

def tracker(requests):
    if requests.method=="POST":
        orderId = requests.POST.get('orderId', '')
        email = requests.POST.get('email', '')
        # print(orderId,email)
        try:
            order = Orders.objects.filter(order_id=orderId, email=email) #returns a list
            print(f"{order}-order")

            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps({"status": "success","updates":updates,"order": order[0].items_json}, default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status": "empty"}')
        except Exception as e:
            return HttpResponse('{"status":error}')

    return render(requests, 'shop/tracker.html')

def productView(requests,myid):
    product = Products.objects.filter(id=myid) 
    # print(product)
    params = {'product':product[0]}
    return render(requests,'shop/prodView.html',params) #product is a list of one element
    # return HttpResponse('productview page')

def checkout(requests):

    # return HttpResponse('checkout page') 
    if (requests.method=="POST"):
        # print(requests)
        items_json=requests.POST.get("itemsJson",'')
        name=requests.POST.get("name",'')
        email=requests.POST.get("email",'')
        address=requests.POST.get("address1",'') + " " + requests.POST.get("address2",'')
        city=requests.POST.get("city",'')
        state=requests.POST.get("state",'')
        zip_code=requests.POST.get("zip_code",'')
        phone=requests.POST.get("phone")
       
        # print(items_json,name,email,address,city,state,zip_code,phone)
        order = Orders(items_json=items_json,name=name,email=email,address=address,city=city,state=state,zip_code=zip_code,phone=phone)
        order.save()

        #"thank is used to check if order was placed, it's made true to notify the js on the checkout.html page to show order placed notification"
        thank = True
        id = order.order_id

        #This to save order tracking update in the database 
        update = OrderUpdate(order_id = id, update_desc = "The order has been placed")
        update.save()

        #to show popup messages by bootstrap
        # messages.success(requests,f"Thanks for ordering with us. Your order ID is {id}. Use it to track your order using our order tracker")
        # index(requests)
        return render(requests, 'shop/checkout.html',{'thank':thank, 'id':id})
    return render(requests, 'shop/checkout.html')

def handelSignup(requests):
    if requests.method=="POST":
        # Get the post parameters
        username=requests.POST.get('username')
        email=requests.POST.get('email')
        fname=requests.POST.get('fname')
        lname=requests.POST.get('lname')
        pass1=requests.POST.get('pass1')
        pass2=requests.POST.get('pass2')

        # check for errorneous input
        # if len(username)<10:
        #     messages.warning(requests, " Your user name must be under 10 characters")
        #     return redirect('/blog')

        if not username.isalnum():
            messages.warning(requests, " User name should only contain letters and numbers")
            return redirect('/shop')
        if (pass1!= pass2):
            messages.warning(requests, " Passwords do not match")
            return redirect('/shop')
        # Create the user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name= fname 
        myuser.last_name= lname
        myuser.save()
        messages.success(requests, " Your Account has been successfully created")
        return redirect('/shop')

    else:
        return HttpResponse("404 - Not found")
    
def handelLogin(request):
    if request.method=="POST":
        # Get the post parameters
        loginusername=request.POST.get('loginusername')
        loginpassword=request.POST.get('loginpassword')

        user=authenticate(username= loginusername, password= loginpassword)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect("/shop")
        else:
            messages.error(request, "Invalid credentials! Please try again")
            return redirect("/shop")

    return HttpResponse("404- Not found")

def handelLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('/shop')
'''making the logout button is yet to be finshed'''

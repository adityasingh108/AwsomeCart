from django import http
from django.core.checks import messages
from django.contrib import messages
from django.db.models import query
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, response
from .models import Contact, product, orders, orderUpdate, accaunt
from django.contrib.auth.decorators import login_required
from math import ceil, trunc
import json
from django.views.decorators.csrf import csrf_exempt
from paytm import Checksum

MERCHANT_KEY = 'zlhSB%nIlSgaXUUG'

# Create your views here.

# Create your views here.


def index(request):
    all_products = []
    category_prod = product.objects.values('product_catogory')
    categories = {item['product_catogory']for item in category_prod}
    for cat in categories:
        products = product.objects.filter(product_catogory=cat)
        n = len(products)
        n_slides = n//4 + ceil((n/4) - (n//4))
        all_products.append([products, range(1, n_slides), n_slides])
    param = {'all_products': all_products}
    return render(request, "shop/index.html", param)


def SerchMatch(query, item):
    if query in item.product_name.lower() or query in item.product_catogory.lower() or query in item.description.lower() or query in item.product_sub_catogory.lower() or query in item.product_brand.lower():
        return True
    else:
        return False


def serch(request):
    query = request.GET.get('serch')
    all_products = []
    category_prod = product.objects.values('product_catogory')
    categories = {item['product_catogory']for item in category_prod}
    for cat in categories:
        products = product.objects.filter(product_catogory=cat)
        prod = [item for item in products if SerchMatch(query, item)]
        n = len(prod)
        n_slides = n//4 + ceil((n/4) - (n//4))
        if len(prod) != 0:
            all_products.append([products, range(1, n_slides), n_slides])
    param = {'all_products': all_products, 'msg': ''}
    if len(all_products) == 0 or len(query) < 2:
        param = {'msg': 'Please make sure to enter relevant Query.'}
    return render(request, "shop/serch.html", param)

# This is about page


# def login(request):
#     return render(request, 'shop/index.html')


def signup(request):
    # if request.method == "POST":
    #     username = request.POST.get('username',"")
    #     name = request.POST.get('fname',"") + " " + request.POST.get('lname',"")
    #     email =  request.POST.get('email',"")
    #     password =  request.POST.get('pass1',"") + " " +  request.POST.get('pass2',"")
    #     signup = accaunt(username=username,name=name,password=password,email=email)
    #     signup.save()
    # else:
    #     return HttpResponse("Page not found ")
    # return render(request,'shop/signup.html')

    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['signupemail']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

    #    checking the usr Creandentials
        if len(username) > 10:
            messages.error(
                request, " Your user name must be under 10 characters")
            return redirect('Homepage')

        if not username.isalnum():
            messages.error(
                request, " User name should only contain letters and numbers")
            return redirect('Homepage')
        if (pass1 != pass2):
            messages.error(request, " Passwords do not match")
            return redirect('Homepage')

      # creating the user

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(
            request, " Your Awsome Cart accaunt has been successfully created")
        return redirect('Homepage')
    else:
        return render(request, 'shop/404.html')


def handlelogin(request):
    if request.method == "POST":
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']

        user = authenticate(username=loginusername, password=loginpassword)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect('Homepage')
        else:
            messages.error(request, "Invalid credentials Please try again")
            return redirect('Homepage')

    else:
        return render(request, 'shop/404.html')


def handlelogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('Homepage')


def about(request):
    return render(request, "shop/about.html")


# this is our cntact
def contact(request):
    if request.method == "POST":
        name = request.POST.get('name', '')
        phone = request.POST.get('phone', '')
        email = request.POST.get('email', '')
        desc = request.POST.get('desc', '')
        contact = Contact(name=name, phone=phone, email=email, desc=desc)
        contact.save()
        thank = True
        return render(request, "shop/contact.html", {"thank": thank})
    return render(request, "shop/contact.html")


# tracker page
def tracker(request):
    if request.method == "POST":
        order_id = request.POST.get('order_id', '')
        trackeremail = request.POST.get('trackeremail', '')
        # print(f" order id {order_id}  email is {email}")
        # return HttpResponse(f" order id {order_id}  email is {email}")
        try:
            order = orders.objects.filter(order_id=order_id, email=trackeremail)
            if len(order) > 0:
                update = orderUpdate.objects.filter(order_id=order_id)
                updates = []
                for item in update:
                    updates.append(
                        {'text': item.update_desc, 'time': item.timestamp})
                response = json.dumps(
                    [updates, order[0].item_json], default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('make sure your id and emai is correct')
        except Exception as e:
            return HttpResponse("order id and email is can't blank.")

    return render(request, 'shop/tracker.html')

# serch page


# product view page
def product_views(request, myid):
    products = product.objects.filter(id=myid)
    return render(request, 'shop/product_view.html', {'product': products[0]})


# chekout page
# @login_required(login_url='login')
def checkout(request):
    if request.method == "POST":

        item_json = request.POST.get('item_json', '')
        amount = request.POST.get('amount', '')
        name = request.POST.get('firist_name', '') + \
            " " + request.POST.get('last_name', '')
        phone = request.POST.get('phone', '')
        email = request.POST.get('email', '')
        adress = request.POST.get('adress', '') + \
            " " + request.POST.get('adress2', '')
        country = request.POST.get('country', '')
        state = request.POST.get('state', '')
        city = request.POST.get('city', '')
        zip_code = request.POST.get('zip_code', '')
        order = orders(item_json=item_json, name=name, phone=phone, email=email,
                       adress=adress, country=country, state=state, city=city, zip_code=zip_code, amount=amount)
        order.save()
        update = orderUpdate(order_id=order.order_id,
                             update_desc="The order has been placed.")
        update.save()
        thank = True
        id = order.order_id
        # return render(request, 'shop/checkout.html', {'thank': thank, 'id': id})
        param_dict = {

            'MID': 'fALCTU78586304196437',
            'ORDER_ID': str(order.order_id),
            'TXN_AMOUNT': str(amount),
            'CUST_ID': email,
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL': 'http://127.0.0.1:8000/shop/handlerequest/',

        }
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(
            param_dict, MERCHANT_KEY)
        return render(request, 'shop/paytm.html', {'param_dict': param_dict})

    return render(request, 'shop/checkout.html')


@csrf_exempt
def handlerequest(request):
    # paytm will send you post request here
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
        else:
            print('order was not successful because' +
                  response_dict['RESPMSG'])
    return render(request, 'shop/paymentstatus.html', {'response': response_dict})

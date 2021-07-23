from django.shortcuts import render
from django.http import HttpResponse, response
from .models import Contact, product, orders, orderUpdate
from math import ceil, trunc
import json
from django.views.decorators.csrf import csrf_exempt
from paytm import Checksum

MERCHANT_KEY = 'kbzk1DSbJiV_03p5';

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


# This is about page
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
        email = request.POST.get('email', '')
        # print(f" order id {order_id}  email is {email}")
        # return HttpResponse(f" order id {order_id}  email is {email}")
        try:
            order = orders.objects.filter(order_id=order_id, email=email)
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


def serch(request):
    return render(request, 'shop/serch.html')


# product view page
def product_views(request, myid):
    products = product.objects.filter(id=myid)
    return render(request, 'shop/product_view.html', {'product': products[0]})


# chekout page
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
        return render(request, 'shop/checkout.html', {'thank': thank, 'id': id})
        param_dict = {

            'MID': 'WorldP64425807474247',
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

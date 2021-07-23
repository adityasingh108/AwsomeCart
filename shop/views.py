from django.shortcuts import render
from django.http import HttpResponse, response
from .models import Contact, product, orders, orderUpdate
from math import ceil, trunc
import json


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
                       adress=adress, country=country, state=state, city=city, zip_code=zip_code ,amount=amount)
        order.save()
        update = orderUpdate(order_id=order.order_id,
                             update_desc="The order has been placed.")
        update.save()
        thank = True
        id = order.order_id
        return render(request, 'shop/checkout.html', {'thank': thank, 'id': id})
    return render(request, 'shop/checkout.html')

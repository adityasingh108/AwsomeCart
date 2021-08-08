from shop.views import signup
from django.contrib import admin

from .models import Contact, orderUpdate, orders, product,accaunt

# Register your models here.

admin.site.register(product)
admin.site.register(Contact)
admin.site.register(orders)
admin.site.register(orderUpdate)
admin.site.register(accaunt)

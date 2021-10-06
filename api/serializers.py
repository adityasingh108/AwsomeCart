from django.db.models import fields
from rest_framework import serializers
from shop.models import product


class AwsomecartProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = product
        fields = ['id','product_name','product_price','product_catogory',
                  'product_brand','product_sub_catogory','description','publish_date','product_image']
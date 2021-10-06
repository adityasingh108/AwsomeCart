from shop.models import product
from .serializers import AwsomecartProductSerializers
from rest_framework.generics import ListCreateAPIView ,RetrieveUpdateDestroyAPIView

# Create your views here.

class AwesomecartApiProduct(ListCreateAPIView):
    queryset = product.objects.all()
    serializer_class= AwsomecartProductSerializers
    
class AwesomecartApiProductSingle(RetrieveUpdateDestroyAPIView):
    queryset = product.objects.all()
    serializer_class= AwsomecartProductSerializers
       



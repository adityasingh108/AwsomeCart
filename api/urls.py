from django.urls import path
from . import views


urlpatterns = [
    path('product/',views.AwesomecartApiProduct.as_view()),
    path('product/<int:pk>',views.AwesomecartApiProductSingle.as_view()),
]

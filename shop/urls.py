from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="Homepage"),
    path("about/", views.about, name="AboutUs"),
    path("contact/", views.contact, name="ContactUs"),
    path("tracker/", views.tracker, name="TrackingStatus"),
    path("serch/", views.serch, name="Serch"),
    path("products/<int:myid>", views.product_views, name="ProductView"),
    path("checkout/", views.checkout, name="Checkout"),
    path("handlerequest/", views.handlerequest, name="HandleRequest"),
    path('login/',views.handlelogin,name="login"),
    path('logout/',views.handlelogout,name="logout"),
    path('signup/',views.signup,name="SignUP"),
]

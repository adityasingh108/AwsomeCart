from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index , name="Blog"),
    path("blogpost/", views.blogpost , name="blogpost"),
]

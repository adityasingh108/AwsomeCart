from django.shortcuts import render
from django.http import HttpResponse
from .models import blogPost

def index(request):
    post = blogPost.objects.all()
    return render(request, 'blog/index.html' ,{'post':post})

def blogpost(request ,id):
    post = blogPost.objects.filter(post_id=id)[0]
    return render(request, 'blog/blogpost.html' ,{'post':post})


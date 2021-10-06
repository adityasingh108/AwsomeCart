from django.db.models import query
from django.shortcuts import render
from django.http import HttpResponse
from .models import blogPost

def index(request):
    post = blogPost.objects.all()
    return render(request, 'blog/index.html' ,{'post':post})

def blogpost(request ,id):
    post = blogPost.objects.filter(post_id=id)[0]
    return render(request, 'blog/blogpost.html' ,{'post':post})

def serchMatch(query):
    pass
def serch(request):
    query= request.GET['query']
    print(query)
    post = blogPost.objects.all()
    return render(request, 'blog/serch.html' ,{'post':post})
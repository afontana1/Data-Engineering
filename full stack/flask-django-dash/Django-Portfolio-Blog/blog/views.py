from blog.forms import CommentForm, CustomUserCreationForm, PostForm
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.urls import reverse
from blog.models import Category, Post, Comment

# Create your views here.
def blog_index(request):
  form = PostForm()
  if request.method == 'POST':
    form = PostForm(request.POST)
    if form.is_valid():
      categories_input = form.cleaned_data["categories"].split(";")
      post = Post.objects.create(
        body = form.cleaned_data['body'],
        title = form.cleaned_data['title'],
        author = str(request.user),
      )
      for category in categories_input:
        cat, _ = Category.objects.get_or_create(name=category)
        post.categories.add(cat)
      post.save()
  posts = Post.objects.all().order_by('-created_on')
  context = {
    "posts": posts,
    "title": "All Blogs",
    "form": form
  }
  return render(request,"blog_index.html", context)

def blog_category(request, category):
  posts = Post.objects.filter(
    categories__name__contains = category
  ).order_by(
    '-created_on'
  )
  
  context = {
    "category": category,
    "posts": posts,
    "isAuthor": False,
    "title": f'{category} Posts'
  }
  
  return render(request,"blog_category.html", context)

def blog_author(request, author):
  posts = Post.objects.filter(
    author__contains = author
  ).order_by(
    '-created_on'
  )
  
  context = {
    "category": author,
    "isAuthor": True,
    "posts": posts,
    "title": f'{author} Posts'
  }
  
  return render(request,"blog_category.html", context)

def blog_delete(request,pk):
  Post.objects.get(pk=pk).delete()
  return blog_index(request)

def blog_detail(request, pk):
  post = Post.objects.get(pk=pk)
  
  form = CommentForm()
  if request.method == 'POST':
    form = CommentForm(request.POST)
    if form.is_valid():
      comment = Comment(
        author = form.cleaned_data['author'],
        body = form.cleaned_data['body'],
        post = post
      )
      comment.save()
  
  comments = Comment.objects.filter(post=post)
  context = {
    "comments": comments,
    "post": post,
    "form": form,
    "title": f'{post.title}'
  }
  
  return render(request,"blog_detail.html", context)

def register(request):
    if request.method == "GET":
        return render(
            request, "register.html",
            {"form": CustomUserCreationForm}
        )
    elif request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.backend = "django.contrib.auth.backends.ModelBackend"
            user.save()
            login(request, user)
            return redirect("blog_index")
        else:
            return render(
            request, "register.html",
            {"form": CustomUserCreationForm, "message": True}
        )
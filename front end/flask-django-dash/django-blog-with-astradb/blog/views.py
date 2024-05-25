from django.shortcuts import render, redirect
from .models import PostModel

# Create your views here.
def home(request):
    posts_list = sorted(list(PostModel.objects.all()), key=lambda p: p.created_at)
    return render(request, 'index.html', {'posts': posts_list})

def posts(request, pk):
    post = PostModel.objects.get(id=pk)
    return render(request, 'post.html', {'post':post})

def newpost(request):
    if request.method == 'POST':
        title = request.POST['title']
        body = request.POST['body']

        new_post = PostModel.objects.create(title=title, body=body)
        new_post.save
        return redirect('/')
    else:
        return render(request, 'newpost.html')
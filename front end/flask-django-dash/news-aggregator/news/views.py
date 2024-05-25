from django.shortcuts import render, redirect
import requests
from django.contrib import messages
from django.contrib.auth.models import User, auth
from .models import News
from django.contrib.auth.decorators import login_required

# Create your views here.
def all_news():
    url = "https://newsnow.p.rapidapi.com/"

    payload = {
        "text": "Europe",
        "region": "wt-wt",
        "max_results": 25
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "082e1babc4msh087e1333d34ef31p1c8f2cjsn7bfaaa543524",
        "X-RapidAPI-Host": "newsnow.p.rapidapi.com"
    }

    response = requests.post(url, json=payload, headers=headers)

    news_list = []

    if response.status_code == 200:
        data = response.json()

        for news_item in data.get('news', []):
            news_dict = {
                "title": news_item.get('title'),
                "body": news_item.get('body'),
                "url": news_item.get('url'),
                "image": news_item.get('image')
            }

            news_list.append(news_dict)

    return news_list

def trending_news():
    url = "https://newsnow.p.rapidapi.com/topheadline"

    payload = {}
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "082e1babc4msh087e1333d34ef31p1c8f2cjsn7bfaaa543524",
        "X-RapidAPI-Host": "newsnow.p.rapidapi.com"
    }

    response = requests.post(url, json=payload, headers=headers)

    headlines_list = []

    if response.status_code == 200:
        data = response.json()

        for news_item in data.get('Top-Headlines', []):
            title = news_item.get('title')
            url = news_item.get('url')
            headlines_list.append({"title": title, "url": url})

    return headlines_list[:10]

def featured_news():
    url = "https://newsnow.p.rapidapi.com/"

    payload = {
        "text": "Top news",
        "region": "wt-wt",
        "max_results": 1
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "082e1babc4msh087e1333d34ef31p1c8f2cjsn7bfaaa543524",
        "X-RapidAPI-Host": "newsnow.p.rapidapi.com"
    }

    response = requests.post(url, json=payload, headers=headers)
    news_list = []

    if response.status_code == 200:
        data  = response.json()

        for news_item in data.get('news', []):
            title = news_item.get('title')
            news_url = news_item.get('url')
            body = news_item.get('body')
            image = news_item.get('image')
            news_list.append({"title": title, "url": news_url, "body": body, "image": image})

    return news_list
    

def index(request):
    featured = featured_news()
    trending = trending_news()
    news = all_news()

    context = {
        'featured_news': featured,
        'trending_news': trending,
        'all_news': news,
    }
    return render(request, 'index.html', context)

def signup(request):
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                # log user in 
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)
                return redirect('/')
        else:
            messages.info(request, 'Password Not Matching')
            return redirect('signup')
    
    else:
        return render(request, 'signup.html')
    
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('login')
    return render(request, 'login.html')

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')

@login_required(login_url='login')
def saved(request):
    user = request.user

    saved_news = News.objects.filter(owner=user)

    context = {
        'saved_news': saved_news
    }
    return render(request, 'saved.html', context)

@login_required(login_url='login')
def save_post(request):
    user = request.user

    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        image_url = request.POST['image']
        link = request.POST['url']

        if News.objects.filter(title=title, description=description, image_url=image_url, link=link, owner=user).exists():
            return redirect('/saved')
        else:
            News.objects.create(title=title, description=description, image_url=image_url, link=link, owner=user)
            return redirect('/saved')
        
    else:
        return redirect('/saved')

@login_required(login_url='login')
def remove_post(request):
    user = request.user

    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        image_url = request.POST['image']
        link = request.POST['url']

        if News.objects.filter(title=title, description=description, image_url=image_url, link=link, owner=user).exists():
            News.objects.filter(title=title, description=description, image_url=image_url, link=link, owner=user).delete()
            return redirect('/saved')

    else:
        return redirect('/saved')
from django.urls import path
from django.urls.conf import include
from . import views

urlpatterns = [
    path("", views.blog_index, name="blog_index"),
    path("<int:pk>/", views.blog_detail, name="blog_detail"),
    path("<int:pk>/delete/", views.blog_delete, name="blog_delete"),
    path("author/<str:author>",views.blog_author, name="blog_author"),
    path("accounts/", include("django.contrib.auth.urls")),
    path('register/',views.register,name="register"),
    path("<str:category>/", views.blog_category, name="blog_category"),
] 
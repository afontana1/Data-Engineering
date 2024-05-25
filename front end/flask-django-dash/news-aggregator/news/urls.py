from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup, name='signup'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('save-post', views.save_post, name='save-post'),
    path('remove-post', views.remove_post, name='remove-post'),
    path('saved', views.saved, name='saved'),
]
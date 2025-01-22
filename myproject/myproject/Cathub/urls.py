from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import user_passes_test

Cathub = ''
urlpatterns = [
    path('', login_required(views.page1), name='Home'),
    path('signup/',views.signup, name='signup'),
    path('signin/',views.signin, name='signin'), 
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'), 
    path('adopt/', views.adopt, name='adopt'), 
    path('post/', views.post_cat, name='post'), 
    path('cat/<int:cat_id>/', views.cat_detail, name='cat_detail'),
    path('home/', views.page1, name='home'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('match/', views.match, name='match'),
    path('profile/<str:username>/', views.user_profile, name='user_profile'),
    path('cat/delete/<int:cat_id>/', views.delete_cat, name='delete_cat'),


]

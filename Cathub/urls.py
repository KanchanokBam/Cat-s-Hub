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
    path('profile/', views.profile_page, name='profile'), 
    path('adopt/', views.adopt, name='adopt'), 
    path('post/', views.post_cat, name='post'), 
    path('cat/<int:cat_id>/', views.cat_detail, name='cat_detail'),
    path('home/', views.page1, name='home'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('match/', views.match, name='match'),
    path('profile/<str:username>/', views.user_profile, name='user_profile'),
    path('cat/delete/<int:cat_id>/', views.delete_cat, name='delete_cat'),
    path('edit_cat/<int:cat_id>/', views.edit_cat, name='edit_cat'),
    path('statistics/', views.statistics, name='statistics'),
    path('find-cat/', views.find_cat, name='find_cat'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-dashboard/addcat/', views.add_cat, name='add_cat'),
    path('admin-dashboard/adduser/', views.add_user, name='add_user'),
    path('admin-dashboard/edit/<int:cat_id>/', views.edit_cat_admin, name='edit_cat_admin'),
    path('admin-dashboard/delete/<int:cat_id>/', views.admin_delete_cat, name='admin_delete_cat'),
    path('admin-dashboard/delete-user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('admin-dashboard/edit-user/<int:user_id>/', views.edit_user, name='edit_user'),
    

]

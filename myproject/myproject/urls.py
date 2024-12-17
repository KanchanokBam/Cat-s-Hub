from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('Cathub.urls')),
    #path('', members, name='home'),
    path('admin/', admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
    
]






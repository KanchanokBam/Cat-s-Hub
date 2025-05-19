from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns  # เพิ่มบรรทัดนี้

urlpatterns = [
    path('admin/', admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
] + i18n_patterns(
    path('', include('Cathub.urls')),  # เพิ่ม i18n_patterns รอบ URL ของแอป
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
import  main.views as main_views

admin.site.site_header = "Панель администрирования новостного портала"
admin.site.index_title = "Новости портала"

handler404 =main_views.custom_404

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include ('main.urls')),
    path('registration/', include ('users.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns=[
        path('__debug/__', include(debug_toolbar.urls)),
    ]+ urlpatterns

    urlpatterns+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
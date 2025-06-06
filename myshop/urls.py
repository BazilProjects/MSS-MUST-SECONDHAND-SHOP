from django.contrib import admin
from django.urls import path  , include, re_path
from django.conf.urls.static import static
from . import settings
from django.urls import path, re_path
from django.views.static import serve
from django.conf.urls import (
                                handler400,
                                handler403,
                                handler404,
                                handler500)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("products.urls")),  # Include the products app URLs
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
]


#if settings.DEBUG:
urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL,
                              document_root=settings.STATIC_ROOT)


# project/urls.py



handler404 = 'products.views.custom_404'
handler403 = 'products.views.custom_403'
handler500 = 'products.views.custom_500'

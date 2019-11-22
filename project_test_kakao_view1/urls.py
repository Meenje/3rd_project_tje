from django.contrib import admin
from django.urls import path, include

from klogin import views, urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('klogin/', include(urls)),
    path('accounts/', include('allauth.urls')),
    path('', views.login),
]

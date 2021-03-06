"""phonathon URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from django.views.generic.base import RedirectView

from ccall import views as ccall_views

urlpatterns = [
    url(r'^login/$', ccall_views.LoginView.as_view(), name='login'),
    url(r'^logout/$', ccall_views.LogoutView.as_view(), name='logout'),
    url(r'^ccall/$', ccall_views.home, name='ccall'),
    url(r'^admin/upload/$', ccall_views.upload, name='upload'),
    url(r'^admin/upload_pool/$', ccall_views.upload_pool, name='upload_pool'),
    url(r'^admin/', admin.site.urls),
    url(r'^$', RedirectView.as_view(url='ccall')),
]

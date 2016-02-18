"""user_password URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.views.generic import TemplateView
from myapp.views import \
 index, register_page, logout_page, login_page, change_password_page

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', index, name='index'),
    url(r'^register/', register_page, name='register'),
    url(r'^login/', login_page, name='login_page'),
    url(r'^logout/', logout_page, name='logout_page'),
    url(r'^changepass/', change_password_page, name='change_password'),
    url(r'^success/', TemplateView.as_view(template_name='myapp/register_success.html'))
]

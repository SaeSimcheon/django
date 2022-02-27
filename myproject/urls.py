"""myproject URL Configuration

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
from django.conf.urls import url,include
from django.urls import path
from django.contrib import admin

# http://127.0.0.1/
# http://127.0.0.1/app/
# http://127.0.0.1/create/
# http://127.0.0.1/read/1/

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    path('',include('myapp.urls')) # 여기에는 우리가 위임하려고 하는 app의 이름인 myapp 입력
    # 또, 그 아래의 urls.py를 사용하라는 의미에서 urls
]

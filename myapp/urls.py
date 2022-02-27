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
from django.conf.urls import url 
from django.urls import path
#from django.contrib import path
from myapp import views


urlpatterns = [
    path('',views.index), # 사용자가 경로를 지정하지 않고 접속했을때 index 함수로 위임하기 위해서는 어떻게 해야하느냐 ?
    # 두번째 파라미터로 from myapp import views를 import하고
    # views.index로 넣어줌.
    # 일단 아래도 똑같이 
    path('creat/',views.Create),
    path('read/<id>/',views.read)
]


- 프로젝트 생성
```console
django-admin startproject config .
```

- 데이터 베이스 초기화
```console
python3 manage.py migrate
```

- 관리자 계정 생성

```console
python3 manage.py createsuperuser
```


### Photo 앱 만들기

#### 앱 만들기

```console
python3 manage.py startapp photo
```

#### settings.py 파일 안의 INSTALLED_APPS에 추가하기.

```python
# /dstagram/config/settings.py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'photo',
]

```

##### 모델 만들기

```python
#/dstagram/photo/models.py
from distutils.command.upload import upload
from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Photo(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_photos')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d',default='photos/no_image.png')
    text = models.TextField()
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now=True)

```

모델은 항상 클래스 형태로 만들고 models.Model을 상속 받음. Photo 모델에는 총 5개의 필드를 만듦.

1. author : ForeignKey를 사용하여 User 테이블과 관계를 만듦. User 모델은 장고에서 기본적으로 사용하는 사용자 모델. 
  on_delete 인수는 연결된 모델이 삭제될 경우 현재 모델의 값을 처리하는 방법.삭제 될 때의 동작은 다음과 같은 옵션을 선택할 수 있음.
  - CASCADE : 연결된 객체가 지워지면 해당 하위 객체도 같이 삭제.
   
2. photo : 사진 필드. upload_to는 사진이 업로드 될 경로를 설정. 만약 업로드가 되지 않을 경우 default 값으로 대체.
3. text : 사진에 대한 설명을 저장할 텍스트 필드.
4. created : 글 작성 일을 저장하기 위한 날짜/시간 필드. auto_now_add 옵션을 설정하면 객체가 추가될 때 자동으로 값을 설정.
5. updated : 글 수정 일을 저장하기 위한 날짜/시간 필드. auto_now 옵션을 설정하면 객체가 수정도리 때마다 자동으로 값을 설정.

- 필드는 나중에 더 추가할 것. 옵션 클래스인 Meta class 추가하기. Photo 모델에 Meta class를 추가하고 ordering 값을 설정.


```python
# /dstagram/photo/models.py
from distutils.command.upload import upload
from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Photo(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_photos')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d',default='photos/no_image.png')
    text = models.TextField()
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now=True)

    class Meta :
        ordering = ['-updated']
```

- ordering class 변수는 해당 모델의 객체들을 어떤 기준으로 정렬할 것인지 설정하는 옵션. -updated로 설정했으니 글 수정 시간의 내림차순으로 정렬.

- Meta class 다음으로 __str__ 메서드 추가.


```python
# /dstagram/photo/models.py
from distutils.command.upload import upload
from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Photo(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_photos')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d',default='photos/no_image.png')
    text = models.TextField()
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now=True)

    class Meta :
        ordering = ['-updated']

    def __str__(self):
        return self.author.username + " " + self.created.strftime("%Y-%m-%d %H:%M:%S")
        
```

- 작성자의 이름과 글 작성일을 합친 문자열을 반환함.


```python
# /dstagram/photo/models.py
from distutils.command.upload import upload
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.


class Photo(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_photos')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d',default='photos/no_image.png')
    text = models.TextField()
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now=True)

    class Meta :
        ordering = ['-updated']

    def __str__(self):
        return self.author.username + " " + self.created.strftime("%Y-%m-%d %H:%M:%S")

    def get_absolute_url(self):
        return reverse("photo:photo_detail",args=[str(self.id)])


```

- get_absolute_url은 객체의 상세 페이지의 주소를 반환하는 메서드.
- 객체를 추가하거나 수정했을 때 이동할 주소를 위해 호출되기도 하고 템플릿에서 상세 화면으로 이동하는 링크를 만들때 호출하기도 함.
- reverse : URL 패턴 이름을 가지고 해당 패턴을 찾아 주소를 만들어주는 함수.
- 여기서 상세 화면의 패턴 이름을 photo:photo_detail로 설정했는데 아직 만들지 않은 뷰이지만, get_absolute_url을 호출하기 전까지는 오류가 발생하지 않기 때문에 미리 만들어도 상관 없음.
- 마지막 인수인 args는 여러 값들을 리스트로 전달하는 데에 사용되는데 여기서는 URL을 만드는데에 필요한 pk 값을 전달하는 데에 사용함.



##### 모델을 데이터베이스에 적용하기.
- makemigrations 명령어를 통해 모델의 변경 사항을 기록함.


```console
python3 manage.py makemigrations photo
```
![image](https://user-images.githubusercontent.com/49121293/160738923-65c8a88c-46cf-459e-b403-ce75155cb0fb.png)


- makemigrations를 이용해 기록한 변경사항을 데이터베이스에 적용하려면 migrate 명령을 사용.

```console
python3 manage.py migrate photo 0001
```


![image](https://user-images.githubusercontent.com/49121293/160739144-54fc6700-22fe-4d7f-b746-1ba9c83017c5.png)


#### 관리자 사이트에 모델 등록

- 관리자 사이트에 모델을 등록하면 모델을 관리하는 뷰를 만들기 전에도 모델을 테스트해볼 수 있음.


```python
# /home/saesimcheon/workspace/dstagram/photo/admin.py
from django.contrib import admin
from .models import Photo
# Register your models here.

admin.site.register(Photo)


```

서버를 실행하여 관리자 페이지에서 사진 올려보기


![image](https://user-images.githubusercontent.com/49121293/160740487-ae157d61-2b34-4244-b006-a9f2afcd6e2a.png)


![image](https://user-images.githubusercontent.com/49121293/160740950-e5b77217-4f06-4469-9845-7e32ac1b9f8b.png)


- 업로드된 파일은 phtos 폴더 밑에 업로드 년월일 순으로 폴더를 만들고 그 안에 저장되어 있는데 앱이 많이진 경우를 생각해보면 프로젝트 루트에 수많은 폴더가 생기게 되어 지저분해질 수 있음.
- 파일들이 모이는 폴더를 따로 하나 만들어서 관리해보기.


#### 업로드 폴더 관리

- 각 앱에서 업로드 하는 파일들을 한 폴더를 중심으로 모으려면 settings.py에 MEDIA_ROOT라는 옵션을 설정해야함.


```python
/home/saesimcheon/workspace/dstagram/config/settings.py
MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR,'media')
```

- MEDIA_ROOT의 값을 프로젝트 루트 밑에 media 폴더로 설정. 그러면 어떤 앱에서 업로드를 하더라도 media 폴더 밑에 각 앱별로 폴더를 만들고 파일을 업로드 하게 됨.
- MEDIA_URL은 STATUC_URL처럼 파일을 브로우저로 서빙할 때 보여줄 가상의 URL.
- 가상 URL은 여러 가지 편의도 있지만 보안을 위해서 필요한 기능.


![image](https://user-images.githubusercontent.com/49121293/160742367-65d84298-5a5f-4c33-bc9b-7f2c914723e8.png)


- 다시 파일을 올리고 폴더를 확인해보면

![image](https://user-images.githubusercontent.com/49121293/160742415-f2664e05-78c4-4695-a1f3-efe3ecc4cf5a.png)

- media 폴더가 생성된 것을 확인할 수 있음. photos 폴더는 제거 하기

#### 관리자 페이지 커스터마이징



```python
# /home/saesimcheon/workspace/dstagram/photo/admin.py
from django.contrib import admin
from .models import Photo
# Register your models here.




class PhotoAdmin(admin.ModelAdmin):
    list_display = ["id","author","created","updated"]
    raw_id_fields = ["author"]
    list_filter = ['created','updated','author']
    search_fields = ['text','created']
    ordering = ['-updated','-created']

admin.site.register(Photo,PhotoAdmin)

```

1. list_display : 목록에 보일 필드 설정. 모델의 필드를 선택하거나 별도 함수를 만들어 필드처럼 등록 가능.
2. raw_id_fields : ForeignKey 필드의 경우 연결된 모델의 객체 목록을 출력하고 선택해야 하는데 목록이 너무 길 경우 불편해짐. 이런 경우 raw_id_fields로 설정하면 값을 써넣는 형태로 바뀌고 검색 기능을 사용해 선택할 수 있게 됨.
3. list_filter : 필터 기능을 사용할 필드를 선택. 장고가 적절하게 필터 범위를 출력해줌.
4. search_fields : 검색 기능을 통해 검색할 필드를 선택. ForeignKey 필드는 설정할 수 없음.
5. ordering : 모델의 기본 정렬값이 아닌 관리자 사이트에서 기본으로 사용할 정렬 값을 설정.


![image](https://user-images.githubusercontent.com/49121293/160745067-2a7edf05-7567-4833-8428-681f45cde24f.png)



위처럼 변경됨.


#### 뷰 만들기
- 사진 목록, 업로드, 확인, 수정, 삭제 기능을 위한 뷰를 만들기.

##### 목록 뷰 만들기
- 함수 형뷰로 만들기 위해 photo_list라는 함수를 만듦.
- 함수형 뷰는 기본 매개변수로 request를 설정. 클래스형 뷰와는 달리 모든 기능을 직접 처리.
- 목록으로 출력할 사진 객체를 불러오기 위해 Photo 모델의 기본 매니저인 objects를 이용해 all메서드 호출.
- 데이터베이스에 저장된 모든 사진을 불러옴.
- 그리고 render 함수를 사용해서 list.html 템플릿을 랜더링함. 
- photos라는 템플릿 변수를 같이 전달.

```python
# /home/saesimcheon/workspace/dstagram/photo/views.py
from django.shortcuts import render
from .models import Photo
# Create your views here.

def photo_list(request):
    photos = Photo.objects.all()
    return render(request,'photo/list.html',{'photos':photos})


```
##### 업로드 뷰 만들기
- 제네릭 뷰를 사용.
- 나머지도 미리 임포트


```python
# /home/saesimcheon/workspace/dstagram/photo/views.py
from re import template
from django.shortcuts import render
from .models import Photo
from django.views.generic.edit import CreateView,DeleteView,UpdateView
# Create your views here.
from django.shortcuts import redirect
def photo_list(request):
    photos = Photo.objects.all()
    return render(request,'photo/list.html',{'photos':photos})

class PhotoUploadView(CreateView):
    model = Photo
    fields = ["photo",'text']
    template_name = 'photo/upload.html'

    def form_valid(self,form):
        form.instance.author_id = self.request.user.id

        if form.is_valid():
            form.instance.save()
            return redirect('/')
        else:
            return self.render_to_response({'form':form})
```


- PhotoUploadView에는 template_name이라는 클래스 변수. 실제 사용할 템플릿 설정. 
- form_valid 메서드는 업로드를 끝낸 후 이동할 페이지를 호출하기 위해 사용하는 메서드.
- 이 메서드를 오버라이드해서 작성자를 설정하는 기능을 추가함.
- 작성자는 현재 로그인 한 사용자로 설정.
- 작성자를 설정하고 valid 메서드를 이용해 입력된 값들을 검증.
- 이상이 없다면 데이터베이스에 저장하고 redirect 메서드를 이용해 메인페이지로 이동.
- 만약 이상이 있다면 작성된 내용을 그대로 작성 페이지에 표시함.

```python
from re import template
from django.shortcuts import render
from .models import Photo
from django.views.generic.edit import CreateView,DeleteView,UpdateView
# Create your views here.
from django.shortcuts import redirect
def photo_list(request):
    photos = Photo.objects.all()
    return render(request,'photo/list.html',{'photos':photos})

class PhotoUploadView(CreateView):
    model = Photo
    fields = ["photo",'text']
    template_name = 'photo/upload.html'

    def form_valid(self,form):
        form.instance.author_id = self.request.user.id

        if form.is_valid():
            form.instance.save()
            return redirect('/')
        else:
            return self.render_to_response({'form':form})

class PhotoDeleteView(DeleteView):
    model = Photo
    success_url = '/'
    template_name = 'photo/delete.html'

class PhotoUpdateView(UpdateView):
    model = Photo
    fields = ["photo",'text']
    template_name = 'photo/update.html'
```

- 나머지 뷰들도 적절히 만들어 주기. '/'는 사이트 메인을 뜻함.
- Detail 뷰는 나중에 따로 만들기

#### URL 연결하기

```python
# /home/saesimcheon/workspace/dstagram/photo/urls.py
from django.urls import path
from django.views.generic.detail import DetailView
from .views import *
from .models import Photo

app_name = 'photo'

urlpatterns = [
    path ('',photo_list,name='photo_list'),
    path ('detail/<int:pk>/',DetailView.as_view(model = Photo,template_name = 'photo/detail.html'),name='photo_detail'),
    path ('upload/',PhotoUploadView.as_view(),name='photo_upload'),
    path ('delete/<int:pk>/',PhotoDeleteView.as_view(),name='photo_delete'),
    path ('update/<int:pk>/',PhotoUpdateView.as_view(),name='photo_update'),
]
```

- 함수형 뷰는 이름만 써주고 클래스형 뷰는 .as_view()

##### 이번 장에서 작성한 urls.py에서는 챙겨봐야할 부분이 두가지.
1. app_name 이라는 변수 : 네임스페이스로 사용되는 값.
    - 템플릿에서 URL 템플릿 태그를 사용할 대 app_name 값이 설정되어 있다면 app_name:URL패턴 ㅣㅇ름 형태로 사용.
2. 제네릭 뷰를 그대로 사용하는 인라인 뷰 : 제네릭 뷰인 DetailView는 views.py가 아닌 urls.py에서 인라인 코드로 작성할 수 있음. path 함수에 인수로 전달할때는 as_view 안에 클래스 변수들을 설정해 사용.


##### 루트 urls.py에 앱의 urls.py를 연결해주기.


- /home/saesimcheon/workspace/dstagram/templates/base.html
```html

<html lang = 'en'>
<head>
    <meta charset ="UTF-8">
    <meta name="viewport" content="width=device-width",initial-scale=1,
    shirink-to-fit="no">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-ka7Sk0Gln4gmtz2MlQnikT1wXgYsOg+OMhuP+IlRH9sENBO0LRn5q+8nbTov4+1p" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.10.2/dist/umd/popper.min.js" integrity="sha384-7+zCNj/IqJ95wo16oMtfsKbZ9ccEh31eOz1HGyDuCQ6wgnyJNSYdrPa03rtR1zdB" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.min.js" integrity="sha384-QJHtvGhmr9XOIpI6YVutG+2QOK9T+ZnN4kzFN1RtK3zEFEIsxhlmWl5/YESvpZ13" crossorigin="anonymous"></script>

    <title>Dstagram {% block title %}{% endblock %}</title>
</head>    

<body>
<div class = "container">
    <header class="header clearfix">
        <nav class="navbar navbar-expand-lg navbar-light bg-light">
            <a class="navbar-brand" href="/">Dstagram</a>
            <ul class="nav">
                <li class="nav-item">
                    <a href="/" class = "activa nav-link ">Home</a>
                </li>
                {% if user.is_authenticated %}
                <li class="nav-item">
                    <a href="#" class="nav-link">Welcom, {{user.get_username}}</a>
                </li>
                <li class="nav-item">
                    <a href="{% url 'photo:photo_upload' %}" class="nav-link">Upload</a>
                </li>
                <li class="nav-item"><a href="#" class="nav-link">Logout</a></li>
                {% else %}
                <li class="nav-item"><a href="#" class="nav-link">Login</a></li>
                <li class="nav-item"><a href="#" class="nav-link">Signup</a></li>
                {% endif %}
            </ul>
        </nav>
    </header>

    {% block content %}
    {% endblock %}

    <footer class="footer">
        <p>&copy; Powered By Django 3</p>
    </footer>
</div>
</body>
</html>
```



- 부트스트랩 적용.
- 메뉴바 만들어서 상단에 배치
- 중간에는 내용을 출력하도록 content block을 만듦.
- 최하단에는 푸터
- 메뉴바는 로그인 한 상태와 로그아웃 한 상태에 따라 다르게 보이도록 만들었음.
- 모든 페이지에서 user 객체를 사용할 수 있음. : 이때 is_authenticated 값을 이용해 로그인 여부를 판단할 수 있음.
- base.html을 추가했으니 템플릿이 검색되도록 settings.py에 경로 추가.


```python
# /home/saesimcheon/workspace/dstagram/config/urls.py
"""config URL Configuration

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
from django.urls import path,include
urlpatterns = [
    path('admin/',admin.site.urls),
    path('',include('photo.urls')),
]

```



![image](https://user-images.githubusercontent.com/49121293/160754542-c2d50db6-510e-49ce-b2c8-8425057c1260.png)




- TEMPLATES 변수에 있는 DIRS 키의 값을 추가함.

```python
# /home/saesimcheon/workspace/dstagram/config/settings.py
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,"templates")], # 이 부분 수정.
        'APP_DIRS': True, 
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

```


- /home/saesimcheon/workspace/dstagram/templates/base.html 
```html
{% extends 'base.html' %}

{% block title %}- LIST{% endblock %}

{% block content %}
    {% for post in photos %}
        <div class="row">
            <div class="col-md-2"></div>
            <div class="col-md-8 panel panel-default">
                <p><img src="{{post.photo.url}}" style = "width:100%;"></p>
                <button type="button" class="btn btn-xs btn-info">
                    {{post.author.username}}
                </button>
                <p>{{post.text|linebreaksbr}}</p>
                <p class="text-right">
                    <a href="{% url 'photo:photo_detail' pk=post.id %}" class="btn btn-xs btn-success">댓글달기</a>
                </p>
            </div>
            <div class="col-md-2"></div>
        </div>
    {% endfor %}
{% endblock %}
```

##### 업로드 뷰의 템플릿 작성
- /home/saesimcheon/workspace/dstagram/photo/templates/photo/upload.html
```html

{% extends 'base.html' %}
{% block title %}- Upload{% endblock %}

{% block content %}
<div class="row">
    <div class="col-md-2"></div>
    <div class="col-md-8 panel panel-default">
        <form action="" method ="post" enctype="multipart/form-data">
            {{form.as_p}}
            {% csrf_token %}
            <input type="submit" class="btn btn-primary" value="Upload">
        </form>
    </div>
    <div class="col-md-2"></div>
</div>
{% endblock %}
```

- 업로드 뷰는 form 태그를 사용해 구성.
- form 태그의 enctype을 잘 보기. form 태그로 작성한 정보를 어떤 형태로 인코딩 해서 서버로 전달할지에 대한 옵션.
- mehtod가 post일때만 사용 가능.

- 사용할 수 있는 옵션 목록 
    - application/x-www-from-urlencoded : 기본 옵션. 모든 문자열을 인코딩해 전달하며 특수문자는 ASCII HEX 값으로 변환하고 띄어쓰기는 +로 변환.
    - multipart/form-data : 파일 업로드 때 사용하는 옵션이며 데이터를 문자열로 인코딩하지 않고 전달.
    - text/plain : 띄어쓰기만 +로 변환하고 특별한 인코딩 없이 전달.

- 템플릿을 작성했으면 상단 메뉴바에 있는 Upload 버튼을 클릭해 화면을 확인하고 이미지를 업로드 해보기.
- 아직 사진이 정상적으로 나오지는 않음.



- detail 탬플릿 생성.
```python
# /home/saesimcheon/workspace/dstagram/photo/templates/photo/detail.html
{% extends 'base.html' %}

{% block title %}
    {{object.text|truncatechars:100}}
{% endblock %}

{% block content %}
    <div class="row">
        <div class="col-md-2"></div>
        <div class="col-md-8 panel panel-default">
            <p><img src="{{object.photo.url}}" style="width:100%;"></p>
            <button type="button" class="btn btn-outline-primary btn-sm">
                {{object.author.username}}
            </button>
            <p>{{object.text|linebreaksbr}}</p>

            <a href="{% url 'photo:photo_delete' pk=object.id %}" class="btn btn-outline-danger btn-sm float-right">
                Delete
            </a>
            <a href="{% url 'photo:photo_update' pk=object.id %}" class="btn btn-outline-success btn-sm float-right">
                Update
            </a>
        </div>
        <div class="col-md-2"></div>
    </div>
{% endblock %}
```

##### 여전히 이미지가 제대로 출력되지 않는데 이는 urls.py를 수정해야한다.

```python
# /home/saesimcheon/workspace/dstagram/config/urls.py
from django.conf.urls import url
from django.contrib import admin
from django.urls import path,include

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/',admin.site.urls),
    path('',include('photo.urls')),
]

urlpatterns += static(settings.MEDIA_URL,document_root =settings.MEDIA_ROOT)

```


- static을 사용해서 MEDIA_URL에 해당하는 주소를 가진 요청에 대해서는 MEDIA_ROOT에서 찾아서 응답하도록 urlspatterns에 추가하는 구문. 이 구문은 디버그 모드가 True일 때만 동작함.


##### 나머지 템플릿들도 완성



```python
# /home/saesimcheon/workspace/dstagram/photo/templates/photo/update.html
{% extends 'base.html' %}
{% block title %}- Update{% endblock %}

{% block content %}
<div class="row">
    <div class="col-md-2"></div>
    <div class="col-md-8 panel panel-default">
        <form action="" method ="post" enctype="multipart/form-data">
            {{form.as_p}}
            {% csrf_token %}
            <input type="submit" class="btn btn-primary" value="Update">
        </form>
    </div>
    <div class="col-md-2"></div>
</div>
{% endblock %}

```


```python
# /home/saesimcheon/workspace/dstagram/photo/templates/photo/delete.html
{% extends 'base.html' %}
{% block title %}- Update{% endblock %}

{% block content %}
<div class="row">
    <div class="col-md-2"></div>
    <div class="col-md-8 panel panel-default">
        <div class="alert alert-info">
            Do you want to delete {{object}}?
        </div>
        <form action="" method="post">
            {{form.as_p}}
            {% csrf_token %}
            <input type="submit" class="btn btn-primary" value="Confirm">
        </form>
    </div>
    <div class="col-md-2"></div>
</div>
{% endblock %}
```

### Accounts 앱 만들기


#### accoutns 앱 만들기

##### 앱 생성
```console
python3 manage.py startapp accounts
```


##### settings.py에 앱 추가하기


```python
# /home/saesimcheon/workspace/dstagram/config/settings.py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'photo',
    'accounts',
]
```


##### 로그인, 로그아웃 기능 추가
- 로그인, 로그아웃 기능은 장고에 이미 만들어져있는 기능.
- 이 기능을 그대로 불러다 쓰기 위해서 accounts 앱 폴더에 urls.py를 만들고 있는 뷰를 불러다가 씀.
- 
```python
# /home/saesimcheon/workspace/dstagram/accounts/urls.py
from django.urls import path
from django.contrib.auth import views as auth_view

urlpatterns = [
    path('login/',auth_view.LoginView.as_view(),name='login'),
    path('logout/',auth_view.LogoutView.as_view(template_name='registration/logout.html'),name='logout'),
]
```


- urls.py를 사용하기 위하여 루트 urls.py에 연결.

```python
# /home/saesimcheon/workspace/dstagram/config/urls.py
from django.conf.urls import url
from django.contrib import admin
from django.urls import path,include

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/',admin.site.urls),
    path('',include('photo.urls')),
    path('accounts/',include('photo.urls')),
]

urlpatterns += static(settings.MEDIA_URL,document_root =settings.MEDIA_ROOT)

```


- 템플릿 만들기

- /home/saesimcheon/workspace/dstagram/accounts/templates/registration/login.html
```html

{% extends 'base.html' %}
{% block title %}-Login{% endblock %}

{% block content %}
<div class="row">
    <div class="col-md-2"></div>
    <div class="col-md-8 panel panel-default">
        <div class="alert alert-info">Please enter your login information</div>
        <form action="" method="post">
            {{form.as_p}}
            {% csrf_token %}
            <input class="btn btn-primary" type="submit" value="Login">
        </form>
    </div>
    <div class="col-md-2"></div>
</div>
{% endblock %}
```




- /home/saesimcheon/workspace/dstagram/accounts/templates/registration/logout.html
```html

{% extends 'base.html' %}
{% block title %}-Logout{% endblock %}

{% block content %}
<div class="row">
    <div class="col-md-2"></div>
    <div class="col-md-8 panel panel-default">
        <div class="alert alert-info">You have been successfully logged out. </div>
        <a class="btn btn-primary" href="{% url 'login' %}">Click to Login</a>
    </div>
    <div class="col-md-2"></div>
</div>
{% endblock %}
```


- 두 템플릿을 메인메뉴에 있는 링크와 연결해주기. 
- base.html에서 login,logout 링

- /home/saesimcheon/workspace/dstagram/templates/base.html
- href 속성 수정.
```html

<li class="nav-item"><a href="{% url 'logout' %}" class="nav-link">Logout</a></li>
                {% else %}
                <li class="nav-item"><a href="{% url 'login' %}" class="nav-link">Login</a></li>
```


![image](https://user-images.githubusercontent.com/49121293/160962320-238f33cb-0015-475c-ad00-620741156e25.png)



![image](https://user-images.githubusercontent.com/49121293/160962400-87030eb4-974f-4218-b2a7-d4bf12740f5a.png)


- 이런 식으로 로그인은 되지만 프로파일이라는 페이지가 없어서 오류가 발생함.
- 로그인 후 이동할 페이지 설정의 기본 값이 profile이기 대문임. 바로 메인 페이지로 이동하도록 변경해보자.
- settings.py의 LOGIN_REDIRECT_URL 변수 추가.



```python
# /home/saesimcheon/workspace/dstagram/config/settings.py

LOGIN_REDIRECT_URL = '/'
```



##### 회원가입 기능 만들기

- 뷰와 폼 만들어야함.



```python
# /home/saesimcheon/workspace/dstagram/accounts/forms.py
from django.contrib.auth.models import User
from django import forms

class RegisterForm(forms.ModleForm):
    password = forms.CharField(label = "Password",widget=forms.PasswordInput)
    password2 = forms.CharField(label = "Repeat Password",widget=forms.PasswordInput)


    class Meta :
        model =User
        fields = ['username','first_name','last_name','email']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('passwords not matched')
        return cd['password2']
```


- 회원 가입 양식을 출력하기 위해서 RegisterForm이라는 클래스를 만듦.
    - 이 클래스는 forms.ModelForm을 상속 받는데 모델이 있고 그에 대한 자료를 입력받고 싶은 경우 사용.
    - 폼 클래스 내부에 있는 Meta class를 이용하면 기존에 있는 모델의 입력 폼을 쉽게 만들 수 있음.
    - model을 설정하고 fields를 이용해서 입력 받을 필드를 지정하면 됨.
    - password2를 만들어서 비밀번호 재입력 기능을 구현하도록 했음.
    - clean_password2는 clean_필드명 형태의 메서드.
    - 각 필드의 clean 메서드 호출된 후에 호출되는 메서드들.
    - 유효성 검사나 조작을 하고 싶은 경우 사용.
    - clean_필드명 형태의 메서드에서 해당 필드의 값을 사용할 때는 clean_data에서 필드 값을 찾아서 써야한다고 함. 이 값이 이전 단계까지 유효성 검사를 마친 상태이기 때문.




- 완성한 폼을 사용해서 뷰를 만들어보자.


```python
from django.shortcuts import render
from .forms import RegisterForm
# Create your views here.


def register(request):
    if request.method =="POST":
        user_form = RegisterForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleand_data['password'])
            new_user.save()
            return render(request , 'registration/register_done.hmtl',{'new_user':new_user})
        
        else:
            user_form = RegisterForm()
        
        return render(request,'registration/register.html',{"form":user_form})



```


```python
# /home/saesimcheon/workspace/dstagram/accounts/views.py

from django.shortcuts import render
from .forms import RegisterForm

def register(request):
    if request.method =="POST":
        user_form = RegisterForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request , 'registration/register_done.html',{'new_user':new_user})
        
    else:
        user_form = RegisterForm()
        
    return render(request,'registration/register.html',{"form":user_form})


```


- 이 뷰에서 기존의 제네릭 뷰에서 어떤 식으로 처리를 하는지 알아볼 수 있는 힌트가 있음.
    - if request.method=="POST" 라는 부분은 회원가입 정보가 서버로 전달 되었다는 으미.
    - 입력을 받는 템플릿들을 보면 form 태그에 method가 post로 설정되어 있는 것을 자주 보았음.
    - post는 http 메서드들 중 하나로 서버로 자료를 전달할 대 사용하는 메서드. 따라서 post 방식으로 뷰를 호출했다는 것은 서버로 자료를 전달하는 상태.
    - 그래서 정보를 전달 받으면 registerform을 이용해서 유효성 검사 후 저장.
    - 저장하는 절차는 두 단계를 거침. 우선 user_form.save 메서드를 통해서 폼 객체에 지정된 모델을 확인하고 이 모델의 객체를 만듦.
    - 이 때 옵션으로 commit=False로 지정했기 때문에 데이터 베이스에 저장하는 것이 아니라, 메모리 상에 객체만 만들어짐.
    - 그리고 set_password 메서드를 사용해 비밀번호를 지정.
    - 이런 과정을 거쳐야 비밀ㅂ번호가 암호화된 상태로 저장됨.
    - 비밀번호까지 지정했다면 new_user의 save 메서드를 호출해 실제로 데이터베이스에 저장함. 
    - 회원가입이 완료 되었으므로 register_done이라는 템플릿을 보여줌.
    - 반대로 post가 아니라면 입력을 받는 페이지를 보여줌. 그래서 비어있는 registerform 객체를 만들고 register 템플릿을 렌더링해서 보여줌.

이 뷰를 사용하기 위해 URL 연결하기




```python
# /home/saesimcheon/workspace/dstagram/accounts/urls.py
from django.urls import path
from django.contrib.auth import views as auth_view
from .views import register
urlpatterns = [
    path('login/',auth_view.LoginView.as_view(),name='login'),
    path('logout/',auth_view.LogoutView.as_view(template_name='registration/logout.html'),name='logout'),
    path('register/',register,name='register'),
]

```
- /home/saesimcheon/workspace/dstagram/accounts/templates/registration/register.html
```html
{% extends 'base.html' %}

{% block title %}- Registration {% endblock %}

{% block content %}
<div class="row">
    <div class="col-md-2"></div>
    <div class="col-md-8 panel panel-default">
        <div class="alert alert-info">Please enter your account information.
        </div>
        <form action="" method="post">
            {{form.as_p}}
            {% csrf_token %}
            <input class="btn btn-primary" type="submit" value="Register">
        </form>
    </div>
    <div class="col-md-2"></div>
</div>
{% endblock %}

```


- /home/saesimcheon/workspace/dstagram/accounts/templates/registration/register_done.html

```html
{% extends 'base.html' %}

{% block title %}- Registration Done{% endblock %}

{% block content %}
<div class="row">
    <div class="col-md-2"></div>
    <div class="col-md-8 panel panel-default">
        <div class="alert alert-info">Registration Success. Welcome, {{new_user.username}}
        </div>
        <a class="btn btn-info" href="/">Move to main</a>
    </div>
    <div class="col-md-2"></div>
</div>
{% endblock %}
```


- base.html에 회원 가입 링크 연결.


- /home/saesimcheon/workspace/dstagram/templates/base.html
```html
<li class="nav-item"><a href="{% url 'register' %}" class="nav-link">Signup</a></li>
```


##### 권한 제어

- 로그인한 사용자만 서비스 이용할 수 있도록 제어하기
- 데코레이터(함수형)와 믹스인()을 사용.


```python
# /home/saesimcheon/workspace/dstagram/photo/views.py
from re import template
from django.shortcuts import render
from .models import Photo
from django.views.generic.edit import CreateView,DeleteView,UpdateView
# Create your views here.
from django.shortcuts import redirect


from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin






@login_required
def photo_list(request):
    photos = Photo.objects.all()
    return render(request,'photo/list.html',{'photos':photos})

class PhotoUploadView(LoginRequiredMixin,CreateView):
    model = Photo
    fields = ["photo",'text']
    template_name = 'photo/upload.html'

    def form_valid(self,form):
        form.instance.author_id = self.request.user.id

        if form.is_valid():
            form.instance.save()
            return redirect('/')
        else:
            return self.render_to_response({'form':form})

class PhotoDeleteView(LoginRequiredMixin,DeleteView):
    model = Photo
    success_url = '/'
    template_name = 'photo/delete.html'

class PhotoUpdateView(LoginRequiredMixin,UpdateView):
    model = Photo
    fields = ["photo",'text']
    template_name = 'photo/update.html'


```

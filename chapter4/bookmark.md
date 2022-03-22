

#### 모델 만들기

- 아래를 선행.

```console
python3 manage.py migrate
```


- 모델은 데이터 베이스 사용을 쉽게 하기 위해 사용하는 도구 
- models.Model을 상속받는 Bookmark 클래스를 만듦.
- 데이터베이스에 생성되는 테이블 이름은 보통 모델의 이름을 따라 만들어짐.
- 앱이름_모델이름 이런 형태로 만들어짐.



```python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Bookmark(models.Model):
    site_name = models.CharField(max_length = 100)
    url = models.URLField('Site URL')
```

##### 모델을 이용해 데이터 베이스에 테이블을 생성하려면 두가지의 명령어를 입력해야함.
##### 데이터베이스 관련 명령어가 제대로 작동하려면 settings.py에 bookmark 앱을 사용하기 위한 설정을 추가해야함.

- config/settings.py 파일의 INSTALLED_APPS 변수에 bookmark 추가. 끝에 ',' 가급적이면 추가해주기.


```python
# config/settings.py
# (생략)
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bookmark',
]

# (생략)

```


```console
python3 manage.py makemigrations bookmark
```
![image](https://user-images.githubusercontent.com/49121293/159501943-a7625fee-a391-4a5c-9059-677ec8711172.png)


```console
python3 manage.py migrate bookmark
```
![image](https://user-images.githubusercontent.com/49121293/159502017-a134c460-2af0-4c7e-ba8a-5ebeee62f5e4.png)


- 앱에서 데이터베이스 관련 변경사항이 있는지 확인하고 변경할 내용이 있다면 파일을 생성함. 이런 파일을 마이그레이션 파일이라고 함.

#### 관리자 페이지에 모델 등록

- 미리 데이터가 필요한 경우가 많아서 미리 모델을 관리할 수 있도록 등록해두면 편리함.

```python
# bookmark/admin.py
from __future__ import unicode_literals
from django.contrib import admin
from .models import Bookmark
admin.site.register(Bookmark)

```

- admin.py는 모델을 관리자 페이지에 등록해 관리할 수 있도록 하는 역할.
- 관리자 페이지에서 보이는 내용의 변경, 기능 추가 등을 할 수 있도록 코드를 입력하는 파일.
- from .models import Bookmakr 구문은 현재 폴더에 있는 models.py파일에서 Bookmark라는 모델을 불러오겠다는 의미.
- admin.site.register 구문을 이용해 등록하면 관리자 페이지에서 해당 모델을 관리할 수 있음.


### 모델 설정 순서 정리

1. 초기 설정 : python3 manage.py migrate
2. 모델 생성 : bookmark(앱이름)/models.py에 Bookmark 모델 생성
3. 전체에 앱 등록 : config/settings.py의 INSTALLED_APPS에 bookmark(앱 이름 추가)
4. 마이그레이션 생성 : python3 manage.py makemigrations bookmark (앱 이름)
5. 마이그레이션 적용 : python3 manage.py migrate bookmark  
6. 관리자 페이지에 모델 추가 : bookmark/admin.py에 모델 추가.



# Q. 저건 뭘까 ? 아마 프라이머리 키 설정이 안 돼서 default 설정된 것 같음.

![image](https://user-images.githubusercontent.com/49121293/159508770-624f1593-33c3-4212-9ef8-57b05a376ccf.png)



- 관리자 페이지를 통해서 예시로 몇 개 등록해보기

![image](https://user-images.githubusercontent.com/49121293/159510282-41e57a4a-4bee-407b-9bb1-f8565ba76692.png)

- 어떤 사이트인지 알아볼 수 없음. 목록에 보면 우리가 알아볼 수 있는 내용은 없고 북마크 모델의 오브젝트라는 내용과 번호만 반복됨.


#### 모델에 __str__ 메서드 추가

- __str__ 메서드의 기능은 클래스 오브젝트를 출력할 때 나타낼 내용을 결정하는 메서드.


```python
# bookmark/models.py

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Bookmark(models.Model):
    site_name = models.CharField(max_length = 100)
    url = models.URLField('Site URL')
    def __str__(self):
        return "이름 : "+self.site_name + ", 주소 :" + self.url

```
- 위처럼 선택하면 아래 같이 나옴.


![image](https://user-images.githubusercontent.com/49121293/159512198-dbf8369a-d922-448b-8688-401b23f7103b.png)

#### 목록 뷰 만들기

- 관리자 페이지를 이용해 모델을 관리할 수 있지만 제대로 된 서비스를 만들기 위해서는 프론트에서 해당 기능을 사용할 수 있어야함.

- 목록 뷰 만들기.


```python
# bookmark/views.py
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic.list import ListView
from .models import Bookmark
# Create your views here.

class BookmarkListView(ListView):
    model = Bookmark

```

- 모든 뷰를 클래스 형 뷰로 만들기. 
- 뷰에는 함수형 뷰와 클래스 형 뷰가 있음.
- 클래스 형 뷰는 웹 프로그래밍에서 자주 사용하는 기능을 장고가 미리 준비 해두었고 가져다 쓰는 형태.
- 북마크 앱은 전형적인 뷰들이 필요하기 때문에 클래스 형 뷰가 적절함.


- ListView를 상속해 사용.
- model을 설정해야주어야 하기 때문에 Bookmark 모델을 임포트 하고 클래스 안에 model = Bookmakr 라는 구문을 이용해 모델 설정.


#### URL 연결하기 


- 뷰를 만들었으면 URL 주소를 사용해 뷰를 사용할 수 있ㄷ록 연결해야함.
- 즉, 어떤 주소를 입력했을 대 해당 페이지를 보여줄지 설정. urls.py 파일에서 설정.
- urls.py 파일은 config 폴더에 있는 루트 파일과 각 앱 폴더에 만들어 두는 서브 파일이 있음.
- 루트 urls.py 파일만 있어도 무방하지만, 한 번 만든 앱은 다른 프로젝트에도 재사용할 수 있기 대문에 앱에 관한 URL 연결은 앱 폴더에 있는 urls.py에 설정.

- 앱에 관한 urls.py의 내용은 루트 파일에서 연결 해주어야만 동작.
- 루트 urls.py 파일을 열고 include 함수를 임포트. urlpatterns에 bookmark.urls를 연결하는 path를 추가한다.



```python
# config/urls.py
from django.conf.urls import url
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('bookmark/',include('bookmark.urls')),
    path('admin/',admin.site.urls),
]
```

- bookmark/까지의 URL을 잘라내고 나머지 부분을 bookmark.urls로 전달해 찾아봄. 나머지 부분을 가지고 어떤 뷰를 연결할지를 bookmark 앱 폴더에 있는 urls.py에 작성하도록 함.
- 남은 문자열이 전달된다. 예를 들면 127.0.0.1:8000/bookmark/가 입력되면 남은 문자열은 ''이므로 매칭되는 path에 연결되어 view가 적용된다.
- 클래스형 뷰는 .as_view()를 항상 붙여주어야 정상작동된다. 
- name은 설정한 이름을 바탕으로 URL 패턴을 찾을 수 있도록 기능함.
```python
# bookmark/urls.py
from django.conf.urls import url
from django.urls import path,include

from .views import BookmarkListView

urlpatterns = [
    path('',BookmarkListView.as_view(),name = 'list'),
]
```

![image](https://user-images.githubusercontent.com/49121293/159534966-257887d6-6553-4c11-b9a2-8266aafaf447.png)

- 템플릿 파일이 없다는 오류 메시지


#### bookmark_list.html 템플릿 만들기

- 템플릿 : 프론트엔드 소스 코드가 저장되는 파일들이며 장고에서 데이터를 끼어 넣는 양식 파일.
- 어떤 뷰를 만들 때는 그 뷰의 내용을 어떻게 브라우저에 표시할지 템플릿을 가지고 결정함.
- 템플릿은 정해진 위치가 있음. 앱 폴더 내부에 templates 폴더에 위치해야 하며 보통 앱 이름으로 폴더를 한번 더 만들어 지정.
- templates/bookmark 폴더 만들어 파일 넣기.


- bookmark/templates/bookmark/bookmark_list.html
- 소스코드 첫 부분에 북마크 추가하기 링크.
- 북마크 목록을 출력하기 위하여 table 태그 사용.
- 제네릭 뷰에서 모델의 오브젝트가 여러 개인 경우 object_list 라는 변수로 전달. object_list에서 북마크를 하나씩 꺼내서 북마크 당 한줄씩 출력할 것.
- 한 북마크는 tr 태그로 묶음. 
- 각 북마크를 출력할 때 사이트 이름 url 등을 출력하고 수정 버튼과 지우기 버튼도 함께 만들기.
```html

<body>
    <div class = "btn-group">
        <a href="#" class = "btn btn-info">Add Bookmark</a>
    </div>
    <p></p>
    <table class="table">
        <thead>
            <tr>
                <th scope="col">#</th>
                <th scope="col">Site</th>
                <th scope="col">URL</th>
                <th scope="col">Modify</th>
                <th scope="col">Delete</th>
            </tr>
        </thead>
        <tbody>
            {% for bookmakr in object_list % }
            <tr>
                <td>{{forloop.counter}}</td>
                <td><a href = "#">{{bookmark.site_name}}</a></td>
                <td><a href="{{bookmakr.url}}"target = "_blank">{{bookmark.url}}</a></td>
                <td><a href="#" class = "btn btn-sucess btn-sm">Modify</a></td>
                <td><a href="#" class = "btn btn-danger btn-sm">Delete</a></td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</body>

```

- 각 태그의 용도 공부해야함.


![image](https://user-images.githubusercontent.com/49121293/159539760-4c4cbb68-b79e-429d-9ca8-cef0190ab665.png)



- 눌러보면 아직 전부 기능하지는 않음. 클릭해보면 url이 임시로 #으로 이동하는 것을 알 수 있음.



#### 북마크 추가 기능 구현 (CREATE)

- 북마크 추가를 위한 뷰를 클래스 뷰로 만듦. 제네릭 뷰인 CreateView를 상속받으면 손쉽게 만들 수 있음.



```python
# bookmark/view.py

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic.list import ListView
from .models import Bookmark
# Create your views here.

from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

class BookmarkListView(ListView):
    model = Bookmark


class BookmakrCreateView(CreateView):
    model=Bookmark
    fields = ['site_name','url'] 
    sucess_url = reverse_lazy('list') # 목록 페이지로 이동. (list 이름을 가진 url로 이동.)
    template_name_suffix = '_create' # 템플릿 파일 사용 설정.
```

- 어던 모델의 입력을 받을 것인지 model 변수를 만들고 Bookmakr로 설정.
- fields 변수는 어떤 필드들을 입력받을 것인지 설정.
- success_url은 글쓰기를 완료하고 이동할 페이지.
- 보통은 상세 페이지로 이동하지만 success_url의 사용법을 알기 위해 목록 페이지로 설정했음.
- template_name_suffix는 사용할 템플릿의 접미사만 변경하는 설정값.
- 기본으로 설정되어 있는 템플릿 이름들은 모델명_xxx 형태. CreateView와 UpdateView는 form이 접미사인데 이걸 변경해서 bookmark_create라는 이름의 템플릿 파일을 사용하도록 설정한 것.

##### view가 response 하는 방법이라는 것을 알 것.
##### 모델 지정 및 필드 설정, url 설정, template 이름 지정.


- bookmark/templates/bookmark/bookmark_create.html

```html
<form action = "" method="post">
    {% csrf_token %}
    {{form.as_p}}
    <input type="submit" value="add" class="btn btn-info btn-sm">
</form>
```


- 이건 CreateView의 기능을 알아야함.
- form 태그는 html로부터 서버로 자료를 전달하기 위해 사용하는 코드.
- 회원가입, 로그인, 글쓰기 등 다양한 기능에 사용.
- action 메서드는 자료를 전달할 대상 페이지. 비워둘 경우 "현재 페이지"로 전달.
- method는 HTTP 메서드 종류를 설정.

- form 태그 안쪽에는 csrf_token 값이 있는데 이를 CSRF공격을 막기 위한 용도. 해커가 만들 외부 사이트에서 우리가 만든 사이트에 로그인 한 사용자 권한 으로 공격하는 것을 막기 위한 용도.
- form.as_p는 클래스형 뷰의 옵션값으로 설정한 필드를 출력하는데 각 필드 폼 태그들을 P태그로 감싸 출력하는 코드.

- 마지막으로 submit 버튼은 입력 완료를 위한 만들어 줌.



- 127.0.0.1:8000/bookmark/add/ 주소로 접속하면 

![image](https://user-images.githubusercontent.com/49121293/159552986-4d01a88f-9d21-4061-b9d2-a9a1a0e95b50.png)



# Q. Site name Site URL로 내가 기입한적이 없는데 어떻게 저렇게 나오지 ??


- Add Bookmark 링크가 동작하도록 만들기 위해서 bookmark_list.html 파일에 있는 Add Bookmark 링크의 href 속성을 변경.


- bookmark/templates/bookmark/bookmark_list.html
- <a href="{% url 'add' %}" class = "btn btn-info">Add Bookmark</a> 이렇게 수정.
```html
<body>
    <div class = "btn-group">
        <a href="{% url 'add' %}" class = "btn btn-info">Add Bookmark</a>
    </div>
    <p></p>
    <table class="table">
        <thead>
            <tr>
                <th scope="col">#</th>
                <th scope="col">Site</th>
                <th scope="col">URL</th>
                <th scope="col">Modify</th>
                <th scope="col">Delete</th>
            </tr>
        </thead>
        <tbody>
            {% for bookmark in object_list %}
            <tr>
                <td>{{forloop.counter}}</td>
                <td><a href = "#">{{bookmark.site_name}}</a></td>
                <td><a href="{{bookmark.url}}"target = "_blank">{{bookmark.url}}</a></td>
                <td><a href="#" class = "btn btn-sucess btn-sm">Modify</a></td>
                <td><a href="#" class = "btn btn-danger btn-sm">Delete</a></td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</body>
```

#### 북마크 확인 기능 구현

- 추가 기능을 구현했으니 북마크의 확인 기능 구현.
- 상세 페이지. 클래스형 뷰를 사용해 간단히 만들기.


```python
# bookmark/views.py
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic.list import ListView
from .models import Bookmark
# Create your views here.

from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy

class BookmarkListView(ListView):
    model = Bookmark


class BookmakrCreateView(CreateView):
    model=Bookmark
    fields = ['site_name','url']
    success_url = reverse_lazy('list')
    template_name_suffix = '_create'


class BookmarkDetailView(DetailView):
    model = Bookmark

```


```python
# bookmark/urls.py
from django.conf.urls import url
from django.urls import path,include

from .views import BookmarkListView,BookmakrCreateView,BookmarkDetailView

urlpatterns = [
    path('',BookmarkListView.as_view(),name = 'list'),
    path('add/',BookmakrCreateView.as_view(),name = 'add'),
    path('detail/<int:pk>/',BookmarkDetailView.as_view(),name = 'detail'),
]
```

- urls.py에 path를 추가하고 BookmarkDetailView를 연결.
- URL 패턴은 다른 뷰들과 차이를 보임.
##### - <int:pk> : 앞에는 int 타입을 나타냄(컨버터). 뒤쪽은 컨버터를 통해 반환받은 값 혹은 패턴에 일치하는 값의 변수명. 컨버터는 생략하거나 커스텀 컨버터를 만들어 넣을 수 있음.

- str : 비어있지 않은 모든 문자와 매칭. 단 '/'는 제외. 컨버터를 설정하지 않을 경우 기본 컨버터
- int : 0을 포함한 양의 정수
- slug : 아스키 문자나 숫자, 하이픈, 언더스코어를 포함한 슬러그 문자열과 매칭
- uuid : UUID와 매칭. 같은 페이지에 여러 URL이 연결되는 것을 막으려 사용.
- path : 기존적으로 str와 같은 기능이나 '/'도 포함. URL의 부분이 아닌 전체에 대한 매칭을 하고 싶을 때 사용.


- bookmark/templates/bookmark/bookmark_detail.html
```html
<body>
{{object.site_name}}<br/>
{{object.url}}
</body>
```

- 확인 페이지는 북마크 하나의 정보만 출력.
- 제네릭 뷰인 DetailView가 object라는 이름으로 북마크의 값을 전달.
- object 변수를 이용해 값을 하나씩 출력.


- bookmark/templates/bookmark/bookmark_list.html
```html
<body>
    <div class = "btn-group">
        <a href="{% url 'add' %}" class = "btn btn-info">Add Bookmark</a>
    </div>
    <p></p>
    <table class="table">
        <thead>
            <tr>
                <th scope="col">#</th>
                <th scope="col">Site</th>
                <th scope="col">URL</th>
                <th scope="col">Modify</th>
                <th scope="col">Delete</th>
            </tr>
        </thead>
        <tbody>
            {% for bookmark in object_list %}
            <tr>
                <td>{{forloop.counter}}</td>
                <td><a href = "{% url 'detail' pk=bookmark.id %}">{{bookmark.site_name}}</a></td>
                <td><a href="{{bookmark.url}}"target = "_blank">{{bookmark.url}}</a></td>
                <td><a href="#" class = "btn btn-sucess btn-sm">Modify</a></td>
                <td><a href="#" class = "btn btn-danger btn-sm">Delete</a></td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</body>
```
- 확인 뷰를 만들었으니 목록 화면에서 확인 뷰로 가는 링크를 연결.
- href 속성 값을 URL 템플릿 태그를 사용하도록 변경.
- 템플릿 태그에 pk 값을 같이 전달해 제대로된 URL이 만들어져 출력할 수 있도록함.

# Q. id는 자동으로 생성되는 속성인가 ?

# Q. 아마 pk는 내부적으로 고정된 이름인 것 같다.

#### 북마크 수정 기능 구현
- 추가 기능과 거의 동일
- 제네릭 뷰를 사용해서 수정 뷰를 추가.


- bookmark/views.py
```python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic.list import ListView
from .models import Bookmark
# Create your views here.

from django.views.generic.edit import CreateView,UpdateView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy

class BookmarkListView(ListView):
    model = Bookmark


class BookmakrCreateView(CreateView):
    model=Bookmark
    fields = ['site_name','url']
    success_url = reverse_lazy('list')
    template_name_suffix = '_create'


class BookmarkDetailView(DetailView):
    model = Bookmark

class BookmakrUpdateView(UpdateView):
    model=Bookmark
    fields = ['site_name','url']
    template_name_suffix = '_update'

```
- UpdateView를 상속받도록 
- 모델을 설정하고 입력받을 필드 목록 설정.
- 템플릿 접미사 '_update'-> bookmakr_update.html이 템플릿이 됨.

- url 설정.
```python
# bookmark/urls.py 
from django.conf.urls import url
from django.urls import path,include

from .views import BookmarkListView,BookmakrCreateView,BookmarkDetailView,BookmakrUpdateView

urlpatterns = [
    path('',BookmarkListView.as_view(),name = 'list'),
    path('add/',BookmakrCreateView.as_view(),name = 'add'),
    path('detail/<int:pk>/',BookmarkDetailView.as_view(),name = 'detail'),
    path('update/<int:pk>/',BookmakrUpdateView.as_view(),name = 'update'),
]
```
- bookmark/templates/bookmark/bookmark_update.html
```html
<form action="" method="post">
    {% csrf_token %}
    {{form.as_p}}
    <input type="submit" value="Update" class="btn btn-info btn-sm">
</form>
```

- bookmark_list도 수정.

```html
<body>
    <div class = "btn-group">
        <a href="{% url 'add' %}" class = "btn btn-info">Add Bookmark</a>
    </div>
    <p></p>
    <table class="table">
        <thead>
            <tr>
                <th scope="col">#</th>
                <th scope="col">Site</th>
                <th scope="col">URL</th>
                <th scope="col">Modify</th>
                <th scope="col">Delete</th>
            </tr>
        </thead>
        <tbody>
            {% for bookmark in object_list %}
            <tr>
                <td>{{forloop.counter}}</td>
                <td><a href = "{% url 'detail' pk=bookmark.id %}">{{bookmark.site_name}}</a></td>
                <td><a href="{{bookmark.url}}"target = "_blank">{{bookmark.url}}</a></td>
                <td><a href="{%url 'update' pk=bookmark.id %}" class = "btn btn-success btn-sm">Modify</a></td>
                <td><a href="#" class = "btn btn-danger btn-sm">Delete</a></td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</body>
```


![image](https://user-images.githubusercontent.com/49121293/159564527-47e5568e-3a09-4c23-9098-b2d2c0cc5c95.png)


- modify 적용해보면 이런 오류 남
- 데이터베이스에 값은 잘 저장되었지만 수정을 마쳤는데 이동할 페이지가 없다는 뜻.


##### 수정이 완료된 후 이동할 페이지는 뷰에 success_url이 설정되어 있거나 모델에 get_absolute_url이라는 메서드를 통해서 결정함.

##### get_absolute_url을 만들어서 적용해보기.

```python
# bookmark/models.py
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.urls import reverse
# Create your models here.

class Bookmark(models.Model):
    site_name = models.CharField(max_length = 100)
    url = models.URLField('Site URL')
    def __str__(self):
        return "이름 : "+self.site_name + ", 주소 :" + self.url
    def get_absolute_url(self):
        return reverse('detail',args = [str(self.id)])

```

- get_absolute_url 메서드는 장고에서 사용하는 메서드. 보통은 객체의 상세 호마ㅕㄴ 주소를 반환하게 만듦.
- 이대 사용하는 reverse 메서드는 URL 패턴의 이름과 추가 인자를 전달받아 URL을 생성하는 메서드.


#### 북마크 삭제 기능 구현

```python
# bookmark/views.py
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from audioop import reverse

from django.shortcuts import render
from django.views.generic.list import ListView
from .models import Bookmark
# Create your views here.

from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy

class BookmarkListView(ListView):
    model = Bookmark


class BookmakrCreateView(CreateView):
    model=Bookmark
    fields = ['site_name','url']
    success_url = reverse_lazy('list')
    template_name_suffix = '_create'


class BookmarkDetailView(DetailView):
    model = Bookmark

class BookmarkUpdateView(UpdateView):
    model=Bookmark
    fields = ['site_name','url']
    
    template_name_suffix = '_update'


class BookmarkDeleteView(DeleteView):
    model = Bookmark
    sucess_url = reverse_lazy('list')
```


```
# bookmark/urls.py
from django.conf.urls import url
from django.urls import path,include

from .views import BookmarkListView,BookmakrCreateView,BookmarkDetailView,BookmarkUpdateView,BookmarkDeleteView

urlpatterns = [
    path('',BookmarkListView.as_view(),name = 'list'),
    path('add/',BookmakrCreateView.as_view(),name = 'add'),
    path('detail/<int:pk>/',BookmarkDetailView.as_view(),name = 'detail'),
    path('update/<int:pk>/',BookmarkUpdateView.as_view(),name = 'update'),
    path('delete/<int:pk>/',BookmarkDeleteView.as_view(),name = 'delete'),
]
```

- 바로 템플릿을 만드는 것이 아니라 bookmakr_list.html에 Delete 버튼을 먼저 연결한 후에 템플릿을 만들도록 함.
- href 속성에 URL 템플릿 태그를 사용해 delete 페이지의 URL을 출력함.

- <td><a href="{% url 'delete' pk=bookmark.id %}" class = "btn btn-danger btn-sm">Delete</a></td> 이렇게 수정.

![image](https://user-images.githubusercontent.com/49121293/159569154-adec0e3c-f9c5-4c42-a8dd-431eda256909.png)



- 이대로 동작 시키면 템플릿이 없다는 에러를 일으킴.

![image](https://user-images.githubusercontent.com/49121293/159569263-f0a769bd-12d5-4ca6-b32b-76b78d53832f.png)


- 템플릿 이름이 특이함. 기존에 사용하던 모델명_xxx 형태이긴 하지만 뷰 이름만 써있는 것이 아님.

- bookmakr/templates/bookmark/bookmark_confirm_delete.html

```html
<form action = "" method = "post">
    {% csrf_token %}
    <div class="alert alert-danger">Do you want to delete Bookmark "{{object}}"</div>
    <input type="submit" value ='Delete' class = 'btn btn-danger'>
</form>
```

- form 태그 안에는 무조건 csrf_token 함께 두기.
- 삭제할 것인지 확인 메시지를 출력하고 확인 버튼을 함께 만들어두었음.


![image](https://user-images.githubusercontent.com/49121293/159570419-52e12487-6d17-48c4-9395-a1124a428105.png)


- 이런식으로 삭제 표시가 뜨고
- ![image](https://user-images.githubusercontent.com/49121293/159570483-baad521e-6cfd-4a93-9490-219ac5ff95be.png)

- 삭제 후에 list로 리다이렉트

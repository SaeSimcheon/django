### 장고 프로젝트 만들기

#### 현재 폴더를 기준으로 프로젝트 생성
```console
django-admin startproject config .
```
#### 결과

![image](https://user-images.githubusercontent.com/49121293/159173295-ac0bc88f-a153-457e-853e-e73bd36434bf.png)

#### 웹서버 실행

```console
$ python3 manage.py runserver 127.0.0.1:7000
```

#### 결과

![image](https://user-images.githubusercontent.com/49121293/159173430-528468a0-dc9f-4df3-805a-2eb56a6c97a7.png)

- default port는 8000인데, 다른 포트를 사용하고 싶은 경우 '127.0.0.1:7000' 이런 식으로 위처럼 직접 포트를 지정해줄 수 있다.


#### 앱 만들기

```console
python3 manage.py startapp polls
```

![image](https://user-images.githubusercontent.com/49121293/159173844-58604326-e8c7-45b2-a254-37a50faab8c1.png)


#### 첫 번째 뷰 만들기
- 맨 처음에 아래 코드에는 'from django.shortcuts import render'를 제외하면 아무 것도 없었음.
```python
# polls/views.py
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return HttpResponse("Hello, world. polls index")

```

- 위와 같이 채워줌

#### 뷰를 만들면 호출하기 위한 URL이 있어야함. URL 연결을 위해서는 polls 폴더에 urls.py 만들어야함.

- polls에 빈 코드 'urls.py'를 만든 후에 아래와 같이 작성한다.

```python
# polls/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index,name = 'index')
]
```
##### path 함수 
- path(route,view,kwargs,name) 총 4개 인수를 받는 함수.
  - route : 주소
  - view : route에서 지정된 주소로 접근했을때 호출할 뷰
  - kwargs : 뷰에 전달할 값들.
  - name : route의 이름. 이 이름을 통해 원하는 곳에서 주소를 호출해 출력하거나 사용할 수 있음. (무슨 말 ?) polls 폴더에 있는 urls.py는 앱의 라우팅만 담당. 

따라서 프로젝트의 메인 urls.py 파일에서 연결을 해주어야 정상적으로 작동함. config/urls.py

```python
# config/urls.py
from django.conf.urls import url
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    #url(r'^admin/', admin.site.urls),
    path('polls/',include('polls.urls')),
    path('admin/',admin.site.urls)
]
```
- include는 다른 urls.py 파일을 참조할 수 있도록 함.
- 127.0.0.1:8000/polls/list/ 라는 주소로 접속하면 polls/까지는 일치하므로 잘라내고 나머지 list/ 부분만 polls/urls.py에서 찾는다.

```console
python3 manage.py runserver
```
# 결과
- 127.0.0.1/polls/로 접속하면 아래와 같은 화면을 확인할 수 있음.

![image](https://user-images.githubusercontent.com/49121293/159174653-46575f4b-3967-483f-afbe-54c32ee8c03f.png)


- path('',include('polls.urls')), 이렇게 설정하면 들어간 페이지에서 바로 polls.urls을 참조함.


#### 데이터베이스 만들기

```console
python manage.py migrate
```


#### 결과

![image](https://user-images.githubusercontent.com/49121293/159175330-263e00c0-f067-4eb8-847a-111fe72f75cf.png)


#### 모델 만들기

- 장고에서 모델은 데이터베이스의 구조도.
- 어떤 테이블을 만들고 어떤 컬럼을 갖게 할 것인지 결정.
- 해당 컬럼의 제약조건까지 모델에서 결정.
- model.py에서 작성하고 클래스의 형태.


```python
# polls/models.py

from django.db import models

# Create your models here.

```

- 이렇게 비어있는 코드에 아래와 같이 추가.

```python
# polls/models.py
from django.db import models

# Create your models here.

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

class Choice(models.Model):
    question = models.ForeignKey(Question,on_delete = models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
```

- 장고의 모델은 models.Model을 상속받아서 만듦.
- DB 각 제품마다 TABLE 등을 작성하는 방식을 django 안의 api를 통해서 만드는 것 같다.
- ForeignKey -> Question을 갖는다는 것은 Choice model이 Question에 소속된다는 것을 의미한다.



모델 완성. 데이터베이스에 적용해야함. 이때 사용하는 명령은 migrate 명령들인데, 이 명령을 사용하려면 polls 앱이 현재 프로젝트에
설치 되어 있다고 알야줘야함.

- config/settings.py 파일을 열고 'INSTALLED_APPS' 변수 제일 윗줄에 polls 앱을 추가함.

```python
'''
생략
'''
INSTALLED_APPS = [
    'polls.apps.PollsConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
'''
생략
'''
```
- 'polls.apps.PollsConfig'는 polls 앱 폴더에 apps.py 파일에 있는 PollsConfig 클래스를 의미함.
- polls만 써도 된다고 함.

```console
python3 manage.py makemigrations polls
```
![image](https://user-images.githubusercontent.com/49121293/159176055-d6918956-52ba-4f09-974b-1c85bbba4628.png)


- 데이터 베이스에 적용.
- 앱의 변경 사항을 추적해 데이터베이스에 적용할 내용을 만들어냄.
- polls/migrations/0001_initial.py에 결과가 기록.


```console
python3 manage.py sqlmigrate polls 0001
```
```
BEGIN;
--
-- Create model Question
--
CREATE TABLE "polls_question" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "question_text" varchar(200) NOT NULL, "pub_date" datetime NOT NULL);
--
-- Create model Choice
--
CREATE TABLE "polls_choice" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "choice_text" varchar(200) NOT NULL, "votes" integer NOT NULL, "question_id" bigint NOT NULL REFERENCES "polls_question" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE INDEX "polls_choice_question_id_c5b4b260" ON "polls_choice" ("question_id");
COMMIT;
```

- SQL 구문 여러줄이 나와 ORM을 통해 쉽게 DB를 구축할 수 있음.
- 아직 DB에 반영된 상태가 아님.
- 변경 사항을 데이터베이스에 반영하기 위한 명령은 아래와 같음.

```console
python3 manage.py migrate polls 0001
```

#### 모델에 함수 추가하기

- Question model과 Choice model에 __str__ 메서드 추가하기.
- 해당 메서드는 관리자 화면이나 쉘에서 객체를 출력할 때 나타날 내용 결정.
- was_published_recently라는 메서드 하나 더 추가.



```python
#polls/models.py

from django.db import models
import datetime

from django.utils import timezone

# Create your models here.

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    
    def __str__(self):
        return self.question_text
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
class Choice(models.Model):
    question = models.ForeignKey(Question,on_delete = models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text
```

#### 관리자 페이지 확인

- 관리자 계정 만들기

```console
python3 manage.py createsuperuser
```

- 서버 실행하기

```console
python3 manage.py runserver
```
- 127.0.0.1:8000/admin/으로 들어가서 로그인하면 아래와 같음.

![image](https://user-images.githubusercontent.com/49121293/159177214-9f123710-5b8c-4cac-87f8-f810ccf96c35.png)

- 계정과 그룹만 관리할 수 있음.


- 관리자 페이지에서 Question model을 관리하려면 등록을 해야함. admin.py 파일에 입력.

```python
# polls/admin.py

from django.contrib import admin

# Register your models here.

```
- 위 코드에서 아래로

```python
# polls/admin.py

from django.contrib import admin



```


![image](https://user-images.githubusercontent.com/49121293/159177645-79523235-a1e5-4fb6-a895-b7375e6dd8a5.png)


- 등록하면 바로 확인할 수 있음.

- Questions를 들어가서 투표 목록으로 들어가자.


![image](https://user-images.githubusercontent.com/49121293/159177701-b4b282be-c986-4793-8cd8-58d5c6a05e55.png)

- 아직 투표 등록을 하지 않았기 때문에 아무 것도 없음.


![image](https://user-images.githubusercontent.com/49121293/159177868-b7fe2540-d0b8-4867-b4dc-445f2dc101bb.png)


- ADD QUESTION 버튼을 클릭해서 등록 화면으로 이동하여 투표 제목 등록.


#### 여러 가지 뷰 추가하기

1. 투표 목록 : 등록된 투표의 목룍을 표시하고 상세 페이지로 이동하는 링크 제공
2. 투표 상세 : 투표의 상세 항목을 보여줌.
3. 투표 기능 : 선택한 답변을 반영.
4. 투표 결과 : 선택한 답변을 반영 한 후 결과를 보여줌.

```python
# polls/views.py
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return HttpResponse("Hello, world. polls index")

```

- 위 코드에서 아래와 같이 추가.


```python
# polls/views.py
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return HttpResponse("Hello, world. polls index")

def detail(request,question_id):
    return HttpResponse(f"You're loocking at question {question_id}")

def results(request,question_id):
    response = f"You're loocking at the results of question {question_id}"
    return HttpResponse(response)

def vote(request,question_id):
    return HttpResponse(f"You're voting on question {question_id}")
```


- 추가한 3개의 view를 위한 URL 연결.


```python 
#polls/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index,name = 'index')
]
```
- 위 코드를 아래와 같이 작성.


```python
#polls/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index,name = 'index'),
    path('<int:question_id>/', views.detail,name = 'detail'),
    path('<int:question_id>/results/', views.results,name = 'results'),
    path('<int:question_id>/vote/', views.vote,name = 'vote'),
]


- index 뷰와 다르게 특이한 모양을 보여줌. 각 URL에 있는 <>는 변수를 의미. 이 부분에 해당하는 값을 뷰에 인자로 전달.


- 실제 동작되는 뷰를 만들기 위하여 index view를 수정.

```python
#polls/views.py

from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    
    return HttpResponse("Hello, world. polls index")

def detail(request,question_id):
    return HttpResponse(f"You're loocking at question {question_id}")

def results(request,question_id):
    response = f"You're loocking at the results of question {question_id}"
    return HttpResponse(response)

def vote(request,question_id):
    return HttpResponse(f"You're voting on question {question_id}")

```

- 위 코드를 아래와 같이 수정.


```python
#polls/views.py
from django.shortcuts import render
from django.http import HttpResponse
from .models import Question
# Create your views here.

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    output = ', '.join([q.question_text for q in latest_question_list])
    return HttpResponse(output)

def detail(request,question_id):
    return HttpResponse(f"You're loocking at question {question_id}")

def results(request,question_id):
    response = f"You're loocking at the results of question {question_id}"
    return HttpResponse(response)

def vote(request,question_id):
    return HttpResponse(f"You're voting on question {question_id}")
```


- 수정된 부분을 살펴보면 Question의 objects라는 attribute를 아마 order_by를 pub_date를 기준으로 하여 5개만 추출하는 것 같음.
- 이를 list comprehension을 통하여 list로 만든 후 ', '으로 문자열을 합침. 
- question_text는 아까 __str__ method를 통하여 지정했었음.
```python
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    output = ', '.join([q.question_text for q in latest_question_list])
    return HttpResponse(output)

```


- 이런 식으로 수정하여 나타내면 됨.
![image](https://user-images.githubusercontent.com/49121293/159179245-fa120715-0f55-4ec0-8d73-582a5e68c528.png)
![image](https://user-images.githubusercontent.com/49121293/159179236-d8d98640-65c4-430d-b13e-c0071cdd5f11.png)



##### 기능이 있는 뷰는 만들었지만, MTV 패턴에는 맞지 않다. 템플릿을 만들어 파이썬 코드와 HTML 코드를 분리.

- 현재 polls 앱 디렉터리 안에 templates/polls 생성하기.

```console
mkdir templates
cd templates/
mkdir polls
```

- polls/templates/polls/index.html에 아래와 같이 작성하기
- 아래는 공부할 것.
- 일단 생각으로는 html 문서를 시작하는 방식으로 첫줄
- 언어설정
- head는 가장 위에 붙는 타이틀인 것 같고 문자열 셋은 utf-8 title을 지정
- body는 본문 latest_question_list에 따라서 if else로 나뉘는 듯.
- if 아래에는 반복문이 있고, /polls/.... 뒤에 오는 것을 question.id로 반는다 ? 
- a 태그는 무엇이고 href는 무엇일까 ? 우리가 model로 지정한 question은 어떻게 연관될 수 있을까 ?
- 
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>>
</head>>
<body>
{% if latest_question_list %}
    <ul>
        {% for question in latest_question_list % }
            <li><a href="/polls/{{question.id}}">{{question.question_text}} </a>>
        {% endfor %}
    </ul>>
{% else %}
    <p>No polls are available. </p>
{% endif %}
</body>>
</html>>
```




- 만든 템플릿을 이용하도록 뷰를 변경. 템플릿을 불러오기 위해 loader를 임포트.

```python
#polls/views.py
from django.shortcuts import render
from django.http import HttpResponse
from .models import Question
# Create your views here.

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    output = ', '.join([q.question_text for q in latest_question_list])
    return HttpResponse(output)

def detail(request,question_id):
    return HttpResponse(f"You're loocking at question {question_id}")

def results(request,question_id):
    response = f"You're loocking at the results of question {question_id}"
    return HttpResponse(response)

def vote(request,question_id):
    return HttpResponse(f"You're voting on question {question_id}")
```

- 위 코드를 아래와 같이 변경

```python
#polls/views.py
from django.shortcuts import render
from django.http import HttpResponse
from .models import Question
# Create your views here.

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    
    output = ', '.join([q.question_text for q in latest_question_list])
    return HttpResponse(output)

def detail(request,question_id):
    return HttpResponse(f"You're loocking at question {question_id}")

def results(request,question_id):
    response = f"You're loocking at the results of question {question_id}"
    return HttpResponse(response)

def vote(request,question_id):
    return HttpResponse(f"You're voting on question {question_id}")
```






- loader를 사용해서 index.html을 불러오고 미리 만들어둔 투표 목록을 context라는 변수를 이용해 전달하는 방식이 불편하다고 함. 장고에는 이를 간소화해줄 수 있는 render라는 단축이 존재.


```python
#polls/views.py
from django.shortcuts import render
from django.http import HttpResponse
from .models import Question
from django.template import loader
# Create your views here.

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list' : latest_question_list
    }
    return HttpResponse(template.render(context,request))

def detail(request,question_id):
    return HttpResponse(f"You're loocking at question {question_id}")

def results(request,question_id):
    response = f"You're loocking at the results of question {question_id}"
    return HttpResponse(response)

def vote(request,question_id):
    return HttpResponse(f"You're voting on question {question_id}")
```
- 위 코드를 아래와 같이 변경
- render 메서드는 request와 템플릿 이름 그리고 사전형 객체를 인자로 받음.


```python
#polls/views.py
from django.shortcuts import render
from django.http import HttpResponse
from .models import Question
from django.template import loader
# Create your views here.

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {
        'latest_question_list' : latest_question_list
    }
    return render(request,'polls/index.html',context)

def detail(request,question_id):
    return HttpResponse(f"You're loocking at question {question_id}")

def results(request,question_id):
    response = f"You're loocking at the results of question {question_id}"
    return HttpResponse(response)

def vote(request,question_id):
    return HttpResponse(f"You're voting on question {question_id}")
```


#### 404 오류 일으키기
- 파일이 존재하지 않을때 발생하는 오류 -> 게시판 등 정보를 불러 오는 페이지의 경우 해당 데이터가 존재하지 않는다.


- detail 뷰를 수정하기.


```python
from django.shortcuts import render
from django.http import HttpResponse
from .models import Question
from django.template import loader
# Create your views here.

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {
        'latest_question_list' : latest_question_list
    }
    return render(request,'polls/index.html',context)

def detail(request,question_id):
    return HttpResponse(f"You're loocking at question {question_id}")

def results(request,question_id):
    response = f"You're loocking at the results of question {question_id}"
    return HttpResponse(response)

def vote(request,question_id):
    return HttpResponse(f"You're voting on question {question_id}")
```

- 위 코드를 아래와 같이 수정


```
from django.shortcuts import get_object_or_404, render
from django.http import Http404, HttpResponse
from .models import Question
from django.template import loader
# Create your views here.

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {
        'latest_question_list' : latest_question_list
    }
    return render(request,'polls/index.html',context)

def detail(request,question_id):
    try :
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise get_object_or_404(Question,pk = question_id)
    return render(request,'polls/detail.html',{'question':question})

def results(request,question_id):
    response = f"You're loocking at the results of question {question_id}"
    return HttpResponse(response)

def vote(request,question_id):
    return HttpResponse(f"You're voting on question {question_id}")
```

- detail.html 파일을 만들고 body를 수정.

- http404를 처리할 때 loader-render 관계처럼 단축 함수가 존재. -> get_object_or_404

- context는 dict로 주어야한다.


![image](https://user-images.githubusercontent.com/49121293/159272300-e0cf4919-9d78-45e1-8e05-da06183295ff.png)

![image](https://user-images.githubusercontent.com/49121293/159273594-8802f908-aacb-4682-9ab6-98d2e3833951.png)


- 없는 question_id에 대해서는 404오류 일어남.

#### 하드 코딩된 URL 없애기

- index.html 파일을 살펴보면 상세페이지로 이동하기 위한 링크의 주소가 하드 코딩 되어 있음.

- #polls/templates/polls/index.html
```html


<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
{% if latest_question_list %}
    <ul>
    {% for question in latest_question_list %}
        <li><a href="/polls/{{question.id}}/">{{question.question_text}} </a></li>
    {% endfor %}
    </ul>
{% else %}
    <p>No polls are available. </p>
{% endif %}
</body>
</html>
```

- href 속성의 값을 직접 써주는 경우 나중에 주소를 polls가 아닌 다른 형태로 바꾸려하면 html을 직접 다 열어서 수정해야한다는 불편함이 있음.그래서 템플릿 태그를 사용해서 하드 코딩된 URL을 없애기

- polls/templates/polls/index.html
```html

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
{% if latest_question_list %}
    <ul>
    {% for question in latest_question_list %}
        <li><a href="{% url 'detail' question.id %}">{{question.question_text}} </a></li>
    {% endfor %}
    </ul>
{% else %}
    <p>No polls are available. </p>
{% endif %}
</body>
</html>
```
- URL 템플릿 태그를 사용해 주소를 만들어 출력하는 방식. URL 템플릿 태그는 URL의 이름을 필수 인자 전달.
- detail이라는 이름을 가진 URL 형식을 찾아서 URL을 만들어 출력. -> 해당 이름을 가진 URL은 urls.py 전체를 검색해서 찾음. (궁금한 점 : urls가 polls를 기준해서만 찾는건지 아니면 전체를 전부 찾는건지 아마 polls만 기준이 아닐까 ?)
- 아래에서 detail을 찾으면 '<int:question_id>/'이고 이를 기준으로 question_id를 적용하여 링크 설정.
'''
urlpatterns = [
    path('', views.index,name = 'index'),
    path('<int:question_id>/', views.detail,name = 'detail'),
    path('<int:question_id>/results/', views.results,name = 'results'),
    path('<int:question_id>/vote/', views.vote,name = 'vote'),
]
'''

- <li><a href="{% url 'detail' question.id %}">{{question.question_text}} </a></li> 이렇게 수정.

#### URL 네임스페이스 설정.
- 분리된 경로 만들기. 예를들면 detail이라는 주소 이름을 가진 뷰가 polls 및 다른 앱에 있는 경우. 장고는 어느 뷰의 URL을 만들지 알 수가 없음. 이런 경우 네임스페이스를 설정해 각각의 뷰가 어느 앱에 속하는 것인지 구분.


```python
# polls/urls.py

from django.urls import path
from . import views

# 여기 추가
app_name = "polls"

urlpatterns = [
    path('', views.index,name = 'index'),
    path('<int:question_id>/', views.detail,name = 'detail'),
    path('<int:question_id>/results/', views.results,name = 'results'),
    path('<int:question_id>/vote/', views.vote,name = 'vote'),
]

```
- 위와 같이 app_name이라는 변수를 추가하면 설정 끝. 템플릿에도 수정하여 사용하면 됨.

#### 투표 기능 추가하기

- detail.html 수정 및 vote view에도 기능을 추가.

- polls/templates/polls

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    <h1>{{question.question_text}}</h1>
    <ul>
    {% for choice in question.choice_set.all%}
    <li>{{choice.choice_text}}</li>
    {% endfor %}
    </ul>
</body>
</html>
```

- polls/templates/polls/detail.html을 아래와 같이 수정.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    <h1>{{question.question_text}}</h1>
    {% if error_message %}<p><strong>{{error_message}}</strong></p>{%endif%}

    <form action ="{% url 'polls:vote' question.id %}" method="post">
    {% csrf_token %}
    {% for choice in question.choice_set.all %}
        <input type = "radio" name = "choice" id ="choice{{forloop.couter}}" value ="{{choice.id}}">
        <label for="choice{{forloop.counter}}">{{choice.choice_text}}</label><br>
        {% endfor %}
        <input type = "submit" value="Vote">
    </form>>
</body>
</html>
```

- 수정사항
    - form 태그를 사용해서 사용자가 답변 항목을 선택하고 전달할 수 있도록
    - 사용자가 선택한 항목의 번호를 vote 뷰를 전달하도록 action 속성에 vote URL이 출력되게 URL 템플릿 태그 사용.
    - method 속성에 써 있는 post는 http 메서드 중 하나. 서버로 정보를 전달할 때 사용하는 일반적인 방법.
    - forloop.counter는 템플릿 문법에서 제공하는 기능 중 하나로 반복문의 횟수 출력.
    - 선택한 답변의 번호를 vote 뷰에 choice=번호 형대로 전달.
    - csrf_token은 CSRF 공격을 막기 위한 수단 중 하나. -> 방금 서버로 들어온 요청이 사이트 내부에서 온 것이 맞는지 확인하는 용도
    
    
- detail.html에서 만들어진 정보를 받을 vote 뷰를 수정

#### 현재 결과
![image](https://user-images.githubusercontent.com/49121293/159296036-6528c2ea-71bf-443d-b550-f8151753e116.png)


# choice_set은 model 안에 없었는데 어디서 나오는 걸까 ? 상속받은 속성이 아닐까 ?
# HttpResponseRedirect는 HttpResponse와 어떻게 다를까 ?
# reverse는 무엇인가 ?
# 분명 question
# selected_choice는 question의 인스턴스가 아닌가 본데 ?
# 애초에 model 자체는 인스턴스화된 상태로 관리되는 것이 아니네.


- views의 vote 함수 수정
- 아래에서 보면 selected_choice에 question.choice_set이 pk가 request.POST["choice"]로 전달 받는 것이 확인 됨.
'''
def vote(request,question_id):
    question = get_object_or_404(Question,pk=question_id)
    try :
        selected_choice = question.choice_set.get(pk = request.POST["choice"])
    except (KeyError,Choice.DoesNotExist):
        return render(request,'polls/detail.html',{
            'question' :question,
            'error_message' : "You didn't select a choice."
        })
    else:
        selected_choice.votes +=1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results',args = (question,id,)))

'''

```python
# polls/urls.py
from django.shortcuts import get_object_or_404, render
from django.http import Http404, HttpResponse,HttpResponseRedirect
from .models import Question , Choice
from django.template import loader
from django.urls import reverse
# Create your views here.

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {
        'latest_question_list' : latest_question_list
    }
    return render(request,'polls/index.html',context)

def detail(request,question_id):
    try :
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise get_object_or_404(Question,pk = question_id)
    return render(request,'polls/detail.html',{'question':question})

def results(request,question_id):
    response = f"You're loocking at the results of question {question_id}"
    return HttpResponse(response)

def vote(request,question_id):
    question = get_object_or_404(Question,pk=question_id)
    try :
        selected_choice = question.choice_set.get(pk = request.POST["choice"])
    except (KeyError,Choice.DoesNotExist):
        return render(request,'polls/detail.html',{
            'question' :question,
            'error_message' : "You didn't select a choice."
        })
    else:
        selected_choice.votes +=1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results',args = (question,id,)))
```

수정사항
- request.POST[변수이름]을 통해 전달받은 변수들의 값들을 확인 할 수 있음. 항상 문자열이기 대문에 문자열이라는 사실을 기억하고 다뤄야함.
- 전달받은 답변이 해당 투표 항목에 있는지 확인하고 없다면 다시 상세 페이지로 이동. 답변을 선택하지 않았다는 오류 메시지도 같이 전달.
- 제대로 된 답변을 선택한 것이라면 해당 답변의 수룰 1 증가시키고 결과 화면으로 이동.


- 결과를 출력하는 result 뷰도 변경.

```python
# polls/urls.py
from django.shortcuts import get_object_or_404, render
from django.http import Http404, HttpResponse,HttpResponseRedirect
from .models import Question , Choice
from django.template import loader
from django.urls import reverse
# Create your views here.

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {
        'latest_question_list' : latest_question_list
    }
    return render(request,'polls/index.html',context)

def detail(request,question_id):
    try :
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise get_object_or_404(Question,pk = question_id)
    return render(request,'polls/detail.html',{'question':question})

def results(request,question_id):
    response = f"You're loocking at the results of question {question_id}"
    return HttpResponse(response)

def vote(request,question_id):
    question = get_object_or_404(Question,pk=question_id)
    try :
        selected_choice = question.choice_set.get(pk = request.POST["choice"])
    except (KeyError,Choice.DoesNotExist):
        return render(request,'polls/detail.html',{
            'question' :question,
            'error_message' : "You didn't select a choice."
        })
    else:
        selected_choice.votes +=1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results',args = (question,id,)))


```
- 위 코드에서 result부분 수정.


```python
# polls/urls.py
from django.shortcuts import get_object_or_404, render
from django.http import Http404, HttpResponse,HttpResponseRedirect
from .models import Question , Choice
from django.template import loader
from django.urls import reverse
# Create your views here.

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {
        'latest_question_list' : latest_question_list
    }
    return render(request,'polls/index.html',context)

def detail(request,question_id):
    try :
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise get_object_or_404(Question,pk = question_id)
    return render(request,'polls/detail.html',{'question':question})

def results(request,question_id):
    question = get_object_or_404(Question,pk = question_id)
    return render(request , 'polls/results.html',{"question":question})

def vote(request,question_id):
    question = get_object_or_404(Question,pk=question_id)
    try :
        selected_choice = question.choice_set.get(pk = request.POST["choice"])
    except (KeyError,Choice.DoesNotExist):
        return render(request,'polls/detail.html',{
            'question' :question,
            'error_message' : "You didn't select a choice."
        })
    else:
        selected_choice.votes +=1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results',args = (question,id,)))
```

- results.html도 만들어줌.

```html
<h1>{{question.question_text}} </h1>

<ul>
{% for choice in question.choice_set.all %}
    <li>{{ choice.choice_text}} -- {{choice.votes}} vote{{choice.votes|pluralize}}</li>
    {% endfor %}
</ul>

<a href = "{% url 'polls:detail' question.id %}"> Vote again ?</a>
```
- results.html 각 답변 항목과 투표 수를 한꺼번에 보여줌


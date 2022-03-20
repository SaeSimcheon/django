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

```
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


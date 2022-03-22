

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

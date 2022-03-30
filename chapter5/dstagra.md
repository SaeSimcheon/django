
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

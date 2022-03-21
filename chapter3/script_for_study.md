```python
# polls/views.py

from django.views import generic
from .models import Question, Choice
from django.shortcuts import get_object_or_404, render
from django.http import Http404, HttpResponse,HttpResponseRedirect
from django.urls import reverse

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'
    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]

class DetailView(generic.DeleteView):
    model = Question
    template_name = 'polls/detail.html'

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

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
        return HttpResponseRedirect(reverse('polls:results',args = (question.id,)))


'''
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

'''
```


```python
# polls/urls.py

from django.urls import path
from . import views

app_name = 'polls'


urlpatterns = [
    path('', views.IndexView.as_view(),name = 'index'),
    path('<int:pk>/', views.DetailView.as_view(),name = 'detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(),name = 'results'),
    path('<int:question_id>/vote/', views.vote,name = 'vote'),
]


'''
urlpatterns = [
    path('', views.index,name = 'index'),
    path('<int:question_id>/', views.detail,name = 'detail'),
    path('<int:question_id>/results/', views.results,name = 'results'),
    path('<int:question_id>/vote/', views.vote,name = 'vote'),
]

'''
```

- polls/static/polls/style.css
```css
body {
    background: white url("images/background.png") no-repeat;
    background-position: right bottom;
}

li a {
    color: green;
}
```


```python

# config/urls.py
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
    #url(r'^admin/', admin.site.urls),
    #path('',include('polls.urls')),
    path('polls/',include('polls.urls')),
    path('admin/',admin.site.urls)
]

```

```python
# polls/models.py
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
    
    was_published_recently.admin_order_filed = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'published recently ?'
    
class Choice(models.Model):
    question = models.ForeignKey(Question,on_delete = models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text



```

```python
# polls/admin.py
from django.contrib import admin

# Register your models here.

from .models import Question, Choice

#admin.site.register(Question)


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

'''
class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 3
'''
class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields':['question_text']}),
        ('Date information', {'fields':['pub_date']}),
    ]
    list_display= ('question_text','pub_date','was_published_recently')
    inlines = [ChoiceInline]

    list_filter = ['pub_date']
    search_fields = ['question_text']




admin.site.register(Question,QuestionAdmin)

```

- polls/templates/polls/results.html
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
    </form>
</body>
</html>
```

- polls/templates/polls/detail.html
```html
<h1>{{question.question_text}} </h1>

<ul>
{% for choice in question.choice_set.all %}
    <li>{{ choice.choice_text}} -- {{choice.votes}} vote{{choice.votes|pluralize}}</li>
    {% endfor %}
</ul>

<a href = "{% url 'polls:detail' question.id %}"> Vote again ?</a>
```

- polls/templates/polls/index.html
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    {% load static %}
    <link rel="stylesheet" type="text/css" href="{% static 'polls/style.css' %}">
</head>
<body>
{% if latest_question_list %}
    <ul>
    {% for question in latest_question_list %}
        <li><a href="{% url 'polls:detail' question.id %}">{{question.question_text}} </a></li>
    {% endfor %}
    </ul>
{% else %}
    <p>No polls are available. </p>
{% endif %}
</body>
</html>
```

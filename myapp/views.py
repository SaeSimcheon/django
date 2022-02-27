# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,HttpResponse

import random

# Create your views here.
topics=[{"id":1,"title":"routing","body":"Routing is .."},
{"id":2,"title":"view","body":"view is .."},
{"id":3,"title":"Model","body":"Model is .."}]

def HTMLTemplate(articleTag):
    global topics
    ol = ''
    for topic in topics :
        ol += f'<li><a href="/read/{topic["id"]}">{topic["title"]}</a></li>'
        # 이렇게 하면 링크가 생김.
        # a href = ''를 하면 해당 위치 url에서 ''가 가리키는 새로운 링크를 만들 수 있나보다.
    # 이 for 문에 의해서 만들어진 코드
    return f'''
    <html>
    <body>
        <h1>Django</h1>
        <ol>
            {ol}
        </ol>
        {articleTag}
    </body>
    </html>
    '''




def index(request): # 약속이 있음 첫번째 파라미터를 요청과 관련된 여러 정보에 관한 객체를 전달하도록 약속
    article = '''
        <h2>Welcom</h2>
        hello, Django
    '''
    return HttpResponse(HTMLTemplate(article)) # response로 http를 이용해서 응답을 하겠다는 의미로 이 객체를 쓰겠다.
    # 또 그 인자로 전송하고 싶은 값을 적어주면 됨.




def Create(request): # 약속이 있음 첫번째 파라미터를 요청과 관련된 여러 정보에 관한 객체를 전달하도록 약속
    return HttpResponse("Create") 



def read(request,id): # 약속이 있음 첫번째 파라미터를 요청과 관련된 여러 정보에 관한 객체를 전달하도록 약속
    global topics
    article = ''
    for topic in topics :
        if topic['id'] == int(id):
            article = f'<h2>{topic["title"]}</h2>{topic["body"]}'
    return HttpResponse(HTMLTemplate(article)) 
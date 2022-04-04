# 모두 shorcut function

# Reverse
- URL template tag와 비슷한 것을 사용하고 싶을때 사용한다 ?
- reverse(viewname,urlconf,args,kwargs)
- viewname은 URL pattern name 또는 callable view object
- 주어진 source에 대한 적절한 URL을 찾는 것이 목표 ?
- 하드 코드 하는 것보다 수월하게 미래에 수정가능.
- [stackoverflow](https://stackoverflow.com/questions/11241668/what-is-reverse)


# Redirect
- httpresponseredict를 적절한 url에 return한다.
- 지정된 URL로 이동.
- 성공적으로 post data를 다룬 후에는 redirect 해야한다 ?
```
As the Python comment above points out, you should always return an HttpResponseRedirect after successfully dealing with POST data. This tip isn’t specific to Django; it’s good web development practice in general.
```



# Render
- 주어진 템플릿과 context를 묶어 HttpResponse 객체를 return한다.


## Request and response objects

- 한 페이지가 요청되면, 장고는 요청에 대한 meta 데이터를 포함하는 httprequest object를 생성한다. 그 후 장고는 적절한 view를 불러와 첫번째 argument로 제공한다.
- 각 view는 httpresponse object를 반환해야한다.
- 랜더링된 텍스트를 반환하는 것이

## HttpResponse class
[좋은 참고 자료](https://inuplace.tistory.com/584?category=933545)
- HttpRequest object와 대조적으로(장고에 의해 자동으로 생성되는), HttpResponse objects는 사용자가 지정해야한다.
- 각 view와 연결.
- django web app에 대한 inbound Http request에 text response를 제공한다.

- HttpResponse는 request에 대해 response할 text를 포함하는 object

## Render와 HttpResponse

- Render는 템플릿 및 인자를 통합하여 HttpResponse objects를 생성하여 return하는 함수이다.


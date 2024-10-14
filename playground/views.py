from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
# Create your views here.

def say_hello(request: HttpRequest) -> HttpResponse:
    return render(request=request, template_name='hello.html', context={'title' : 'Hello, Django!'})
from django.http import HttpRequest, HttpResponse
from django.urls import path
from typing import List
from . import views

urlpatterns:List[path] = [
    path(route='hello/', view=views.say_hello, name='say_hello'),
]

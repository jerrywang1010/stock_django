from django.conf.urls import url, include
from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^$', views.on_click, name="on_click"),
]
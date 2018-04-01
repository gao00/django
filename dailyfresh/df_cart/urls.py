#-*-coding:utf-8-*-
from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^$',views.cart),
    url(r'^cart_(\d+)_(\d+)/$',views.add_cart),
    url(r'^edit(\d+)_(\d+)/$',views.edit),
    url(r'^delete(\d+)/$',views.delete),
]
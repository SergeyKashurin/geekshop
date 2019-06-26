from django.urls import path, re_path
import mainapp.views as mainapp
import basketapp.views as basket
from django.conf.urls import include

app_name = 'mainapp'

urlpatterns = [
    # path('', mainapp.product, name='index'),
    # path('category/<int:pk>/', mainapp.product, name='category'),
    # path('category/<int:pk>/page/<int:page>/', mainapp.product, name='page'),
    # path('product_details/<int:pk>/', mainapp.product_details, name='product_details'),
    re_path(r'^$', mainapp.index, name='index'),
    re_path(r'^products/$', mainapp.products, name='products'),

    re_path(r'^catalog/(?P<pk>\d+)/$', mainapp.catalog, name='catalog'),
    re_path(r'^catalog/(?P<pk>\d+)/(?P<page>\d+)/$', mainapp.catalog, name='catalog_paginator'),
    re_path(r'^product/(?P<pk>\d+)/$', mainapp.product, name='product'),

    re_path(r'^contact/$', mainapp.contact, name='contact'),
]

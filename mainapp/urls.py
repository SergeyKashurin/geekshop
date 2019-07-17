from django.urls import re_path
import mainapp.views as mainapp
from django.views.decorators.cache import cache_page

app_name = 'mainapp'

# urlpatterns = [
#     re_path(r'^$', mainapp.index, name='index'),
#     re_path(r'^products/$', mainapp.products, name='products'),
#
#     re_path(r'^catalog/(?P<pk>\d+)/$', mainapp.catalog, name='catalog'),
#     re_path(r'^catalog/(?P<pk>\d+)/(?P<page>\d+)/$', mainapp.catalog, name='catalog_paginator'),
#     re_path(r'^product/(?P<pk>\d+)/$', mainapp.product, name='product'),
#
#     re_path(r'^category/(?P<pk>\d+)/$', cache_page(3600)(mainapp.products)),
#
#     re_path(r'^contact/$', mainapp.contact, name='contact'),
# ]

urlpatterns = [
   re_path(r'^$', mainapp.index, name='index'),
   re_path(r'^category/(?P<pk>\d+)/$', mainapp.products, name='category'),
   re_path(r'^category/(?P<pk>\d+)/ajax/$', cache_page(3600)(mainapp.products_ajax)),
   re_path(r'^products/$', mainapp.products, name='products'),
   re_path(r'^product/(?P<pk>\d+)/$', mainapp.product, name='product'),

   re_path(r'^catalog/(?P<pk>\d+)/$', mainapp.catalog, name='catalog'),
   re_path(r'^catalog/(?P<pk>\d+)/(?P<page>\d+)/$', mainapp.catalog, name='catalog_paginator'),

   re_path(r'^category/(?P<pk>\d+)/page/(?P<page>\d+)/$', mainapp.products, name='page'),
   re_path(r'^category/(?P<pk>\d+)/page/(?P<page>\d+)/ajax/$', cache_page(3600)(mainapp.products_ajax)),
   re_path(r'^contact/$', mainapp.contact, name='contact'),
]

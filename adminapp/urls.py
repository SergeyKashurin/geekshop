import adminapp.views as adminapp
from django.urls import re_path, path

app_name = 'adminapp'

urlpatterns = [
    re_path(r'^$', adminapp.UsersListView.as_view(), name='index'),
    re_path(r'^user/create/$', adminapp.user_create, name='user_create'),
    re_path(r'^user/update/(?P<pk>\d+)/$', adminapp.user_update, name='user_update'),
    re_path(r'^user/delete/(?P<pk>\d+)/$', adminapp.user_delete, name='user_delete'),

    path('productcategories/', adminapp.categories, name='categories'),
    re_path(r'^productcategory/create/$', adminapp.product_create, name='productcategory_create'),
    re_path(r'^productcategory/update/(?P<pk>\d+)/$', adminapp.ProductCategoryUpdate.as_view(), name='productcategory_update'),
    re_path(r'^productcategory/delete/(?P<pk>\d+)/$', adminapp.ProductCategoryDelete.as_view(), name='productcategory_delete'),

    re_path(r'^products/category/(?P<category_pk>\d+)/$', adminapp.products, name='products'),
    re_path(r'^product/create/(?P<category_pk>\d+)/$', adminapp.product_create, name='product_create'),
    re_path(r'^product/read/(?P<pk>\d+)/$', adminapp.ProductDetail.as_view(), name='product_read'),
    re_path(r'^product/update/(?P<pk>\d+)/$', adminapp.product_update, name='product_update'),
    re_path(r'^product/delete/(?P<pk>\d+)/$', adminapp.product_delete, name='product_delete'),
]

from django.urls import path
import mainapp.views as mainapp
import basketapp.views as basket
from django.conf.urls import include

app_name = 'mainapp'

urlpatterns = [
    path('', mainapp.product, name='index'),
    path('product/<int:pk>/', mainapp.product, name='product'),
    path('product_details/<int:pk>/', mainapp.product_details, name='product_details'),
    path('category/<int:pk>/', mainapp.product, name='category'),
]

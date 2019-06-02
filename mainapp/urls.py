from django.urls import path
import mainapp.views as mainapp
from django.conf.urls import include

app_name = 'mainapp'

urlpatterns = [
    path('', mainapp.product, name='index'),
    path('<int:pk>/', mainapp.product, name='category'),
    path('auth/', include('authapp.urls', namespace='auth'))
]
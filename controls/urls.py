from django.urls import path
from .views import index, welcome

app_name = 'controls'

urlpatterns = [
    path('welcome', welcome, name='welcome'),
    path('', index, name='index_page'),
]

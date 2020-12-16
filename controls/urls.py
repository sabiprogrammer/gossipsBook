from django.urls import path
from .views import index, welcome
from users.views import register_user

app_name = 'controls'

urlpatterns = [
    path('users', register_user, name='register_user'),
    path('welcome', welcome, name='welcome'),
    path('', index, name='index_page'),
]

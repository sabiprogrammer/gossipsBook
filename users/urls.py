from django.urls import path
from .views import register_user, login_user

app_name = 'users'

urlpatterns = [
    path('', login_user, name='register_user'),
    path('login', login_user, name='login_user'),
]

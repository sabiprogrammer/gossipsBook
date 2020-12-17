from django.urls import path
from .views import register_user, login_user, user_profile

app_name = 'users'

urlpatterns = [
    path('profile', user_profile, name='user_profile'),
    path('login', login_user, name='login_user'),
    path('', login_user, name='register_user'),
]

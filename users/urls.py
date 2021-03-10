from django.contrib.auth import views as auth_views
from django.urls import path

from .views import login_user, user_profile, user_view_profile, follow_user

app_name = 'users'

urlpatterns = [
    path('profile', user_profile, name='user_profile'),
    path('<str:username>/profile', user_view_profile, name='user_view_profile'),
    path('follow/<str:username>', follow_user, name='follow_user'),
    # path('login', login_user, name='login_user'),
    path('', user_profile, name='register_user'),
]

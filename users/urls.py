from django.urls import path
from .views import login_user, user_profile, user_view_profile

app_name = 'users'

urlpatterns = [
    path('profile', user_profile, name='user_profile'),
    path('view_profile', user_view_profile, name='user_view_profile'),
    # path('login', login_user, name='login_user'),
    path('', user_profile, name='register_user'),
]

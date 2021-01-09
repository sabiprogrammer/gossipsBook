from django.urls import path
from .views import index, welcome, rfr, feedback

app_name = 'controls'

urlpatterns = [
    path('welcome', welcome, name='welcome'),
    path('rfr', rfr, name='rfr'),
    path('feedback', feedback, name='feedback'),
    path('', index, name='index_page'),
]

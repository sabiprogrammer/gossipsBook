from django.urls import path
from .views import answers_all, answers_new

app_name = 'answers'

urlpatterns = [
    path('', answers_all, name='answers'),
    path('all', answers_all, name='answers_all'),
    path('new', answers_new, name='answers_new'),
]

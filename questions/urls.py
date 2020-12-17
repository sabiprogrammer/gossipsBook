from django.urls import path
from .views import questions_index, questions_new

app_name = 'questions'

urlpatterns = [
    path('', questions_index, name='questions_index'),
    path('new', questions_new, name='questions_new'),
]

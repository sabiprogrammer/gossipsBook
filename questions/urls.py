from django.urls import path
from .views import questions_index, questions_new, oppose_question

app_name = 'questions'

urlpatterns = [
    path('', questions_index, name='questions_index'),
    path('oppose_question', oppose_question, name='oppose_question'),
    path('new', questions_new, name='questions_new'),
]

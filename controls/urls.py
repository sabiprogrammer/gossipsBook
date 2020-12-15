from django.urls import path
from .views import index, gossips,cheaters

app_name = 'controls'

urlpatterns = [
    path('', index, name='index_page'),
    path('questions', index, name='questions_page'),
    path('gossips', gossips, name='gossips_page'),
    path('cheaters', cheaters, name='cheaters_page'),
]

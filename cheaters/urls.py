from django.urls import path
from .views import cheaters_index, cheaters_new

app_name = 'cheaters'

urlpatterns = [
    path('', cheaters_index, name='cheaters_index'),
    path('new', cheaters_new, name='cheaters_new'),
]

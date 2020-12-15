from django.urls import path
from .views import gossips_index, gossips_new

app_name = 'gossips'

urlpatterns = [
    path('', gossips_index, name='gossips_index'),
    path('new', gossips_new, name='gossips_new'),
]

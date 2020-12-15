from django.urls import path
from .views import index, gossips,cheaters

app_name = 'controls'

urlpatterns = [
    path('', index, name='index_page'),
]

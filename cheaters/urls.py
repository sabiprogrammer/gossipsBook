from django.urls import path
from .views import cheaters_index, cheaters_new, cheater_add_comment, cheater_reaction

app_name = 'cheaters'

urlpatterns = [
    path('new', cheaters_new, name='cheaters_new'),
    path('cheater_add_comment', cheater_add_comment, name='cheater_add_comment'),
    path('reaction', cheater_reaction, name='cheater_reaction'),
    path('', cheaters_index, name='cheaters_index'),
]

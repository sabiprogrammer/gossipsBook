from django.urls import path
from .views import gossips_index, gossips_new, gossip_detail, gossip_reaction, gossip_add_comment

app_name = 'gossips'

urlpatterns = [
    path('', gossips_index, name='gossips_index'),
    path('new', gossips_new, name='gossips_new'),
    path('gossip_add_comment', gossip_add_comment, name='gossip_add_comment'),
    path('reactions', gossip_reaction, name='gossip_reaction'),
    path('<slug:gossip_slug>', gossip_detail, name='gossip_detail'),
]

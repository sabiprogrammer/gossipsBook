from django.contrib import admin
from .models import FalseInformation

# Register your models here.

@admin.register(FalseInformation)
class FalseInformationAdmin(admin.ModelAdmin):
    list_display = ['gossip', 'cheater']

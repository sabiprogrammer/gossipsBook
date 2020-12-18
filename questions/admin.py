from django.contrib import admin

from .models import QuestionsModel, Tags

admin.site.register(QuestionsModel)
admin.site.register(Tags)


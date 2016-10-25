from django.contrib import admin

from .models import Question

class ReportedQuestion(admin.ModelAdmin):
    list_filter= ['Reportada']

admin.site.register(Question, ReportedQuestion)

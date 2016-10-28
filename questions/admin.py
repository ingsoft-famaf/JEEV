from django.contrib import admin

from .models import Question


class QuestionAdmin(admin.ModelAdmin):
    fields = ['NombreTema', 'NombreMateria', 'TextPreg']

admin.site.register(Question, QuestionAdmin)

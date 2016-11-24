from django.contrib import admin
from .models import Question
from .models import Question, Answer


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 1


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['nombre_materia']}),
        (None, {'fields': ['nombre_tema']}),
        (None, {'fields': ['text_preg']}),
        (None, {'fields': ['reportada']}),
    ]
    inlines = [AnswerInline]

admin.site.register(Question, QuestionAdmin)

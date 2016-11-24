from django.contrib import admin
from models import Exam, ExamErrores, TemaE

# Register your models here.
"""
class TemaEAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['nombre_tema']}),
        ]"""
        
admin.site.register(Exam)
admin.site.register(ExamErrores)
admin.site.register(TemaE)
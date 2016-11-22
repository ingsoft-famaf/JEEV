from django.contrib import admin
from models import Materia, Tema


class TemaInline(admin.TabularInline):
    model = Tema
    extra = 1


class MateriaAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['nombre_materia']}),
        (None, {'fields': ['promedio']})
    ]
    inlines = [TemaInline]

admin.site.register(Materia, MateriaAdmin)

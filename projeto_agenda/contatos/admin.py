from django.contrib import admin
from .models import Categoria, Contato


class ContatoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'sobrenome', 'telefone', 'email', 'data_criacao', 'categoria', 'mostrar')
    list_display_links = ('nome', 'sobrenome')
    list_per_page = 10
    search_fields = ('nome', 'telefone', 'sobrenome', 'email')
    list_editable = ('telefone', 'mostrar')

# Register your models here.
admin.site.register(Categoria)
admin.site.register(Contato, ContatoAdmin)
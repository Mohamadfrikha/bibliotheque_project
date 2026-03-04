from django.contrib import admin
from .models import Catalogue, Livre
@admin.register(Catalogue)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ['nom', 'description']
    search_fields = ['nom']
@admin.register(Livre)
class LivreAdmin(admin.ModelAdmin):
    list_display = ['titre', 'auteur', 'categorie', 'date_publication']
    list_filter = ['categorie', 'date_publication']
    search_fields = ['titre', 'auteur']
    date_hierarchy = 'date_ajout'
    readonly_fields = ['date_ajout']
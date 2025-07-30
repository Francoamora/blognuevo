from django.contrib import admin
from .models import Post, Categoria, Comentario, Tag

# Personalización del panel de administración para Post
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'categoria', 'fecha_creacion', 'publicado')
    list_filter = ('categoria', 'fecha_creacion', 'publicado')
    search_fields = ('titulo', 'contenido', 'autor__username')
    date_hierarchy = 'fecha_creacion'
    autocomplete_fields = ['tags']
    list_editable = ('publicado',)
    ordering = ('-fecha_creacion',)
    filter_horizontal = ('tags',)

# Admin de Categorías
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

# Admin de Comentarios
@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('post', 'autor', 'fecha_creacion')
    list_filter = ('fecha_creacion',)
    search_fields = ('contenido', 'autor__username', 'post__titulo')

# Admin de Tags
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

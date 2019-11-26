from django.contrib import admin
from .models import Genre, Movie, Rating

# Register your models here.
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

class MovieAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'popularity', 'poster_path', 'overview', )

admin.site.register(Genre, GenreAdmin)
admin.site.register(Movie, MovieAdmin)


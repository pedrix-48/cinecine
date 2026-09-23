from django.contrib import admin
from .models import Movie, Genre, MovieGenre, MovieCast, MovieWatchLink, Review

admin.site.register(Movie)
admin.site.register(Genre)
admin.site.register(MovieCast)
admin.site.register(MovieWatchLink)
admin.site.register(Review)
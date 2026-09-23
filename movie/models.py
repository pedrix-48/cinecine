from django.db import models
from django.contrib.auth.models import User

class Movie(models.Model):
    title = models.CharField(max_length=150)
    overview = models.TextField(blank=True)
    release_year = models.SmallIntegerField(null=True, blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    runtime_minutes = models.SmallIntegerField(null=True, blank=True)
    language = models.CharField(max_length=10, blank=True)
    director = models.CharField(max_length=100, blank=True)
    poster_url = models.CharField(max_length=255, blank=True)
    trailer_youtube_id = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    genres = models.ManyToManyField('Genre', through='MovieGenre', related_name='movies')

    class Meta:
        db_table = 'movies'

    def __str__(self):
        return self.title


class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'genres'

    def __str__(self):
        return self.name


class MovieGenre(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='movie_genres')
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='movie_genres')

    class Meta:
        db_table = 'movie_genres'
        unique_together = ('movie', 'genre')


class MovieCast(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='cast')
    actor_name = models.CharField(max_length=100)
    character_name = models.CharField(max_length=100, blank=True)
    cast_order = models.IntegerField(default=0)

    class Meta:
        db_table = 'movie_cast'
        ordering = ['cast_order']

    def __str__(self):
        return f'{self.actor_name} as {self.character_name}'



class MovieWatchLink(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='watch_links')
    platform_name = models.CharField(max_length=50)
    url = models.CharField(max_length=500)
    sort_order = models.IntegerField(default=0)

    class Meta:
        db_table = 'movie_watch_links'
        ordering = ['sort_order']

    def __str__(self):
        return f'{self.movie.title} - {self.platform_name}'


class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.SmallIntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'reviews'

    def __str__(self):
        return f'Review by {self.user.username} on {self.movie.title}'
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.db.models import Q
from .models import Movie, Genre, MovieCast, MovieWatchLink, Review


def is_admin(user):
    return user.is_authenticated and user.is_staff


def home(request):
    movies = Movie.objects.all().order_by('-created_at')[:12]
    genres = Genre.objects.all()
    context = {
        'movies': movies,
        'genres': genres,
    }
    return render(request, 'movie/home.html', context)


def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    cast = MovieCast.objects.filter(movie=movie).order_by('cast_order')
    watch_links = MovieWatchLink.objects.filter(movie=movie).order_by('sort_order')
    reviews = Review.objects.filter(movie=movie).select_related('user')
    context = {
        'movie': movie,
        'cast': cast,
        'watch_links': watch_links,
        'reviews': reviews,
    }
    return render(request, 'movie/movie_detail.html', context)


def genre_movies(request, genre_name):
    genre = get_object_or_404(Genre, name=genre_name)
    movies = Movie.objects.filter(genres=genre).order_by('-created_at')
    context = {
        'genre': genre,
        'movies': movies,
    }
    return render(request, 'movie/genre_movies.html', context)


def search_movies(request):
    query = request.GET.get('q', '')
    movies = Movie.objects.all()
    if query:
        movies = movies.filter(
            Q(title__icontains=query) |
            Q(overview__icontains=query) |
            Q(director__icontains=query)
        )
    context = {
        'movies': movies,
        'query': query,
    }
    return render(request, 'movie/search.html', context)


def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            return render(request, 'movie/admin/login.html', {'error': 'Invalid credentials or not admin access'})
    return render(request, 'movie/admin/login.html')


@login_required(login_url='admin_login')
def admin_logout(request):
    logout(request)
    return redirect('admin_login')


@login_required(login_url='admin_login')
def admin_dashboard(request):
    if not is_admin(request.user):
        return HttpResponseForbidden()
    total_movies = Movie.objects.count()
    total_genres = Genre.objects.count()
    total_reviews = Review.objects.count()
    recent_movies = Movie.objects.all().order_by('-created_at')[:5]
    context = {
        'total_movies': total_movies,
        'total_genres': total_genres,
        'total_reviews': total_reviews,
        'recent_movies': recent_movies,
    }
    return render(request, 'movie/admin/dashboard.html', context)

@login_required(login_url='admin_login')
def admin_movies(request):
    if not is_admin(request.user):
        return HttpResponseForbidden()
    movies = Movie.objects.all().order_by('-created_at')
    context = {'movies': movies}
    return render(request, 'movie/admin/movies.html', context)


@login_required(login_url='admin_login')
def admin_add_movie(request):
    if not is_admin(request.user):
        return HttpResponseForbidden()
    if request.method == 'POST':
        title = request.POST.get('title')
        overview = request.POST.get('overview', '')
        release_year = request.POST.get('release_year') or None
        rating = request.POST.get('rating') or None
        runtime_minutes = request.POST.get('runtime_minutes') or None
        language = request.POST.get('language', '')
        director = request.POST.get('director', '')
        poster_url = request.POST.get('poster_url', '')
        trailer_youtube_id = request.POST.get('trailer_youtube_id', '')
        genre_names = request.POST.getlist('genres')

        movie = Movie.objects.create(
            title=title,
            overview=overview,
            release_year=release_year,
            rating=rating,
            runtime_minutes=runtime_minutes,
            language=language,
            director=director,
            poster_url=poster_url,
            trailer_youtube_id=trailer_youtube_id,
        )

        for gname in genre_names:
            genre, _ = Genre.objects.get_or_create(name=gname)
            movie.genres.add(genre)

        return redirect('admin_movies')

    genres = Genre.objects.all()
    context = {'genres': genres}
    return render(request, 'movie/admin/movie_form.html', context)


@login_required(login_url='admin_login')
def admin_edit_movie(request, movie_id):
    if not is_admin(request.user):
        return HttpResponseForbidden()
    movie = get_object_or_404(Movie, pk=movie_id)
    if request.method == 'POST':
        movie.title = request.POST.get('title')
        movie.overview = request.POST.get('overview', '')
        movie.release_year = request.POST.get('release_year') or None
        movie.rating = request.POST.get('rating') or None
        movie.runtime_minutes = request.POST.get('runtime_minutes') or None
        movie.language = request.POST.get('language', '')
        movie.director = request.POST.get('director', '')
        movie.poster_url = request.POST.get('poster_url', '')
        movie.trailer_youtube_id = request.POST.get('trailer_youtube_id', '')
        movie.save()

        genre_names = request.POST.getlist('genres')
        movie.genres.clear()
        for gname in genre_names:
            genre, _ = Genre.objects.get_or_create(name=gname)
            movie.genres.add(genre)

        return redirect('admin_movies')

    genres = Genre.objects.all()
    context = {'movie': movie, 'genres': genres}
    return render(request, 'movie/admin/movie_form.html', context)


@login_required(login_url='admin_login')
def admin_delete_movie(request, movie_id):
    if not is_admin(request.user):
        return HttpResponseForbidden()
    movie = get_object_or_404(Movie, pk=movie_id)
    if request.method == 'POST':
        movie.delete()
        return redirect('admin_movies')
    context = {'movie': movie}
    return render(request, 'movie/admin/movie_confirm_delete.html', context)


@login_required(login_url='admin_login')
def admin_genres(request):
    if not is_admin(request.user):
        return HttpResponseForbidden()
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            Genre.objects.create(name=name)
    genres = Genre.objects.all().order_by('name')
    context = {'genres': genres}
    return render(request, 'movie/admin/genres.html', context)


@login_required(login_url='admin_login')
def admin_cast(request):
    if not is_admin(request.user):
        return HttpResponseForbidden()
    if request.method == 'POST':
        movie_id = request.POST.get('movie')
        actor_name = request.POST.get('actor_name')
        character_name = request.POST.get('character_name', '')
        cast_order = request.POST.get('cast_order', 0)
        movie = get_object_or_404(Movie, pk=movie_id)
        MovieCast.objects.create(
            movie=movie,
            actor_name=actor_name,
            character_name=character_name,
            cast_order=cast_order,
        )
    casts = MovieCast.objects.all().select_related('movie').order_by('movie', 'cast_order')
    movies = Movie.objects.all()
    context = {'casts': casts, 'movies': movies}
    return render(request, 'movie/admin/cast.html', context)


@login_required(login_url='admin_login')
def admin_reviews(request):
    if not is_admin(request.user):
        return HttpResponseForbidden()
    reviews = Review.objects.all().select_related('movie', 'user').order_by('-created_at')
    context = {'reviews': reviews}
    return render(request, 'movie/admin/reviews.html', context)
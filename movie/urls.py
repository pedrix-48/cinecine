from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('movie/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('genre/<str:genre_name>/', views.genre_movies, name='genre_movies'),
    path('search/', views.search_movies, name='search_movies'),
    path('admin-panel/', views.admin_login, name='admin_login'),
    path('admin-panel/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-panel/movies/', views.admin_movies, name='admin_movies'),
    path('admin-panel/movies/add/', views.admin_add_movie, name='admin_add_movie'),
    path('admin-panel/movies/edit/<int:movie_id>/', views.admin_edit_movie, name='admin_edit_movie'),
    path('admin-panel/movies/delete/<int:movie_id>/', views.admin_delete_movie, name='admin_delete_movie'),
    path('admin-panel/genres/', views.admin_genres, name='admin_genres'),
    path('admin-panel/cast/', views.admin_cast, name='admin_cast'),
    path('admin-panel/reviews/', views.admin_reviews, name='admin_reviews'),
    path('admin-panel/logout/', views.admin_logout, name='admin_logout'),
]
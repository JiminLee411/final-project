from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('', views.movies_index, name='movies_index'),
    path('genres/', views.genres_index, name="genres_index"),
    path('<int:movie_pk>/', views.detail, name='detail'),
    path('<int:movie_pk>/like/', views.like, name='like'),
    path('<int:movie_pk>/ratings/<int:rating_pk>/update/', views.rating_update, name='rating_update'),
    path('<int:movie_pk>/ratings/<int:rating_pk>/delete/', views.rating_delete, name='rating_delete'),
    path('<int:movie_pk>/ratings/new/', views.create_rating, name='create_rating'),
    path('myfavorite/', views.myfavorite, name='myfavorite'),
    path('genres/', views.genres_list, name='genres_list'),
    path('actors/', views.actors_list),
    path('<int:movie_pk>/rating/<int:rating_pk>/', views.rating_update_and_delete),
    path('<int:movie_pk>/rating/', views.rating_create),
    # path('<int:movie_pk>/', views.movie_detail),
    path('api/genres/', views.genres_list, name="genres_list"),
    path('api/genres/<int:pk>/', views.genres_detail, name="genres_detail"),
    path('api/movies/<int:pk>/', views.movies_detail, name="movies_detail"),
    
]
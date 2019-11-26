from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('', views.movies_index, name='movies_index'),
    path('<int:movie_pk>/', views.movies_detail, name='movies_detail'),
    path('<int:movie_pk>/ratings/new/', views.rating_create, name='rating_create'),
    path('<int:movie_pk>/ratings/<int:rating_pk>/delete/', views.rating_delete, name='rating_delete'),
    path('<int:movie_pk>/like/', views.like, name='like'),
    path('<int:rating_pk>/update_score/', views.update_score, name="update_score"),
]
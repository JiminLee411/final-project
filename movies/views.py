from django.shortcuts import render, redirect, get_object_or_404
from .models import Genre, Movie, Rating
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .forms import RatingForm
from django.contrib import messages

from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import GenreSerializer, MovieSerializer, RatingSerializer


# Create your views here.
def movies_index(request):
    movies = Movie.objects.exclude(poster_path=0)
    movies_popular = Movie.objects.order_by('id')[0:20]
    movies_vote = Movie.objects.order_by('-vote_average')[0:20]
    print(movies_vote)
    genres = Genre.objects.all()
    keyword = request.GET.get('keyword', '')
    if keyword:
        movies = movies.filter(title__icontains=keyword)
        context = {
            'movies_popular' : None,
            'movies_vote' : None,
            'movies': movies,
            'genres' : genres,
        }
    else:
        context = {
            'movies_popular' : movies_popular,
            'movies_vote' : movies_vote,
            'movies': None,
            'genres' : genres,
        }
    return render(request, 'movies/movies_index.html', context)
    
def detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    # genres = Genre.objects.all()
    # if movie.genres == genres.name:

    form = RatingForm()
    context = {
        'movie': movie,
        'form': form
    }
    return render(request, 'movies/movies_detail.html', context)

def genres_index(request):
    genre = get_object_or_404(Genre, type=request.GET.get('type'))
    return render(request, 'movies/genre.html', {'genre': genre})


@api_view(["GET"])
def genres_list(request):
    genres = Genre.objects.all()
    serializer = GenreSerializer(genres, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def genres_detail(request, pk):
    genre = get_object_or_404(Genre, pk=pk)
    serializer = GenreSerializer(genre)
    return Response(serializer.data)


@api_view(["GET"])
def movies_list(request):
    movies = Movie.objects.all()
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def movies_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    serializer = MovieSerializer(movie)
    return Response(serializer.data)


@api_view(["GET", "POST"])
def ratings_list(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    if request.method == "GET":
        ratings = movie.ratings.all()
        serializer = RatingSerializer(ratings, many=True)
        return Response(serializer.data)
    else:
        if request.user.is_authenticated:
            request.data["movie"] = movie.id
            request.data["user"] = request.user.id
            serializer = RatingSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(["GET", "DELETE", "PUT"])
def ratings_detail(request, pk):
    rating = get_object_or_404(Rating, pk=pk)
    if request.method == 'GET':
        serializer = RatingSerializer(rating)
        return Response(serializer.data)
    else:
        if request.user == rating.user:
            request.data["movie"] = rating.movie.id
            request.data["user"] = request.user.id
            if request.method == 'PUT':
                serializer = RatingSerializer(rating, data=request.data)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            elif request.method == 'DELETE':
                rating.delete()
                return Response({"message": "삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


@require_POST
def rating_create(request, movie_pk):
    if request.user.is_authenticated:
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.user = request.user
            rating.movie_id = movie_pk
            rating.save()
    else:
        messages.warning(request, '로그인이 필요합니다.')
    return redirect('movies:movies_detail', movie_pk)

def rating_delete(request, movie_pk, rating_pk):
    rating = get_object_or_404(Rating, pk=rating_pk)
    rating.delete()
    messages.warning(request, '리뷰가 삭제되었습니다.')
    return redirect('movies:movies_detail', movie_pk)

@require_POST
def like(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    if request.user.is_authenticated:
        if movie in request.user.like_movies.all():
            request.user.like_movies.remove(movie)
        else:
            request.user.like_movies.add(movie)
    else:
        messages.warning(request, '로그인이 필요한 기능입니다.')
    return redirect('movies:movies_detail', movie_pk)

def update_score(request, rating_pk):
    rating = get_object_or_404(Rating, pk=rating_pk)
    if request.user == rating.user:
        if request.method == 'POST':
            form = ratingForm(request.POST, instance=rating)
            if form.is_valid():
                form.save()
                return redirect('movies:movies_detail', rating.movie.pk)
        else:
            form = ratingForm(instance=rating)
        context = {
            'form': form
        }
        return render(request, 'accounts/form.html', context)
    else:
        messages.warning(request, '수정 권한이 없습니다.')
    return redirect('movies:movies_detail', rating.movie.pk)

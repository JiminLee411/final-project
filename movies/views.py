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
    ratings = movie.rating_set.all()
    # genres = Genre.objects.all()
    # if movie.genres == genres.name:

    rating_form = RatingForm()
    context = {
        'movie': movie,
        'ratings': ratings,
        'rating_form': rating_form
    }
    return render(request, 'movies/movies_detail.html', context)

def genres_index(request):
    genre = get_object_or_404(Genre, type=request.GET.get('type'))
    return render(request, 'movies/genre.html', {'genre': genre})

@api_view(["GET"])
def movies_list(request):
    movies = Movie.objects.all()
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def genres_list(request):
    genres = Genre.objects.all()
    serializer = GenreSerializer(genres, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def actors_list(request):
    actors = Actor.objects.all()
    serializer = ActorSerializer(actors, many=True)
    return Response(serializer.data)

# @api_view(["GET"])
# def genres_detail(request, pk):
#     genre = get_object_or_404(Genre, pk=pk)
#     serializer = GenreSerializer(genre)
#     return Response(serializer.data)

@api_view(["GET"])
def movies_detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    serializer = MovieSerializer(movie)
    return Response(serializer.data)

@login_required  
@api_view(['POST'])
def rating_create(request, movie_pk):
    movie = get_object_or_404(Movie, pk= movie_pk)
    serializer = RatingSerializer(data = request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(movie_id=movie_pk)
        return Response({'message': '작성되었습니다'})

@login_required
@api_view(['PUT','DELETE'])
def rating_update_and_delete(request, rating_pk, movie_pk):
    rating = get_object_or_404(Rating, pk = rating_pk)
    if request.method == 'PUT':
        serializer = RatingSerializer(data= request.data, instance=rating)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': '수정되었습니다'})
    else:
        # 작성자와 동일한지 확인해보고 삭제시켜줘
        score.delete()
        return Response({'message': '삭제되었습니다.'})

@require_POST
@login_required
def create_rating(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    if len(movie.rating_set.filter(user_id = request.user.id)) == 0:
        rating_form = RatingForm(request.POST)
        if rating_form.is_valid():
            rating = rating_form.save(commit=False)
            rating.user = request.user
            rating.movie_id = movie_pk
            rating.save()
    return redirect('movies:detail', movie_pk)

@login_required
def rating_update(request, movie_pk, rating_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    rating = get_object_or_404(Rating, pk=rating_pk)
    if rating.user != request.user:
        return redirect('movies:detail', movie_pk)

    if request.method == 'POST':
            rating_form = RatingForm(request.POST, instance=rating)
            if rating_form.is_valid():
                rating.save()
                return redirect('movies:detail', movie_pk)
    else:
        rating_form = RatingForm(instance=rating)
    context = {
        'rating_form':rating_form
    }
    return render(request, 'movies/form.html', context)

@login_required
def rating_delete(request, movie_pk, rating_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    rating = get_object_or_404(Rating, pk=rating_pk)
    if request.method == 'POST':
        rating.delete()
        messages.warning(request, '리뷰가 삭제되었습니다.')
    return redirect('movies:detail', movie_pk)

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
    return redirect('movies:detail', movie_pk)

def update_score(request, rating_pk):
    rating = get_object_or_404(Rating, pk=rating_pk)
    if request.user == rating.user:
        if request.method == 'POST':
            form = ratingForm(request.POST, instance=rating)
            if form.is_valid():
                form.save()
                return redirect('movies:detail', rating.movie.pk)
        else:
            form = ratingForm(instance=rating)
        context = {
            'form': form
        }
        return render(request, 'accounts/form.html', context)
    else:
        messages.warning(request, '수정 권한이 없습니다.')
    return redirect('movies:detail', rating.movie.pk)
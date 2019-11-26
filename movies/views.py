from django.shortcuts import render, redirect, get_object_or_404
from .models import Genre, Movie, Rating
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .forms import RatingForm
from django.contrib import messages

# Create your views here.
def movies_index(request):
    movies = Movie.objects.all()
    genres = Genre.objects.all()
    keyword = request.GET.get('keyword', '')
    if keyword:
        movies = movies.filter(title__icontains=keyword)
    context = {
        'movies' : movies,
        'genres' : genres,
    }
    return render(request, 'movies/movies_index.html', context)

def genres_view(request):
    genre = get_object_or_404(Genre, type=request.GET.get('type'))
    return render(request, 'movies/genre.html', {'genre': genre})

    
def movies_detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    form = RatingForm()
    context = {
        'movie': movie,
        'form': form
    }
    return render(request, 'movies/movies_detail.html', context)

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
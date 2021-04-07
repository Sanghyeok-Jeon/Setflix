from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Genre, Review, Comment
from .forms import ReviewForm, CommentForm
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q
from decouple import config

# Create your views here.

def index(request):
    movies = Movie.objects.order_by('?')
    genres = Genre.objects.order_by('name')
    MOVIES_API = config('MOVIES_API')

    context = {
        'movies': movies,
        'genres': genres,
        'MOVIES_API': MOVIES_API,
    }

    return render(request, 'movies/index.html', context)

def community(request):
    reviews = Review.objects.order_by('-created_at') ###
    paginator = Paginator(reviews, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'reviews': reviews,
        'page_obj': page_obj,
    }
    return render(request, 'movies/community.html', context)

@login_required
def review_form(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)

    if request.method == "POST":
        form = ReviewForm(request.POST)

        if form.is_valid():
            review = form.save(commit=False)
            review.movie_title = movie
            review.user = request.user
            review.save()
            return redirect('movies:movie_detail', movie_pk)

    else:
        form = ReviewForm()

    context = {
        'form': form
    }
    return render(request, 'movies/review_form.html', context)

@login_required
def review_detail(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    comment_form = CommentForm()

    context = {
        'review': review,
        'comment_form': comment_form,
    }
    return render(request, 'movies/review_detail.html', context)

@require_POST
@login_required
def delete(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if request.user == review.user:
        review.delete()

    return redirect('movies:community')


@login_required
def update(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if request.user == review.user:
        if request.method == "POST":
            form = ReviewForm(request.POST, instance=review)
            if form.is_valid():
                review = form.save(commit=False)
                review.user = request.user
                review.save()
                return redirect('movies:review_detail', review.pk)

        else:
            form = ReviewForm(instance=review)
        context = {
            'form': form
        }
        return render(request, 'movies/review_form.html', context)
    else:
        return redirect('movies:index')

@login_required
def like(request, review_pk):
    user = request.user
    review = get_object_or_404(Review, pk=review_pk)

    if review.like_users.filter(pk=user.pk).exists():
        review.like_users.remove(user)
        liked = False
    else:
        review.like_users.add(user)
        liked = True

    context = {
        'liked': liked,
        'count': review.like_users.count(),
    }
    return JsonResponse(context)

@login_required
def comment_create(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)

    if request.method == "POST":
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.review = review
            comment.user = request.user
            comment.save()

    return redirect('movies:review_detail', review_pk)

@login_required
def comment_delete(request, review_pk, comment_pk):
    if request.method == "POST":
        comment = get_object_or_404(Comment, pk=comment_pk)
        if request.user == comment.user:
            comment.delete()

    return redirect('movies:review_detail', review_pk)

def movie_detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    reviews = movie.review_set.all().order_by('-review.created_at')

    context = {
        'reviews': reviews,
        'movie': movie,
    }
    return render(request, 'movies/movie_detail.html', context)

@login_required
def recommend1(request):
    genres = Genre.objects.order_by('name')

    context = {
        'genres': genres,
    }
    return render(request, 'movies/recommend1.html', context)

@login_required
def recommend2(request, genre_pk):
    genre = Genre.objects.get(pk=genre_pk)
    genre_movies = []

    for movie in Movie.objects.all():
        if genre in movie.genres.all():
            genre_movies.append(movie)

    context = {
        'genre': genre,
        'genre_movies': genre_movies,
    }
    return render(request, 'movies/recommend2.html', context)

@login_required
def recommend3(request, genre_pk, nation):
    genre = Genre.objects.get(pk=genre_pk)
    nation_movies = []

    if nation == 'ko':
        for movie in Movie.objects.filter(original_language='ko'):
            if genre in movie.genres.all():
                nation_movies.append(movie)
    else:
        for movie in Movie.objects.filter(~Q(original_language='ko')):
            if genre in movie.genres.all():
                nation_movies.append(movie)

    context = {
        'genre': genre,
        'nation_movies': nation_movies,
        'nation': nation,
    }
    return render(request, 'movies/recommend3.html', context)

@login_required
def recommend4(request, genre_pk, nation, popular):
    genre = Genre.objects.get(pk=genre_pk)
    popular_movies = []

    if popular == 'yes':
        if nation == 'ko':
            for movie in Movie.objects.filter(original_language='ko').order_by('-popularity'):
                if genre in movie.genres.all():
                    popular_movies.append(movie)
        else:
            for movie in Movie.objects.filter(~Q(original_language='ko')).order_by('-popularity'):
                if genre in movie.genres.all():
                    popular_movies.append(movie)
    else:
        if nation == 'ko':
            for movie in Movie.objects.filter(original_language='ko').order_by('?'):
                if genre in movie.genres.all():
                    popular_movies.append(movie)
        else:
            for movie in Movie.objects.filter(~Q(original_language='ko')).order_by('?'):
                if genre in movie.genres.all():
                    popular_movies.append(movie)

    context = {
        'genre': genre,
        'popular_movies': popular_movies,
        'nation': nation,
        'popular': popular,
    }

    return render(request, 'movies/recommend4.html', context)

@login_required
def recommend_result(request, genre_pk, nation, popular, vote):
    genre = Genre.objects.get(pk=genre_pk)
    result_movies = []

    if vote == 'yes':
        if popular == 'yes':
            if nation == 'ko':
                for movie in Movie.objects.filter(original_language='ko').order_by('-vote_average', '-popularity'):
                    if genre in movie.genres.all():
                        result_movies.append(movie)
            else:
                for movie in Movie.objects.filter(~Q(original_language='ko')).order_by('-vote_average', '-popularity'):
                    if genre in movie.genres.all():
                        result_movies.append(movie)
        else:
            if nation == 'ko':
                for movie in Movie.objects.filter(original_language='ko').order_by('-vote_average'):
                    if genre in movie.genres.all():
                        result_movies.append(movie)
            else:
                for movie in Movie.objects.filter(~Q(original_language='ko')).order_by('-vote_average'):
                    if genre in movie.genres.all():
                        result_movies.append(movie)
    else:
        if popular == 'yes':
            if nation == 'ko':
                for movie in Movie.objects.filter(original_language='ko').order_by('-popularity'):
                    if genre in movie.genres.all():
                        result_movies.append(movie)
            else:
                for movie in Movie.objects.filter(~Q(original_language='ko')).order_by('-popularity'):
                    if genre in movie.genres.all():
                        result_movies.append(movie)
        else:
            if nation == 'ko':
                for movie in Movie.objects.filter(original_language='ko').order_by('?'):
                    if genre in movie.genres.all():
                        result_movies.append(movie)
            else:
                for movie in Movie.objects.filter(~Q(original_language='ko')).order_by('?'):
                    if genre in movie.genres.all():
                        result_movies.append(movie)
    count = len(result_movies)
    context = {
        'genre': genre,
        'result_movies': result_movies[:3] if count > 3 else result_movies,
        'count': count,
    }
    return render(request, 'movies/recommend_result.html', context)

@login_required
def recommend_anything(request):
    movies = Movie.objects.order_by('?')[:3]

    context = {
        'movies': movies,
    }
    return render(request, 'movies/recommend_anything.html', context)

@login_required
def recommend_genre(request, pk):
    genre = Genre.objects.get(pk=pk)
    movies = []
    count = 0
    for movie in Movie.objects.order_by('-vote_count'):
        if count > 2:
            break

        if genre in movie.genres.all():
            movies.append(movie)
            count += 1
    context = {
        'genre': genre,
        'movies': movies,
        'count': count,
    }
    return render(request, 'movies/recommend_genre.html', context)
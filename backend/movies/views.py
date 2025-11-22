from django.shortcuts import render
from .models import MovieData
from django.db.models import Q
from django.http import HttpResponse

def home(request):
    movies = MovieData.objects.all()
    return render(request, 'movies/home.html', {'movies' : movies})

def detail(request, id):
    movie = MovieData.objects.get(id=id)
    return render(request, 'movies/detail.html', {'movie': movie})

def score(request):
    return render(request, 'movies/score.html')

def recommend(request):
    return render(request, 'movies/home.html')



def search(request):
    query = request.GET.get('query', '')       # 검색어
    genre = request.GET.get('genre', '')       # 장르
    difficulty = request.GET.get('difficulty', '')  # 난이도

    movies = MovieData.objects.all()

    if query:
        movies = movies.filter(
            Q(title_ko__icontains=query) |
            Q(title_en__icontains=query)
        )

    if genre:
        movies = movies.filter(genre__icontains=genre)

    if difficulty:
        movies = movies.filter(difficulty=difficulty)

    return render(request, 'movies/home.html', {'movies': movies})

def recommend(request):
    score = request.GET.get('score')

    movies = []

    if score:
        eng_score = int(score)

        if 0<= eng_score <= 220 :
            movies = MovieData.objects.filter(difficulty = 0)

        elif eng_score <= 545:
            movies = MovieData.objects.filter(difficulty = 1)

        elif eng_score <= 780:
            movies = MovieData.objects.filter(difficulty = 2)

        elif eng_score <= 940:
            movies = MovieData.objects.filter(difficulty = 3)

        elif eng_score <= 990:
            movies = MovieData.objects.filter(difficulty = 4)

        else :
            context = {'message': '유효한 점수가 아닙니다 (0~990). 다시 입력해주세요.'}
            return render(request, 'movies/score.html', context)

  
        
    return render(request, 'movies/home.html', {'movies' : movies})

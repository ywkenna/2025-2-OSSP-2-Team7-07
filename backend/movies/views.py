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

CATEGORY_MAP = {
    "액션/스릴러": ["액션", "스릴러", "범죄", "느와르", "네오 느와르", "네오-서부"],
    "드라마/감성": ["드라마", "심리 드라마","심리 스릴러", "성장","우정", "가족", "감성"],
    "SF/판타지": ["SF", "판타지", "디스토피아", "포스트 아포칼립스"],
    "코미디": ["코미디", "블랙 코미디"],
    "역사/전쟁": ["전쟁", "역사", "시대극"],
    "애니메이션": ["애니메이션"],
    "기타": ["어드벤처", "미스터리", "음악", "스포츠", "전기 영화(실화)", "크리스마스", "질병", "항공"],
}


def search(request):
    query = request.GET.get('query', '')       # 검색어
    genre_category = request.GET.get('genre', '')       # 장르
    difficulty = request.GET.get('difficulty', '')  # 난이도

    movies = MovieData.objects.all()


    if query:
        movies = movies.filter(
            Q(title_ko__icontains=query) |
            Q(title_en__icontains=query)
        )

    if genre_category:
        tags = CATEGORY_MAP.get(genre_category, [])
        if tags:
            genre_filter = Q()
            for tag in tags:
                genre_filter |= Q(genre__icontains=tag)
            movies = movies.filter(genre_filter)

    if difficulty:
        movies = movies.filter(difficulty=difficulty)

    return render(request, 'movies/home.html', {'movies': movies})

def recommend(request):

    exam_type = request.GET.get('type')   # toeic / toefl / ielts
    score = request.GET.get('score')

    try:
        score = float(score)
    except ValueError:
        return render(request, 'movies/score.html', {
            'message': '점수는 숫자로 입력해주세요.'
        })
    
    difficulty = None

    if exam_type == 'toeic':
        if 0 <= score <= 220:
            difficulty = 0
        elif score <= 545:
            difficulty = 1
        elif score <= 780:
            difficulty = 2
        elif score <= 940:
            difficulty = 3
        elif score <= 990:
            difficulty = 4

    elif exam_type == 'toefl':
        if 42 <= score <=71:
            difficulty = 2
        elif 72 <= score <=94:
            difficulty = 3
        elif 95 <= score <=120:
            difficulty = 4
    

    elif exam_type == 'ielts':
        if 2.5 <= score < 3.5:
            difficulty = 1
        elif 4.0 <= score < 5.0:
            difficulty = 2
        elif 5.5 <= score < 6.5:
            difficulty = 3
        elif 7.0 <= score < 8.0:
            difficulty = 4
        elif 8.5 <= score <= 9.0:
            difficulty = 5

    movies = MovieData.objects.filter(difficulty=difficulty)

    return render(request, 'movies/home.html', {'movies': movies})
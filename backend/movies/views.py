from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q
from django.conf import settings

from .models import MovieData


# CATEGORY MAP (프론트 필터와 매칭)
CATEGORY_MAP = {
    "액션/스릴러": ["액션", "스릴러", "범죄"],
    "드라마/감성": ["드라마", "멜로", "감성"],
    "SF/판타지": ["SF", "판타지"],
    "코미디": ["코미디"],
    "역사/전쟁": ["전쟁", "역사"],
    "애니메이션": ["애니메이션"],
    "기타": [],
}


# ------------------------------------------------
# 1) 기본 영화 리스트 API
# ------------------------------------------------
def movies_api(request):
    movies = MovieData.objects.all()
    results = []

    for m in movies:
        # m.image 처리 (FileField / 문자열 모두 지원)
        if hasattr(m.image, 'url'):
            image_path = m.image.url
        else:
            image_path = m.image

        # 절대 URL 생성
        image_url = f"{request.scheme}://{request.get_host()}{settings.STATIC_URL}{image_path.lstrip('/')}"
        
        results.append({
            "id": m.id,
            "title_ko": m.title_ko,
            "title_en": m.title_en,
            "year": m.year,
            "runtime": m.runtime,
            "genre": m.genre,
            "difficulty": m.difficulty,
            "plot": m.plot,
            "image": image_url,
        })

    return JsonResponse(results, safe=False)


# ------------------------------------------------
# 2) 검색 API (프론트 search 기능)
# ------------------------------------------------
def movies_search_api(request):
    query = request.GET.get("query", "")
    genre = request.GET.get("genre", "")
    difficulty = request.GET.get("difficulty", "")

    movies = MovieData.objects.all()

    # 검색어 필터
    if query:
        movies = movies.filter(
            Q(title_ko__icontains=query) |
            Q(title_en__icontains=query)
        )

    # 장르 필터 (CATEGORY_MAP 기반)
    if genre and genre != "전체":
        tags = CATEGORY_MAP.get(genre, [])
        if tags:
            genre_filter = Q()
            for t in tags:
                genre_filter |= Q(genre__icontains=t)
            movies = movies.filter(genre_filter)

    # 난이도 필터
    if difficulty and difficulty != "전체":
        try:
            movies = movies.filter(difficulty=int(difficulty))
        except:
            pass

    # 이미지 포함한 JSON으로 변환
    results = []
    for m in movies:
        # image가 str인지 File인지 체크
        if hasattr(m.image, 'url'):
            image_path = m.image.url
        else:
            image_path = m.image

        image_url = f"{request.scheme}://{request.get_host()}/static/{image_path.lstrip('/')}"

        results.append({
            "id": m.id,
            "title_ko": m.title_ko,
            "title_en": m.title_en,
            "year": m.year,
            "runtime": m.runtime,
            "genre": m.genre,
            "difficulty": m.difficulty,
            "plot": m.plot,
            "image": image_url,
        })

    return JsonResponse(results, safe=False)

# ------------------------------------------------
# 3) detail 페이지 HTML용
# ------------------------------------------------
def home(request):
    return render(request, "movies/home.html")

def detail(request, id):
    return render(request, "movies/detail.html")

def score(request):
    return render(request, "movies/score.html")

def recommend(request):
    return render(request, "movies/recommend.html")


# ------------------------------------------------
# 4) 단일 영화 JSON API
# ------------------------------------------------
def movie_detail_api(request, id):
    movie = MovieData.objects.get(id=id)

    if hasattr(movie.image, 'url'):
        image_path = movie.image.url
    else:
        image_path = movie.image

    image_url = f"{request.scheme}://{request.get_host()}{settings.STATIC_URL}{image_path.lstrip('/')}"

    result = {
        "id": movie.id,
        "title_ko": movie.title_ko,
        "title_en": movie.title_en,
        "year": movie.year,
        "runtime": movie.runtime,
        "genre": movie.genre,
        "difficulty": movie.difficulty,
        "plot": movie.plot,
        "image": image_url,
    }

    return JsonResponse(result)

def movies_recommend_api(request):
    score = int(request.GET.get("score", 0))
    test_type = request.GET.get("type")

    # 예시: 난이도 선택 단순 버전
    if test_type == "toeic":
        level = score_to_level_toeic(score)
    elif test_type == "toefl":
        level = score_to_level_toefl(score)
    else:
        level = 2  # 기본값

    movies = MovieData.objects.filter(difficulty=level)
    return JsonResponse(list(movies.values()), safe=False)

def score_to_level_toeic(score):
    score = int(score)
    if score < 300: return 0   # A1
    if score < 500: return 1   # A2
    if score < 700: return 2   # B1
    if score < 900: return 3   # B2
    return 4                  # C1 이상

def score_to_level_toefl(score):
    score = int(score)
    if score < 40: return 0
    if score < 60: return 1
    if score < 80: return 2
    if score < 100: return 3
    return 4

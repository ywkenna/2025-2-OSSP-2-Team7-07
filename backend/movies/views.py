from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q
from django.conf import settings

from .models import MovieData, Comment

from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


# CATEGORY MAP (프론트 필터와 매칭)
CATEGORY_MAP = {
    "액션/스릴러": ["액션", "스릴러", "범죄", "느와르", "네오 느와르", "네오-서부"],
    "드라마/감성": ["드라마", "심리 드라마","심리 스릴러", "성장","우정", "가족", "감성"],
    "SF/판타지": ["SF", "판타지", "디스토피아", "포스트 아포칼립스"],
    "코미디": ["코미디", "블랙 코미디"],
    "역사/전쟁": ["전쟁", "역사", "시대극"],
    "애니메이션": ["애니메이션"],
    "기타": ["어드벤처", "미스터리", "음악", "스포츠", "전기 영화(실화)", "크리스마스", "질병", "항공"],
}


# ------------------------------------------------
# 기본 영화 리스트 API
# ------------------------------------------------
def movies_api(request):
    movies = MovieData.objects.all()
    results = []

    for m in movies:
         

        if m.image.startswith("http://") or m.image.startswith("https://"):
        # 이미 완전한 URL인 경우
            image_url = m.image  
        else:
        # 상대경로 → 정적경로로 변환
            image_url = f"{request.scheme}://{request.get_host()}/static/{m.image.lstrip('/')}"

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
# 검색 API (프론트 search 기능)
# ------------------------------------------------
def movies_search_api(request):
    query = request.GET.get("query", "")
    genre = request.GET.get("genre", "")
    difficulty = request.GET.get("difficulty", "")
    year_range = request.GET.get("year", "")
    sort_option = request.GET.get("sort", "default")

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

    #연도 범위 필터 
    if year_range and year_range != "전체":
        try:
            start, end = year_range.split("~")
            start = int(start.strip())
            end = int(end.strip())
            movies = movies.filter(year__gte=start, year__lte=end)
        except:
            pass  

    # 정렬
    if sort_option == "difficulty_desc":
        movies = movies.order_by("-difficulty")   # 어려운 순
    elif sort_option == "difficulty_asc":
        movies = movies.order_by("difficulty")    # 쉬운 순
    elif sort_option == "year_desc":
        movies = movies.order_by("-year")         # 최신 순
    elif sort_option == "year_asc":
        movies = movies.order_by("year")          # 오래된 순
    else:
        movies = movies.order_by("id")            # 기본 정렬 (id 기준)

    # 이미지 포함한 JSON으로 변환
    results = []
    for m in movies:


        if m.image.startswith("http://") or m.image.startswith("https://"):
        # 이미 완전한 URL인 경우
            image_url = m.image  
        else:
        # 상대경로 → 정적경로로 변환
            image_url = f"{request.scheme}://{request.get_host()}/static/{m.image.lstrip('/')}"

       

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
#  단일 영화 JSON API
# ------------------------------------------------
def movie_detail_api(request, id):
    movie = MovieData.objects.get(id=id)

    
    if movie.image.startswith("http://") or movie.image.startswith("https://"):
        # 이미 완전한 URL인 경우
        image_url = movie.image  
    else:
        # 상대경로 → 정적경로로 변환
        image_url = f"{request.scheme}://{request.get_host()}/static/{movie.image.lstrip('/')}"


    #코멘트 목록 추가
    comments_qs = Comment.objects.filter(movie=movie).select_related("user")

    comments_data = [
        {
            "user": c.user.username,
            "content": c.content,
            "created": c.created_time.strftime("%Y-%m-%d %H:%M")
        }
        for c in comments_qs
    ]

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

        #지표별 분석 결과 (전부 0~100으로 정규화됨.)
        ##어휘: 어휘 다양성, 어휘 난이도, 숙어 비율, 슬랭 비율, 희귀단어 비율, 단어 당 음절 수 
        ##문법: 절 비율, 구문 트리 깊이, 과거분사 비율
        ##중첩발화 비율, 전체 빠르기, 발음 정확도, 레벤슈타인 거리 
        

        "status" : {
            "word_avg_level":movie.word_avg_level, #어휘 난이도 
            "tree_depth" : movie.tree_depth,   #구문 트리 깊이
            "pron_acc" : movie.pron_acc,    #발음 정확도
            "real_word" : movie.real_word, #어휘 다양성
            "clause_ratio" : movie.clause_ratio,  #절 비율
            "overlap_ratio": movie.overlap_ratio, #중첩발화 비율
            "phrase_ratio": movie.phrase_ratio, #숙어 비율
            "pp_ratio": movie.pp_ratio,  #과거분사 비율 
            "rare_word_ratio": movie.rare_word_ratio, #희귀단어 비율
            "slang_ratio": movie.slang_ratio, #슬랭 비율
            "syllable_word": movie.syllable_word,  #단어 당 음절 수
            "avg_speed": movie.avg_speed,   #전체 빠르기
            "lev_distance": movie.lev_distance,     #레벤슈타인 거리 
        },

        #OTT 바로가기 링크 (각 영화별로 1~4개의 링크 존재 (예: 프레스티지: 웨이브, 왓챠 링크 존재))

        "ott" : {
            "wavve_url": movie.wavve_url,
            "watcha_url":  movie.watcha_url,
            "netflix_url": movie.netflix_url,
            "tiving_url": movie.tiving_url,
            "coupang_url": movie.coupang_url,
            "disney_url": movie.disney_url,
        },

        "comments": comments_data

        
    }

    return JsonResponse(result)

def movies_recommend_api(request):
    score = request.GET.get("score")
    test_type = request.GET.get("type")

    # 점수 숫자 변환
    try:
        score = float(score)
    except (TypeError, ValueError):
        return JsonResponse({"error": "점수는 숫자로 입력해주세요."}, status=400)

    # 시험 종류별 난이도 매핑
    if test_type == "toeic":
        level = score_to_level_toeic(score)
    elif test_type == "toefl":
        level = score_to_level_toefl(score)
    elif test_type == "ielts":
        level = score_to_level_ielts(score)

    #잘못된 점수를 입력한 경우
    if level is None:
        return JsonResponse({"error": "유효하지 않은 점수 범위입니다."}, status=400)

    

    movies = MovieData.objects.filter(difficulty=level)

    return JsonResponse(list(movies.values()), safe=False)


def score_to_level_toeic(score):
    
    if not (0 <= score <= 990):
        return None
    if 0 <=score <= 545:
        return 1
    elif score <= 780:
        return 2
    elif score <= 940:
        return 3
    else: 
        return 4


def score_to_level_toefl(score):
   
    if not (0 <= score <= 120):
        return None
   
    if 0 <= score <= 41:
        return 1
    elif score <= 71:
        return 2
    elif score <= 94:
        return 3
    else :
        return 4
    


def score_to_level_ielts(score):
    if not (0 <= score <= 9.0):
        return None
    
    if 0 <= score < 3.5:
        return 1
    elif score < 5.0:
        return 2
    elif score < 6.5:
        return 3
    else:
        return 4



# -----코멘트 작성 API-------
@require_POST
@login_required   # 회원만 댓글 작성 가능
def comment_create_api(request, movie_id):
    content = request.POST.get("content", "").strip()

    if not content:
        return JsonResponse({"error": "댓글 내용을 입력해주세요."}, status=400)

    try:
        movie = MovieData.objects.get(id=movie_id)
    except MovieData.DoesNotExist:
        return JsonResponse({"error": "영화를 찾을 수 없습니다."}, status=404)

    comment = Comment.objects.create(
        movie=movie,
        user=request.user,
        content=content
    )

    return JsonResponse({
        "message": "댓글이 등록되었습니다.",
        "comment": {
            "user": request.user.username,
            "content": comment.content,
            "created": comment.created_time.strftime("%Y-%m-%d %H:%M"),
        }
    })



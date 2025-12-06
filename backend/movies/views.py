from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q
from django.conf import settings

from .models import MovieData, Comment

from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model

User = get_user_model()



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
        # 이미지 경로 보정
            img = m.image.strip()

            # DB에 파일명만 저장되어 있으면 자동으로 movies/images/ 붙여줌
            if not img.startswith("movies/images/"):
                img = "movies/images/" + img.lstrip("/")

            image_url = f"{request.scheme}://{request.get_host()}/static/{img}"


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
    query       = request.GET.get("query", "")
    genre       = request.GET.get("genre", "")
    difficulty  = request.GET.get("difficulty", "")
    year_range  = request.GET.get("year", "")
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

    # -----------------------------
    # 난이도 필터
    # -----------------------------
    if difficulty and difficulty != "전체":
        print(">>> difficulty param:", difficulty)  # 디버깅용 로그

        try:
            d_int = int(difficulty)
        except ValueError:
            d_int = None

        if d_int is not None:
            # 숫자 / 문자열 두 경우 모두 고려 (0, "0")
            movies = movies.filter(
                Q(difficulty=d_int) | Q(difficulty=str(d_int))
            )
        else:
            # 숫자로 변환이 안 되면 문자열 그대로 비교 (예: "A1")
            movies = movies.filter(difficulty=difficulty)

        print(">>> after difficulty filter count:", movies.count())

    # -----------------------------
    # 연도 범위 필터
    # -----------------------------
    if year_range and year_range != "전체":
        try:
            start, end = year_range.split("~")
            start = int(start.strip())
            end   = int(end.strip())
            movies = movies.filter(year__gte=start, year__lte=end)
        except:
            pass  

    # -----------------------------
    # 정렬
    # -----------------------------
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

    # -----------------------------
    # JSON 변환
    # -----------------------------
    results = []
    for m in movies:
        if m.image.startswith("http://") or m.image.startswith("https://"):
            image_url = m.image
        else:
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
        # 이미지 경로 보정
        img = movie.image.strip()

        # DB에 movies/1.png 같이 저장된 경우 → movies/images/1.png 로 보정
        if not img.startswith("movies/images/"):
            img = "movies/images/" + img.lstrip("/")

        image_url = f"{request.scheme}://{request.get_host()}/static/{img}"



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
    score_raw = request.GET.get("score")
    type_raw = request.GET.get("type")

    print(">>> movies_recommend_api CALLED!", {"type": type_raw, "score": score_raw})

    # 1) 영화가 1편도 없으면 그냥 빈 리스트
    qs = MovieData.objects.all()
    if not qs.exists():
        print(">>> no movies in DB")
        return JsonResponse([], safe=False)

    # 2) 점수 숫자 변환 실패하면: 점수 무시하고 랜덤 추천
    try:
        score = float(score_raw)
    except (TypeError, ValueError):
        print(">>> invalid score, fallback to random")
        movies = qs.order_by("?")[:6]
        return JsonResponse(
            [
                {
                    "id": m.id,
                    "title_ko": m.title_ko,
                    "title_en": m.title_en,
                    "year": m.year,
                    "runtime": m.runtime,
                    "genre": m.genre,
                    "difficulty": m.difficulty,
                    "plot": m.plot,
                    "image": getattr(m.image, "url", m.image),
                }
                for m in movies
            ],
            safe=False,
        )

    # 3) 시험 종류별 난이도 레벨 계산 (0~5)
    if type_raw == "toeic":
        level = score_to_level_toeic(score)
    elif type_raw == "toefl":
        level = score_to_level_toefl(score)
    elif type_raw == "ielts":
        level = score_to_level_ielts(score)
    else:
        print(">>> invalid type, fallback to random")
        movies = qs.order_by("?")[:6]
        return JsonResponse(
            [
                {
                    "id": m.id,
                    "title_ko": m.title_ko,
                    "title_en": m.title_en,
                    "year": m.year,
                    "runtime": m.runtime,
                    "genre": m.genre,
                    "difficulty": m.difficulty,
                    "plot": m.plot,
                    "image": getattr(m.image, "url", m.image),
                }
                for m in movies
            ],
            safe=False,
        )

    if level is None:
        print(">>> level is None, fallback to random")
        movies = qs.order_by("?")[:6]
    else:
        print(">>> calculated level:", level)

        # 4) 1차: difficulty == level
        movies = qs.filter(difficulty=level)
        print(">>> difficulty == level count:", movies.count())

        # 5) 문자열로 저장된 경우도 (예: "3")
        if not movies.exists():
            movies = qs.filter(difficulty=str(level))
            print(">>> difficulty == str(level) count:", movies.count())

        # 6) 주변 난이도(±1)까지 허용 (0~5)
        if not movies.exists():
            low = max(0, level - 1)
            high = min(5, level + 1)
            movies = qs.filter(difficulty__gte=low, difficulty__lte=high)
            print(">>> difficulty in [%d, %d] count:" % (low, high), movies.count())

        # 7) 그래도 없으면 랜덤
        if not movies.exists():
            print(">>> still empty, fallback to random")
            movies = qs.order_by("?")[:6]

    # 8) 최종 결과 JSON 변환
    results = [
        {
            "id": m.id,
            "title_ko": m.title_ko,
            "title_en": m.title_en,
            "year": m.year,
            "runtime": m.runtime,
            "genre": m.genre,
            "difficulty": m.difficulty,
            "plot": m.plot,
            "image": getattr(m.image, "url", m.image),
        }
        for m in movies
    ]
    print(">>> final result count:", len(results))
    return JsonResponse(results, safe=False)



def score_to_level_toeic(score):
    # 0 ~ 990 → 0 ~ 5로 매핑
    if not (0 <= score <= 990):
        return None

    if score < 300:
        return 0   # A1
    elif score < 500:
        return 1   # A2
    elif score < 700:
        return 2   # B1
    elif score < 850:
        return 3   # B2
    elif score < 940:
        return 4   # C1
    else:
        return 5   # C2


def score_to_level_toefl(score):
    # 0 ~ 120 → 0 ~ 5로 매핑
    if not (0 <= score <= 120):
        return None

    if score < 30:
        return 0
    elif score < 50:
        return 1
    elif score < 70:
        return 2
    elif score < 90:
        return 3
    elif score < 105:
        return 4
    else:
        return 5


def score_to_level_ielts(score):
    # 0 ~ 9.0 → 0 ~ 5로 매핑
    if not (0 <= score <= 9.0):
        return None

    if score < 3.0:
        return 0
    elif score < 4.0:
        return 1
    elif score < 5.5:
        return 2
    elif score < 6.5:
        return 3
    elif score < 7.5:
        return 4
    else:
        return 5


@csrf_exempt
@require_POST
def comment_create_api(request, movie_id):
    """
    영화 리뷰(댓글) 작성 API
    - POST /api/movies/<movie_id>/comments/
    - body: content (FormData)
    - 헤더: Authorization: Bearer <access>  (없으면 401)
    """
    # 0) JWT 토큰 유무 확인 (간단 체크)
    auth_header = request.META.get("HTTP_AUTHORIZATION", "")
    if not auth_header.startswith("Bearer "):
        return JsonResponse({"error": "로그인이 필요합니다."}, status=401)

    # 1) 내용 가져오기
    content = request.POST.get("content", "").strip()
    if not content:
        return JsonResponse({"error": "리뷰 내용을 입력해주세요."}, status=400)

    # 2) 영화 찾기
    try:
        movie = MovieData.objects.get(id=movie_id)
    except MovieData.DoesNotExist:
        return JsonResponse({"error": "영화를 찾을 수 없습니다."}, status=404)

    # 3) 유저 설정 (임시: 첫 번째 유저 사용)
    user = request.user if getattr(request, "user", None) and request.user.is_authenticated else None
    if user is None:
        user = User.objects.first()  # 과제/시연용, 실제 서비스면 JWT에서 추출

    # 4) 댓글 생성
    comment = Comment.objects.create(
        movie=movie,
        user=user,
        content=content,
    )

    # 5) 응답 JSON
    return JsonResponse({
        "message": "리뷰가 등록되었습니다.",
        "comment": {
            "user": comment.user.username,
            "content": comment.content,
            "created": comment.created_time.strftime("%Y-%m-%d %H:%M"),
        }
    })



def frontend_home(request):
    return render(request, "home.html")
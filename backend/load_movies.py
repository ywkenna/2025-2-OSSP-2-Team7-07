import os
import django
import pandas as pd

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

from movies.models import MovieData


EXCEL_PATH = "movie_list.xlsx"  # 실제 파일명으로 변경해줘


df = pd.read_excel(EXCEL_PATH)

for _, row in df.iterrows():

    movie = MovieData(
        # 엑셀 컬럼 매핑
        title_ko=row.get("2005-2025 top movies", ""),
        title_en=row.get("영문", ""),
        year=row.get("개봉연도"),
        genre=row.get("장르 태그", ""),
        runtime=row.get("영화 길이"),

        # 지금 엑셀엔 없는 값 → 기본값 또는 None
        image="",          # 나중에 이미지 연결
        plot="",           # 줄거리 없음
        difficulty=None,   # 난이도 없음

        # 추가 지표들 전부 None
        word_avg_level=None,
        tree_depth=None,
        pron_acc=None,
        real_word=None,
        clause_ratio=None,
        overlap_ratio=None,
        phrase_ratio=None,
        pp_ratio=None,
        rare_word_ratio=None,
        slang_ratio=None,
        syllable_word=None,
        avg_speed=None,
        lev_distance=None,

        wavve_url=None,
        watcha_url=None,
        netflix_url=None,
        tiving_url=None,
        coupang_url=None,
        disney_url=None,
    )

    movie.save()

print("✔ 영화 데이터 삽입 완료!")

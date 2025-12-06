import os
import django
import pandas as pd

# 1) 장고 세팅 로드
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

from movies.models import MovieData

# 2) 엑셀 경로
EXCEL_PATH = r"C:\Users\hyera\Downloads\전체 영화 데이터 feature와 도출된 최종 난이도.xlsx"

df = pd.read_excel(EXCEL_PATH)

UPDATED = 0
SKIPPED = 0

for _, row in df.iterrows():
    movie_no = row.get("영화 번호")

    if pd.isna(movie_no):
        SKIPPED += 1
        continue

    try:
        movie_id = int(movie_no)
    except ValueError:
        print(f"[SKIP] 영화 번호 값 이상함: {movie_no}")
        SKIPPED += 1
        continue

    try:
        movie = MovieData.objects.get(id=movie_id)
    except MovieData.DoesNotExist:
        print(f"[SKIP] id={movie_id} 인 MovieData 없음")
        SKIPPED += 1
        continue

    # ====== 컬럼 매핑 ======
    # 엑셀 컬럼 이름 그대로 사용
    movie.overlap_ratio  = row.get("중첩발화비율_정규화_ratio")
    movie.avg_speed      = row.get("속도 평균")
    movie.real_word      = row.get("실질 단어 비율")
    movie.syllable_word  = row.get("단어 당 음절 수")
    movie.clause_ratio   = row.get("평균 절 비율")
    movie.pp_ratio       = row.get("평균 과거 분사 비율")
    movie.tree_depth     = row.get("평균 트리 깊이")
    movie.word_avg_level = row.get("평균난이도(가중)")
    movie.phrase_ratio   = row.get("숙어비율(%)")
    movie.slang_ratio    = row.get("슬랭비율(%)")
    movie.rare_word_ratio = row.get("희귀단어비율(%)")
    movie.lev_distance   = row.get("lev_distance")
    movie.pron_acc       = row.get("pronounce_accuracy")

    # 난이도(도출된 결과) → difficulty
    diff = row.get("도출된 결과")
    if pd.isna(diff):
        movie.difficulty = None
    else:
        try:
            movie.difficulty = int(diff)
        except ValueError:
            # 혹시 실수형으로 들어가 있으면 반올림
            movie.difficulty = int(round(float(diff)))

    movie.save()
    UPDATED += 1

print(f"✅ 업데이트 완료: {UPDATED}개, 스킵: {SKIPPED}개")

import pandas as pd
from movies.models import MovieData

df = pd.read_excel(r"C:\Users\hyera\Downloads\전체 영화 데이터 feature와 도출된 최종 난이도.xlsx")

MAX_TREE_DEPTH = 15
MAX_SPEED = 7.0   # 속도 평균의 최대값을 7로 가정(필요하면 조정 가능)

for _, row in df.iterrows():
    movie_id = int(row["영화 번호"])

    try:
        movie = MovieData.objects.get(id=movie_id)
    except MovieData.DoesNotExist:
        continue

    # 정규화
    movie.word_avg_level = row["평균난이도(가중)"] / 5
    movie.phrase_ratio = row["숙어비율(%)"] / 100
    movie.slang_ratio = row["슬랭비율(%)"] / 100
    movie.rare_word_ratio = row["희귀단어비율(%)"] / 100

    movie.clause_ratio = row["평균 절 비율"]  # 이미 0~1
    movie.past_ratio = row["평균 과거 분사 비율"]  # 0~1

    movie.tree_depth = row["평균 트리 깊이"] / MAX_TREE_DEPTH
    movie.avg_speed = row["속도 평균"] / MAX_SPEED

    movie.pron_acc = row["pronounce_accuracy"]  # 0~1
    movie.overlap_ratio = row["중첩발화비율_정규화_ratio"]  # 0~1

    movie.save()

print("데이터 업데이트 완료!")

import pandas as pd
from .models import MovieData

def run():
    file_path = "영화 리스트 및 추가 정보 한글제목 수정본(개봉연도, 장르태그, 영화 길이).xlsx"
    df = pd.read_excel(file_path)

    for idx, row in df.iterrows():
        # "1. 다크나이트" → "다크나이트"
        raw_title = str(row["2005-2025 top movies"])
        title_ko = raw_title.split(". ", 1)[1] if ". " in raw_title else raw_title

        MovieData.objects.create(
            image=f"movies/images/{idx+1}.png",   # <<<<<<<<<< 여기!
            title_ko=title_ko,
            title_en=row["영문"],
            year=int(row["개봉연도"]),
            plot="",
            runtime=int(row["영화 길이"]),
            genre=row["장르 태그"],
            difficulty=0,
            word_avg_level=0,
            tree_depth=0,
            pron_acc=0,
            real_world=0,
        )

    print("엑셀 데이터 DB 저장 완료!")



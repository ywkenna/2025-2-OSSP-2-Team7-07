import os
import pandas as pd
from .models import MovieData

def run():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    file_path = os.path.join(base_dir, "data", "movie_data.csv")
    df = pd.read_csv(file_path)
    
    #공백 열 제거
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

    for idx, row in df.iterrows():
        MovieData.objects.create(
            image=row["image"],
            title_ko=row["title_ko"],
            title_en=row["title_en"],
            year=row["year"],
            plot=row["plot"],
            runtime=row["runtime"],
            genre=row["genre"],
            difficulty=row["difficulty"],

            word_avg_level=row["word_avg_level"],
            tree_depth=row["tree_depth"],
            pron_acc=row["pron_acc"],
            real_word=row["real_word"],
            clause_ratio=row["clause_ratio"],
            overlap_ratio=row["overlap_ratio"],
            phrase_ratio=row["phrase_ratio"],
            pp_ratio=row["pp_ratio"],
            rare_word_ratio=row["rare_word_ratio"],
            slang_ratio=row["slang_ratio"],
            syllable_word=row["syllable_word"],
            avg_speed=row["avg_speed"],
            lev_distance=row["lev_distance"],

            wavve_url=row.get("wavve_url", None),
            watcha_url=row.get("watcha_url", None),
            netflix_url=row.get("netflix_url", None),
            tiving_url=row.get("tiving_url", None),
            coupang_url=row.get("coupang_url", None),
            disney_url=row.get("disney_url", None),
        )

    print("movie_data.csv - DB 저장 완료")



import csv
from movies.models import MovieData

def to_int(v):
    v = (v or "").strip()
    return int(float(v)) if v != "" else 0

def to_float(v):
    v = (v or "").strip()
    return float(v) if v != "" else 0.0

def run():
    path = "data/movie_data.csv"

    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            raw_image = (row["image"] or "").strip()

            if raw_image.startswith("http://") or raw_image.startswith("https://"):
                image_path = raw_image
            else:
                image_path = f"movies/images/{raw_image.lstrip('/')}"

            MovieData.objects.create(
                image           = image_path,
                title_ko        = row["title_ko"],
                title_en        = row["title_en"],
                year            = to_int(row["year"]),
                plot            = row["plot"],
                runtime         = to_int(row["runtime"]),
                genre           = row["genre"],
                difficulty      = to_int(row["difficulty"]),

                word_avg_level  = to_float(row["word_avg_level"]),
                tree_depth      = to_float(row["tree_depth"]),
                pron_acc        = to_float(row["pron_acc"]),
                real_word       = to_float(row["real_word"]),
                clause_ratio    = to_float(row["clause_ratio"]),
                overlap_ratio   = to_float(row["overlap_ratio"]),
                phrase_ratio    = to_float(row["phrase_ratio"]),
                pp_ratio        = to_float(row["pp_ratio"]),
                rare_word_ratio = to_float(row["rare_word_ratio"]),
                slang_ratio     = to_float(row["slang_ratio"]),
                syllable_word   = to_float(row["syllable_word"]),
                avg_speed       = to_float(row["avg_speed"]),
                lev_distance    = to_float(row["lev_distance"]),

                wavve_url       = (row.get("wavve_url") or "").strip() or None,
                watcha_url      = (row.get("watcha_url") or "").strip() or None,
                netflix_url     = (row.get("netflix_url") or "").strip() or None,
                tiving_url      = (row.get("tiving_url") or "").strip() or None,
                coupang_url     = (row.get("coupang_url") or "").strip() or None,
                disney_url      = (row.get("disney_url") or "").strip() or None,
            )

    print("CSV → DB 입력 완료!")
